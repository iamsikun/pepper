from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from pepper.manifest import InstallManifest
from pepper.project import assemble_paper, camera_ready, create_journal_version, new_paper, set_target, write_workflow_brief
from pepper.renderers import render_claude_system_prompt, render_codex_system_prompt
from pepper.sync import MANIFEST_PATH, dev_sync_root, find_repo_root, install_or_sync
from pepper.validate import validate_repo


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    return repo


def test_find_repo_root_walks_up(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    nested = repo / "a" / "b"
    nested.mkdir(parents=True)
    assert find_repo_root(nested) == repo


def test_install_writes_both_adapter_sets_and_manifest(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    result = install_or_sync(repo, adapters="claude,codex")
    assert result.conflicts == []

    manifest = InstallManifest.load(repo / MANIFEST_PATH)
    assert manifest is not None
    assert manifest.adapters == ["claude", "codex"]
    assert ".claude/settings.json" in manifest.managed_files
    assert ".pepper/adapters/codex/workflows/new-paper.md" in manifest.managed_files

    assert "<!-- pepper:start -->" in (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "<!-- pepper:start -->" in (repo / "AGENTS.md").read_text(encoding="utf-8")
    assert (repo / ".claude/commands/new-paper.md").exists()
    assert (repo / ".pepper/adapters/codex/roles/intro-writer.md").exists()


def test_install_can_limit_to_codex_only(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    result = install_or_sync(repo, adapters="codex")
    assert result.conflicts == []
    manifest = InstallManifest.load(repo / MANIFEST_PATH)
    assert manifest is not None
    assert manifest.adapters == ["codex"]
    assert not (repo / ".claude").exists()
    assert not (repo / "CLAUDE.md").exists()
    assert (repo / "AGENTS.md").exists()


def test_sync_detects_local_conflict(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex")
    target = repo / ".claude/settings.json"
    target.write_text('{"modified": true}\n', encoding="utf-8")
    result = install_or_sync(repo, adapters="claude,codex")
    assert ".claude/settings.json" in result.conflicts


def test_dev_sync_root_prunes_removed_generated_files(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex", force=True, write_manifest=False)
    stale = repo / ".pepper/adapters/codex/roles/stale.md"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("stale\n", encoding="utf-8")
    dev_sync_root(repo, adapters="claude,codex")
    assert not stale.exists()


def test_validate_is_adapter_aware(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="codex")
    result = validate_repo(repo)
    assert result.ok

    agents = repo / "AGENTS.md"
    agents.unlink()
    result = validate_repo(repo)
    assert not result.ok
    assert any("missing Codex adapter file" in error for error in result.errors)


def test_new_paper_creates_workspace_and_context(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex")
    (repo / "docs").mkdir()
    (repo / "src").mkdir()

    target = new_paper(
        repo,
        title="Optimal Pricing with LLMs",
        topic="We study dynamic pricing with language-model-assisted demand inference.",
        contributions=["A new demand estimator", "A policy regret bound"],
        venue_key="neurips",
        paper_type="Theory+Experiments",
    )

    assert target == "conference"
    state = yaml.safe_load((repo / "paper/state.yaml").read_text(encoding="utf-8"))
    assert state["active_target"] == "conference"
    assert (repo / "paper/conference/target.yaml").exists()
    context = (repo / "paper/shared/context.md").read_text(encoding="utf-8")
    assert "Optimal Pricing with LLMs" in context
    assert "Documentation: docs" in context


def test_set_target_and_create_journal_version(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex")
    new_paper(
        repo,
        title="Paper",
        topic="Topic",
        contributions=["One"],
        venue_key="neurips",
        paper_type="Theory",
    )
    create_journal_version(repo, venue_key="econometrica", activate=True)
    metadata = set_target(repo, "journal")
    assert metadata["venue"] == "econometrica"
    state = yaml.safe_load((repo / "paper/state.yaml").read_text(encoding="utf-8"))
    assert state["active_target"] == "journal"


def test_assemble_and_camera_ready_generate_outputs(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex")
    new_paper(
        repo,
        title="Paper",
        topic="Topic",
        contributions=["One"],
        venue_key="neurips",
        paper_type="Theory",
    )
    sections = repo / "paper/conference/sections"
    (sections / "abstract.tex").write_text("A concise abstract.\n", encoding="utf-8")
    (sections / "introduction.tex").write_text("\\section{Introduction}\nIntro.\n", encoding="utf-8")
    (sections / "methodology.tex").write_text("\\section{Method}\nMethod.\n", encoding="utf-8")
    (repo / "paper/conference/references.bib").write_text("", encoding="utf-8")

    main_path = assemble_paper(repo)
    assert main_path.exists()
    assert "\\input{sections/introduction}" in main_path.read_text(encoding="utf-8")

    zip_path = camera_ready(repo)
    assert zip_path.exists()
    assert (repo / "paper/conference/camera-ready/VERIFICATION.md").exists()


def test_workflow_brief_writes_runtime_brief(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    install_or_sync(repo, adapters="claude,codex")
    path = write_workflow_brief(repo, "draft-paper", guidance="Keep it concise.")
    text = path.read_text(encoding="utf-8")
    assert "Pepper Workflow Brief: draft-paper" in text
    assert "Keep it concise." in text


def test_rendered_system_prompts_reference_cli() -> None:
    assert "canonical interface" in render_claude_system_prompt().lower()
    assert "canonical interface" in render_codex_system_prompt().lower()


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
