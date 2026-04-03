from __future__ import annotations

import hashlib
from dataclasses import dataclass
from importlib import metadata
from importlib.resources import files
from pathlib import Path
from typing import Iterable

from .manifest import InstallManifest
from .renderers import CORE_SCOPE, DEFAULT_ADAPTERS, managed_files_by_scope, normalize_adapters, rendered_adapter_assets, rendered_marker_files

PACKAGE_NAME = "pepper"
SCAFFOLD_DIR = ".pepper"
MARKER_START = "<!-- pepper:start -->"
MARKER_END = "<!-- pepper:end -->"
GITIGNORE_START = "# pepper:start"
GITIGNORE_END = "# pepper:end"
MANIFEST_PATH = Path(f"{SCAFFOLD_DIR}/install-manifest.json")
EXCLUDED_ASSET_SUFFIXES = {
    ".DS_Store",
    "settings.local.json",
    "install.sh",
    "validate.sh",
    "neurips.sty",
}
EXCLUDED_ASSET_PREFIXES = (
    ".claude/",
    "CLAUDE.template.md",
)
ROOT_EXTRA_KEEP = {
    ".claude/settings.local.json",
    f"{SCAFFOLD_DIR}/scripts/install.sh",
    f"{SCAFFOLD_DIR}/scripts/validate.sh",
}
GITIGNORE_LINES = [
    "paper/**/camera-ready/",
    "paper/**/submission/",
    "paper/**/*.aux",
    "paper/**/*.bbl",
    "paper/**/*.blg",
    "paper/**/*.fdb_latexmk",
    "paper/**/*.fls",
    "paper/**/*.log",
    "paper/**/*.out",
    "paper/**/*.synctex.gz",
]


@dataclass(slots=True)
class SyncResult:
    written_files: list[str]
    conflicts: list[str]


def package_version() -> str:
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return "0.0.0+local"


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "pyproject.toml").exists():
            return candidate
    return current


def _walk_resources(node, prefix: str = "") -> dict[str, bytes]:
    assets: dict[str, bytes] = {}
    for child in sorted(node.iterdir(), key=lambda item: item.name):
        relative = f"{prefix}/{child.name}" if prefix else child.name
        if any(relative == excluded or relative.startswith(excluded) for excluded in EXCLUDED_ASSET_PREFIXES):
            continue
        if child.is_dir():
            assets.update(_walk_resources(child, relative))
            continue
        if any(relative.endswith(suffix) for suffix in EXCLUDED_ASSET_SUFFIXES):
            continue
        assets[relative] = child.read_bytes()
    return assets


def static_asset_bytes_by_path() -> dict[str, bytes]:
    root = files(PACKAGE_NAME).joinpath("assets")
    return _walk_resources(root)


def asset_bytes_by_path(adapters: str | list[str] | tuple[str, ...] | None = None) -> dict[str, bytes]:
    normalized = normalize_adapters(adapters)
    assets = static_asset_bytes_by_path()
    assets.update(rendered_adapter_assets(normalized))
    return assets


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: Path) -> str:
    return hash_bytes(path.read_bytes())


def _replace_or_append_block(existing: str, start: str, end: str, body: str) -> str:
    block = f"{start}\n{body.rstrip()}\n{end}\n"
    if existing.strip() == body.rstrip():
        return block
    if start in existing and end in existing:
        before, remainder = existing.split(start, 1)
        _, after = remainder.split(end, 1)
        return before.rstrip("\n") + "\n\n" + block + after.lstrip("\n")
    if not existing.strip():
        return block
    return existing.rstrip() + "\n\n" + block


def _remove_managed_block(existing: str, start: str, end: str) -> str:
    if start not in existing or end not in existing:
        return existing
    before, remainder = existing.split(start, 1)
    _, after = remainder.split(end, 1)
    cleaned = (before.rstrip("\n") + "\n\n" + after.lstrip("\n")).strip()
    return cleaned + ("\n" if cleaned else "")


def _write_marker_file(path: Path, start: str, end: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    updated = _replace_or_append_block(existing, start, end, body)
    path.write_text(updated, encoding="utf-8")


def _remove_marker_file_block(path: Path, start: str, end: str) -> None:
    if not path.exists():
        return
    existing = path.read_text(encoding="utf-8")
    updated = _remove_managed_block(existing, start, end)
    if updated:
        path.write_text(updated, encoding="utf-8")
    else:
        path.unlink()


def _ensure_marker_files(repo_root: Path, adapters: tuple[str, ...]) -> None:
    marker_files = rendered_marker_files(adapters)
    for relative, body in marker_files.items():
        _write_marker_file(repo_root / relative, MARKER_START, MARKER_END, body)
    for obsolete in {"CLAUDE.md", "AGENTS.md"} - set(marker_files):
        _remove_marker_file_block(repo_root / obsolete, MARKER_START, MARKER_END)
    _write_marker_file(repo_root / ".gitignore", GITIGNORE_START, GITIGNORE_END, "\n".join(GITIGNORE_LINES))


def _prune_empty_dirs(directory: Path, stop: Path) -> None:
    current = directory
    while current != stop and current.exists() and current.is_dir() and not any(current.iterdir()):
        parent = current.parent
        current.rmdir()
        current = parent


def install_or_sync(
    repo_root: Path,
    *,
    force: bool = False,
    write_manifest: bool = True,
    adapters: str | list[str] | tuple[str, ...] | None = None,
) -> SyncResult:
    normalized_adapters = normalize_adapters(adapters)
    assets = asset_bytes_by_path(normalized_adapters)
    manifest_path = repo_root / MANIFEST_PATH
    existing_manifest = InstallManifest.load(manifest_path)
    conflicts: list[str] = []
    hashes: dict[str, str] = {}
    writes: list[tuple[str, bytes]] = []
    deletes: list[str] = []

    for relative_path, payload in assets.items():
        destination = repo_root / relative_path
        desired_hash = hash_bytes(payload)
        hashes[relative_path] = desired_hash
        if destination.exists():
            current_hash = hash_file(destination)
            if existing_manifest and relative_path in existing_manifest.hashes:
                known_hash = existing_manifest.hashes[relative_path]
                if current_hash != known_hash and current_hash != desired_hash and not force:
                    conflicts.append(relative_path)
                    continue
            elif current_hash != desired_hash and not force:
                conflicts.append(relative_path)
                continue
            if current_hash == desired_hash:
                continue
        writes.append((relative_path, payload))

    if existing_manifest:
        obsolete_paths = sorted(set(existing_manifest.managed_files) - set(assets))
        for relative_path in obsolete_paths:
            destination = repo_root / relative_path
            if not destination.exists():
                continue
            current_hash = hash_file(destination)
            known_hash = existing_manifest.hashes.get(relative_path)
            if known_hash and current_hash != known_hash and not force:
                conflicts.append(relative_path)
                continue
            deletes.append(relative_path)

    if conflicts:
        return SyncResult(written_files=[], conflicts=sorted(conflicts))

    written_files: list[str] = []
    for relative_path, payload in writes:
        destination = repo_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        written_files.append(relative_path)

    for relative_path in deletes:
        destination = repo_root / relative_path
        if destination.exists():
            destination.unlink()
            written_files.append(relative_path)
            _prune_empty_dirs(destination.parent, repo_root)

    _ensure_marker_files(repo_root, normalized_adapters)
    if write_manifest:
        InstallManifest.create(
            package_version(),
            adapters=list(normalized_adapters),
            managed_files_by_scope=managed_files_by_scope(normalized_adapters, list(assets)),
            hashes=hashes,
        ).save(manifest_path)
    return SyncResult(written_files=written_files, conflicts=[])


def _iter_root_managed_files(repo_root: Path) -> Iterable[Path]:
    for relative in (".claude", SCAFFOLD_DIR):
        root = repo_root / relative
        if not root.exists():
            continue
        yield from (path for path in root.rglob("*") if path.is_file())


def dev_sync_root(repo_root: Path, *, adapters: str | list[str] | tuple[str, ...] | None = None) -> SyncResult:
    normalized_adapters = normalize_adapters(adapters)
    result = install_or_sync(repo_root, force=True, write_manifest=False, adapters=normalized_adapters)
    managed_files = set(asset_bytes_by_path(normalized_adapters))
    for path in _iter_root_managed_files(repo_root):
        relative = path.relative_to(repo_root).as_posix()
        if relative in managed_files or relative in ROOT_EXTRA_KEEP:
            continue
        path.unlink()
        _prune_empty_dirs(path.parent, repo_root)
    for base in (repo_root / ".claude", repo_root / SCAFFOLD_DIR):
        if not base.exists():
            continue
        for directory in sorted(base.rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    return result
