from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .manifest import InstallManifest
from .sync import MANIFEST_PATH

BANNED_PATTERNS = ("projects/", "papers/", "workspace/", "current-paper.md", "literature/references")
SCAFFOLD_DIR = Path(".pepper")
CORE_REQUIRED = (Path(".pepper/config.yaml"),)
CLAUDE_REQUIRED = (Path("CLAUDE.md"), Path(".claude/settings.json"), Path(".claude/agents"), Path(".claude/commands"))
CODEX_REQUIRED = (
    Path("AGENTS.md"),
    Path(".pepper/adapters/codex/roles"),
    Path(".pepper/adapters/codex/workflows"),
)


@dataclass(slots=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_adapters(repo_root: Path) -> tuple[str, ...]:
    manifest = InstallManifest.load(repo_root / MANIFEST_PATH)
    if manifest is not None:
        return tuple(manifest.adapters)
    inferred: list[str] = []
    if (repo_root / ".claude").exists() or (repo_root / "CLAUDE.md").exists():
        inferred.append("claude")
    if (repo_root / "AGENTS.md").exists() or (repo_root / ".pepper/adapters/codex").exists():
        inferred.append("codex")
    return tuple(inferred)


def _scan_markdown_tree(root: Path, result: ValidationResult, repo_root: Path) -> None:
    if not root.exists():
        result.warnings.append(f"missing prompt directory: {root.relative_to(repo_root).as_posix()}")
        return
    for file_path in sorted(root.rglob("*.md")):
        content = file_path.read_text(encoding="utf-8")
        for pattern in BANNED_PATTERNS:
            if pattern in content:
                rel = file_path.relative_to(repo_root).as_posix()
                result.errors.append(f"{rel} contains banned pattern '{pattern}'")


def _check_required_files(repo_root: Path, result: ValidationResult, adapters: tuple[str, ...]) -> None:
    for required_path in CORE_REQUIRED:
        if not (repo_root / required_path).exists():
            result.errors.append(f"missing required scaffold file: {required_path.as_posix()}")
    if "claude" in adapters:
        for required_path in CLAUDE_REQUIRED:
            if not (repo_root / required_path).exists():
                result.errors.append(f"missing Claude adapter file: {required_path.as_posix()}")
    if "codex" in adapters:
        for required_path in CODEX_REQUIRED:
            if not (repo_root / required_path).exists():
                result.errors.append(f"missing Codex adapter file: {required_path.as_posix()}")


def _scan_prompt_paths(repo_root: Path, result: ValidationResult, adapters: tuple[str, ...]) -> None:
    if "claude" in adapters:
        _scan_markdown_tree(repo_root / ".claude/agents", result, repo_root)
        _scan_markdown_tree(repo_root / ".claude/commands", result, repo_root)
    if "codex" in adapters:
        _scan_markdown_tree(repo_root / ".pepper/adapters/codex/roles", result, repo_root)
        _scan_markdown_tree(repo_root / ".pepper/adapters/codex/workflows", result, repo_root)


def _check_templates(repo_root: Path, result: ValidationResult) -> None:
    templates_root = repo_root / SCAFFOLD_DIR / "templates"
    if not templates_root.exists():
        result.errors.append(".pepper/templates is missing")
        return
    for venue_dir in sorted(path for path in templates_root.iterdir() if path.is_dir()):
        if not (venue_dir / "template-manifest.yaml").exists():
            result.errors.append(f"{venue_dir.relative_to(repo_root).as_posix()} is missing template-manifest.yaml")
        if not (venue_dir / "main.tex").exists():
            result.warnings.append(f"{venue_dir.relative_to(repo_root).as_posix()} is missing main.tex")


def _check_runtime_state(repo_root: Path, result: ValidationResult) -> None:
    paper_root = repo_root / "paper"
    if not paper_root.exists():
        return
    state_file = paper_root / "state.yaml"
    if not state_file.exists():
        result.errors.append("paper/state.yaml is missing")
        return
    state_data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
    active_target = state_data.get("active_target")
    if not active_target:
        result.errors.append("paper/state.yaml is missing active_target")
        return
    if not (paper_root / str(active_target)).exists():
        result.errors.append(f"paper/{active_target} is missing")
    if not (paper_root / "shared/context.md").exists():
        result.warnings.append("paper/shared/context.md is missing")

    camera_ready = any(
        target_data.get("stage") == "camera-ready"
        for target_data in (state_data.get("targets") or {}).values()
        if isinstance(target_data, dict)
    )
    tex_files = list(paper_root.glob("*/main.tex")) + list(paper_root.glob("*/sections/*.tex"))
    label_locations: dict[str, list[str]] = {}
    for tex_file in tex_files:
        text = tex_file.read_text(encoding="utf-8", errors="ignore")
        rel = tex_file.relative_to(repo_root).as_posix()
        if r"\ref{??}" in text or r"\cite{??}" in text:
            result.errors.append(f"{rel} has unresolved placeholder references")
        if camera_ready and "TODO" in text:
            result.errors.append(f"{rel} contains TODO while in camera-ready stage")
        for match in re.finditer(r"\\label\{([^}]+)\}", text):
            label_locations.setdefault(match.group(1), []).append(rel)
    for label, files in label_locations.items():
        if len(files) > 1:
            result.warnings.append(f"duplicate \\label{{{label}}} in: {', '.join(files)}")


def validate_repo(repo_root: Path) -> ValidationResult:
    result = ValidationResult()
    adapters = _load_adapters(repo_root)
    _check_required_files(repo_root, result, adapters)
    _scan_prompt_paths(repo_root, result, adapters)
    _check_templates(repo_root, result)
    _check_runtime_state(repo_root, result)
    return result
