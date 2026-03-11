from __future__ import annotations

import json
import os
import subprocess
import sys
import hashlib
from pathlib import Path

from pepper.sync import MANIFEST_PATH, dev_sync_root, find_repo_root, install_or_sync
from pepper.validate import validate_repo


def test_find_repo_root_walks_up(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    nested = repo / "a" / "b"
    nested.mkdir(parents=True)
    (repo / ".git").mkdir()
    assert find_repo_root(nested) == repo


def test_install_writes_manifest_and_marker_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    result = install_or_sync(repo)
    assert result.conflicts == []
    manifest = json.loads((repo / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert manifest["managed_files"]
    claude_text = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "<!-- pepper:start -->" in claude_text
    gitignore_text = (repo / ".gitignore").read_text(encoding="utf-8")
    assert "# pepper:start" in gitignore_text


def test_sync_detects_local_conflict(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    install_or_sync(repo)
    target = repo / ".claude/settings.json"
    target.write_text('{"modified": true}\n', encoding="utf-8")
    result = install_or_sync(repo)
    assert ".claude/settings.json" in result.conflicts


def test_dev_sync_root_prunes_removed_packaged_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    install_or_sync(repo, force=True, write_manifest=False)
    stale = repo / ".pepper/templates/neurips/neurips.sty"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("stale\n", encoding="utf-8")
    dev_sync_root(repo)
    assert not stale.exists()


def test_sync_removes_obsolete_managed_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    install_or_sync(repo)
    obsolete = repo / ".claude/obsolete.md"
    obsolete.write_text("old\n", encoding="utf-8")
    manifest_path = repo / MANIFEST_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["managed_files"].append(".claude/obsolete.md")
    manifest["hashes"][".claude/obsolete.md"] = hashlib.sha256(b"old\n").hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = install_or_sync(repo)
    assert result.conflicts == []
    assert not obsolete.exists()


def test_validate_reports_legacy_prompt_pattern(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    install_or_sync(repo)
    prompt = repo / ".claude/commands/new-paper.md"
    prompt.write_text("legacy projects/path\n", encoding="utf-8")
    result = validate_repo(repo)
    assert not result.ok
    assert any("banned pattern" in error for error in result.errors)


def test_python_module_version_command() -> None:
    env = {**os.environ, "PYTHONPATH": "src"}
    completed = subprocess.run(
        [sys.executable, "-m", "pepper", "version"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert completed.returncode == 0
    assert "package version:" in completed.stdout
