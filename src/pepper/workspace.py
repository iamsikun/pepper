from __future__ import annotations

import re
import textwrap
from datetime import date, datetime
from pathlib import Path

import yaml

from .core_specs import workflow_map

EXCLUDED_SCAN_DIRS = {".git", ".claude", ".pepper", "paper", "node_modules", ".venv", "dist", "__pycache__"}

_LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
_SECTION_RE = re.compile(r"\\(?:sub)?section\{([^}]+)\}")
CANONICAL_SECTION_ORDER = (
    "abstract.tex",
    "introduction.tex",
    "related_work.tex",
    "background.tex",
    "methodology.tex",
    "theory.tex",
    "experiments.tex",
    "empirics.tex",
    "conclusion.tex",
    "appendix_proofs.tex",
    "appendix_experiments.tex",
)
GRAPHIC_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps")


def _today() -> str:
    return date.today().isoformat()


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _load_config(repo_root: Path) -> dict:
    config_path = repo_root / ".pepper/config.yaml"
    if not config_path.exists():
        raise FileNotFoundError("missing .pepper/config.yaml; run `pepper install` first")
    return _load_yaml(config_path)


def _slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return value or "section"


def _detect_target_name(venue_config: dict) -> str:
    audience = str(venue_config.get("audience", "")).lower()
    return "conference" if audience == "ml" else "journal"


def _target_metadata(config: dict, venue_key: str, *, target_name: str | None = None) -> dict:
    venues = config.get("venues", {})
    if venue_key not in venues:
        available = ", ".join(sorted(venues))
        raise ValueError(f"unknown venue '{venue_key}'; available venues: {available}")
    venue = dict(venues[venue_key])
    resolved_target = target_name or _detect_target_name(venue)
    return {
        "name": resolved_target,
        "venue": venue_key,
        "template": venue["template_dir"],
        "mode": "blind" if venue.get("blind_review", True) else "submission",
        "page_limit": venue.get("page_limit"),
        "audience": venue.get("audience"),
        "format": venue.get("format"),
        "bibstyle": venue.get("bibstyle"),
    }


def scan_source_map(repo_root: Path) -> dict[str, list[str]]:
    config = _load_config(repo_root)
    patterns = config.get("source_categories", {})
    results: dict[str, set[str]] = {category: set() for category in patterns}
    for directory in sorted(path for path in repo_root.rglob("*") if path.is_dir()):
        rel = directory.relative_to(repo_root).as_posix()
        if not rel or any(part in EXCLUDED_SCAN_DIRS for part in directory.parts):
            continue
        rel_slash = f"{rel}/"
        for category, prefixes in patterns.items():
            if any(rel_slash.startswith(prefix) for prefix in prefixes):
                results.setdefault(category, set()).add(rel)
    return {category: sorted(paths) for category, paths in results.items() if paths}


def _context_markdown(
    *,
    title: str,
    topic: str,
    contributions: list[str],
    paper_type: str,
    source_map: dict[str, list[str]],
    import_notes: str | None = None,
) -> str:
    contribution_lines = "\n".join(f"{idx}. {item}" for idx, item in enumerate(contributions, start=1))
    source_lines = "\n".join(
        f"- {category.replace('_', ' ').title()}: {', '.join(paths)}"
        for category, paths in source_map.items()
    ) or "- No matching repo paths discovered"
    import_block = ""
    if import_notes:
        import_block = f"\n## Import Notes\n{import_notes.strip()}\n"
    return textwrap.dedent(
        f"""\
        # Paper Context

        ## Title
        {title}

        ## Topic
        {topic}

        ## Contributions
        {contribution_lines}

        ## Paper Type
        {paper_type}

        ## Source Map
        {source_lines}

        ## Key Files
        - Fill in important project-specific files here
        {import_block}
        """
    ).strip() + "\n"


def _initialize_shared_files(shared_root: Path) -> None:
    shared_root.mkdir(parents=True, exist_ok=True)
    (shared_root / "literature").mkdir(parents=True, exist_ok=True)
    (shared_root / "evidence").mkdir(parents=True, exist_ok=True)
    starter_files = {
        "claims.md": "# Claims and Evidence\n",
        "figure-plan.md": "# Figure Plan\n",
        "table-plan.md": "# Table Plan\n",
        "references-master.bib": "",
    }
    for name, content in starter_files.items():
        target = shared_root / name
        if not target.exists():
            target.write_text(content, encoding="utf-8")


def initialize_workspace(
    repo_root: Path,
    *,
    title: str,
    topic: str,
    contributions: list[str],
    venue_key: str,
    paper_type: str,
    source_map: dict[str, list[str]] | None = None,
    stage: str = "init",
    imported_from: str | None = None,
    import_mode: str | None = None,
    target_name: str | None = None,
) -> str:
    config = _load_config(repo_root)
    target = _target_metadata(config, venue_key, target_name=target_name)
    paper_root = repo_root / "paper"
    target_root = paper_root / target["name"]
    target_root.mkdir(parents=True, exist_ok=True)
    (target_root / "sections").mkdir(parents=True, exist_ok=True)
    (target_root / "figures").mkdir(parents=True, exist_ok=True)
    _initialize_shared_files(paper_root / "shared")

    state_path = paper_root / "state.yaml"
    state = _load_yaml(state_path)
    state.setdefault("targets", {})
    state["active_target"] = target["name"]
    state["initialized"] = True
    target_state = {
        "stage": stage,
        "created": state.get("targets", {}).get(target["name"], {}).get("created", _today()),
        "venue": venue_key,
    }
    if imported_from:
        state["imported_from"] = imported_from
    if import_mode:
        target_state["import_mode"] = import_mode
    state["targets"][target["name"]] = target_state
    _write_yaml(state_path, state)

    import_notes = None
    if imported_from:
        import_notes = f"- Imported from: `{imported_from}`\n- Import mode: `{import_mode or 'review'}`"
    context_text = _context_markdown(
        title=title,
        topic=topic,
        contributions=contributions,
        paper_type=paper_type,
        source_map=source_map or scan_source_map(repo_root),
        import_notes=import_notes,
    )
    (paper_root / "shared/context.md").write_text(context_text, encoding="utf-8")
    _write_yaml(target_root / "target.yaml", target)
    return target["name"]


def new_paper(
    repo_root: Path,
    *,
    title: str,
    topic: str,
    contributions: list[str],
    venue_key: str,
    paper_type: str,
) -> str:
    return initialize_workspace(
        repo_root,
        title=title,
        topic=topic,
        contributions=contributions,
        venue_key=venue_key,
        paper_type=paper_type,
        source_map=scan_source_map(repo_root),
    )


# -- State management ---------------------------------------------------------


def _load_state(repo_root: Path) -> dict:
    state_path = repo_root / "paper/state.yaml"
    if not state_path.exists():
        raise FileNotFoundError("paper/state.yaml is missing; initialize the workspace first")
    return _load_yaml(state_path)


def _save_state(repo_root: Path, state: dict) -> None:
    _write_yaml(repo_root / "paper/state.yaml", state)


def active_target(repo_root: Path) -> str:
    state = _load_state(repo_root)
    target = state.get("active_target")
    if not target:
        raise ValueError("paper/state.yaml is missing active_target")
    return str(target)


def set_target(repo_root: Path, target_name: str) -> dict:
    state = _load_state(repo_root)
    if target_name not in state.get("targets", {}):
        raise ValueError(f"unknown target '{target_name}'")
    state["active_target"] = target_name
    _save_state(repo_root, state)
    return state["targets"][target_name]


def create_journal_version(repo_root: Path, *, venue_key: str, activate: bool = False) -> str:
    config = _load_config(repo_root)
    metadata = _target_metadata(config, venue_key, target_name="journal")
    if metadata["audience"] == "ml":
        raise ValueError("journal target must use a non-ML venue")
    paper_root = repo_root / "paper"
    (paper_root / "journal/sections").mkdir(parents=True, exist_ok=True)
    (paper_root / "journal/figures").mkdir(parents=True, exist_ok=True)
    state = _load_state(repo_root) if (paper_root / "state.yaml").exists() else {"targets": {}, "initialized": True}
    state.setdefault("targets", {})
    state["targets"]["journal"] = {
        "stage": state.get("targets", {}).get("journal", {}).get("stage", "init"),
        "created": state.get("targets", {}).get("journal", {}).get("created", _today()),
        "venue": venue_key,
    }
    if activate or "active_target" not in state:
        state["active_target"] = "journal"
    _save_state(repo_root, state)
    _write_yaml(paper_root / "journal/target.yaml", metadata)
    return "journal"


# -- Session log --------------------------------------------------------------

_SESSION_LOG_HEADER = "# Session Decisions Log\n"


def _session_log_path(repo_root: Path) -> Path:
    return repo_root / "paper/shared/session-log.md"


def _read_session_log(repo_root: Path) -> str:
    path = _session_log_path(repo_root)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def log_decision(repo_root: Path, text: str) -> Path:
    path = _session_log_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(_SESSION_LOG_HEADER, encoding="utf-8")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"- [{stamp}] {text}\n")
    return path


def clear_session(repo_root: Path) -> Path:
    path = _session_log_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_SESSION_LOG_HEADER, encoding="utf-8")
    return path


# -- Brief generation ---------------------------------------------------------


def _resolve_section_file(repo_root: Path, target: str, hint: str) -> Path | None:
    """Resolve a section hint to a .tex file path, or None if not found."""
    sections_dir = repo_root / f"paper/{target}/sections"
    if not sections_dir.exists():
        return None
    hint = hint.strip()
    # Try as-is
    candidate = sections_dir / hint
    if candidate.exists():
        return candidate
    # Try with .tex suffix
    if not hint.endswith(".tex"):
        candidate = sections_dir / f"{hint}.tex"
        if candidate.exists():
            return candidate
    # Try slugified
    slugified = _slugify(hint)
    candidate = sections_dir / f"{slugified}.tex"
    if candidate.exists():
        return candidate
    return None


def write_workflow_brief(
    repo_root: Path,
    workflow_slug: str,
    *,
    guidance: str = "",
    target_name: str | None = None,
    section: str | None = None,
    lines: str | None = None,
) -> Path:
    workflows = workflow_map()
    if workflow_slug not in workflows:
        available = ", ".join(sorted(workflows))
        raise ValueError(f"unknown workflow '{workflow_slug}'; available workflows: {available}")
    spec = workflows[workflow_slug]
    active = target_name
    try:
        active = active or active_target(repo_root)
    except (FileNotFoundError, ValueError):
        active = target_name or "uninitialized"
    output_root = repo_root / ".pepper/runtime-briefs"
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / f"{workflow_slug}.md"
    brief_text = textwrap.dedent(
        f"""\
        # Pepper Workflow Brief: {workflow_slug}

        - Canonical CLI: `{spec.cli_command}`
        - Active target: `{active}`

        ## Summary

        {spec.summary}

        ## Deterministic Steps

        {_format_brief_steps(spec.deterministic_steps)}

        ## Role Steps

        {_format_brief_steps(spec.role_steps)}

        ## Guidance

        {spec.instructions}
        """
    ).strip()
    # Session decisions
    session_log = _read_session_log(repo_root)
    if session_log.strip() and session_log.strip() != _SESSION_LOG_HEADER.strip():
        brief_text += f"\n\n## Session Decisions\n\n{session_log.strip()}\n"
    if guidance.strip():
        brief_text += f"\n\n## Extra Guidance\n\n{guidance.strip()}\n"
    if workflow_slug in ("draft-section", "edit-section"):
        # Sibling context
        try:
            sibling_ctx = collect_sibling_context(repo_root, target_name=active)
            brief_text += f"\n\n{sibling_ctx}"
        except (FileNotFoundError, ValueError):
            pass
        # Embed target section content
        section_hint = section or guidance.split()[0] if guidance.strip() else None
        if section_hint:
            section_path = _resolve_section_file(repo_root, active, section_hint)
            if section_path and section_path.exists():
                content = section_path.read_text(encoding="utf-8")
                rel = section_path.relative_to(repo_root).as_posix()
                brief_text += f"\n\n## Current Section Content\n\n"
                brief_text += f"**File:** `{rel}`\n\n"
                if lines:
                    # Embed full content and highlight focus range
                    all_lines = content.splitlines()
                    brief_text += f"```latex\n{content}\n```\n"
                    parts = lines.split("-", 1)
                    try:
                        start = int(parts[0]) - 1
                        end = int(parts[1]) if len(parts) > 1 else start + 1
                    except ValueError:
                        start, end = 0, len(all_lines)
                    start = max(0, start)
                    end = max(start, end)
                    focus = "\n".join(
                        f"{i + 1:4d}  {line}"
                        for i, line in enumerate(all_lines[start:end], start=start)
                    )
                    brief_text += f"\n### Edit Focus (lines {lines})\n\n```latex\n{focus}\n```\n"
                else:
                    brief_text += f"```latex\n{content}\n```\n"
    output_path.write_text(brief_text + "\n", encoding="utf-8")
    return output_path


def _extract_tex_metadata(tex_path: Path) -> dict:
    """Extract labels and section titles from a .tex file."""
    content = tex_path.read_text(encoding="utf-8")
    return {
        "labels": _LABEL_RE.findall(content),
        "sections": _SECTION_RE.findall(content),
    }


def sync_context(repo_root: Path, *, target_name: str | None = None) -> Path:
    """Scan .tex files and update context.md with the actual paper structure."""
    target = target_name or active_target(repo_root)
    sections_dir = repo_root / f"paper/{target}/sections"
    if not sections_dir.exists():
        raise FileNotFoundError(f"no sections directory at {sections_dir}")

    structure_lines: list[str] = []
    for tex_file in sorted(sections_dir.glob("*.tex")):
        meta = _extract_tex_metadata(tex_file)
        title = meta["sections"][0] if meta["sections"] else tex_file.stem.replace("_", " ").title()
        label_info = ", ".join(meta["labels"]) if meta["labels"] else "no labels"
        structure_lines.append(f"- `{tex_file.name}`: {title} [{label_info}]")

    context_path = repo_root / "paper/shared/context.md"
    content = context_path.read_text(encoding="utf-8")

    structure_block = "## Current Structure\n\n" + "\n".join(structure_lines)
    if "## Current Structure" in content:
        content = re.sub(
            r"## Current Structure\n.*?(?=\n## |\Z)",
            structure_block + "\n",
            content,
            flags=re.DOTALL,
        )
    else:
        content = content.rstrip() + "\n\n" + structure_block + "\n"

    context_path.write_text(content, encoding="utf-8")
    return context_path


def collect_sibling_context(repo_root: Path, *, target_name: str | None = None) -> str:
    """Collect labels from all sibling .tex files for cross-reference context."""
    target = target_name or active_target(repo_root)
    sections_dir = repo_root / f"paper/{target}/sections"
    if not sections_dir.exists():
        return "No sibling sections found.\n"

    lines = ["## Sibling Section Context\n"]
    for tex_file in sorted(sections_dir.glob("*.tex")):
        meta = _extract_tex_metadata(tex_file)
        title = meta["sections"][0] if meta["sections"] else tex_file.stem.replace("_", " ").title()
        label_list = ", ".join(f"`{lbl}`" for lbl in meta["labels"]) if meta["labels"] else "no labels"
        lines.append(f"- **{tex_file.name}** ({title}): {label_list}")

    return "\n".join(lines) + "\n"


def _format_brief_steps(items: tuple[str, ...]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)
