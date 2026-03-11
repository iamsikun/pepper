from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


BANNED_PATTERNS = ("projects/", "papers/", "workspace/", "current-paper.md", "literature/references")
PROMPT_DIRS = (Path(".claude/agents"), Path(".claude/commands"))
REQUIRED_FILES = (Path("CLAUDE.md"), Path(".claude/settings.json"))
SCAFFOLD_DIR = Path(".pepper")


@dataclass(slots=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _scan_prompt_paths(repo_root: Path, result: ValidationResult) -> None:
    for prompt_dir in PROMPT_DIRS:
        full_dir = repo_root / prompt_dir
        if not full_dir.exists():
            result.warnings.append(f"missing prompt directory: {prompt_dir.as_posix()}")
            continue
        for file_path in sorted(full_dir.glob("*.md")):
            content = file_path.read_text(encoding="utf-8")
            for pattern in BANNED_PATTERNS:
                if pattern in content:
                    result.errors.append(f"{file_path.relative_to(repo_root).as_posix()} contains banned pattern '{pattern}'")


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
    state_text = state_file.read_text(encoding="utf-8")
    active_match = re.search(r"^active_target:\s*(\w+)\s*$", state_text, re.MULTILINE)
    if not active_match:
        result.errors.append("paper/state.yaml is missing active_target")
        return
    active_target = active_match.group(1)
    if not (paper_root / active_target).exists():
        result.errors.append(f"paper/{active_target} is missing")
    if not (paper_root / "shared/context.md").exists():
        result.warnings.append("paper/shared/context.md is missing")
    camera_ready = "stage: camera-ready" in state_text
    tex_files = list(paper_root.glob("*/main.tex")) + list(paper_root.glob("*/sections/*.tex"))
    for tex_file in tex_files:
        text = tex_file.read_text(encoding="utf-8", errors="ignore")
        if r"\ref{??}" in text or r"\cite{??}" in text:
            result.errors.append(f"{tex_file.relative_to(repo_root).as_posix()} has unresolved placeholder references")
        if camera_ready and "TODO" in text:
            result.errors.append(f"{tex_file.relative_to(repo_root).as_posix()} contains TODO while in camera-ready stage")


def validate_repo(repo_root: Path) -> ValidationResult:
    result = ValidationResult()
    for required_path in REQUIRED_FILES:
        if not (repo_root / required_path).exists():
            result.errors.append(f"missing required scaffold file: {required_path.as_posix()}")
    if not (repo_root / SCAFFOLD_DIR / "config.yaml").exists():
        result.errors.append("missing required scaffold file: .pepper/config.yaml")
    _scan_prompt_paths(repo_root, result)
    _check_templates(repo_root, result)
    _check_runtime_state(repo_root, result)
    return result
