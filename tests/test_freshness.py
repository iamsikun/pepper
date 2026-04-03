"""Verify that committed rendered files match current core_specs + renderers output.

If this test fails, someone edited core_specs.py or renderers.py without running
`pepper dev-sync-root` to regenerate the adapter files.
"""

from __future__ import annotations

from pathlib import Path

from pepper.manifest import InstallManifest
from pepper.renderers import DEFAULT_ADAPTERS, rendered_adapter_assets, rendered_marker_files
from pepper.sync import MANIFEST_PATH, MARKER_END, MARKER_START, find_repo_root

REPO_ROOT = find_repo_root(Path(__file__).parent)


def _installed_adapters() -> tuple[str, ...]:
    manifest = InstallManifest.load(REPO_ROOT / MANIFEST_PATH)
    if manifest is not None:
        return tuple(manifest.adapters)
    return DEFAULT_ADAPTERS


def _extract_managed_block(text: str) -> str | None:
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1:
        return None
    return text[start : end + len(MARKER_END)]


def test_committed_adapter_assets_are_fresh() -> None:
    adapters = _installed_adapters()
    expected = rendered_adapter_assets(adapters)
    stale: list[str] = []
    for relative_path, expected_bytes in expected.items():
        on_disk = REPO_ROOT / relative_path
        if not on_disk.exists():
            stale.append(f"{relative_path} (missing)")
            continue
        if on_disk.read_bytes() != expected_bytes:
            stale.append(relative_path)
    assert not stale, (
        f"These adapter files are stale: {', '.join(stale)}. "
        f"Run `pepper dev-sync-root` to regenerate."
    )


def test_committed_marker_files_are_fresh() -> None:
    adapters = _installed_adapters()
    expected_markers = rendered_marker_files(adapters)
    stale: list[str] = []
    for relative_path, expected_body in expected_markers.items():
        on_disk = REPO_ROOT / relative_path
        if not on_disk.exists():
            stale.append(f"{relative_path} (missing)")
            continue
        block = _extract_managed_block(on_disk.read_text(encoding="utf-8"))
        expected_block = f"{MARKER_START}\n{expected_body.rstrip()}\n{MARKER_END}"
        if block != expected_block:
            stale.append(relative_path)
    assert not stale, (
        f"These marker files are stale: {', '.join(stale)}. "
        f"Run `pepper dev-sync-root` to regenerate."
    )
