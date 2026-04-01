from __future__ import annotations

import re
import shutil
import subprocess
import textwrap
import zipfile
from datetime import date
from pathlib import Path

import yaml

from .core_specs import workflow_map

EXCLUDED_SCAN_DIRS = {".git", ".claude", ".pepper", "paper", "node_modules", ".venv", "dist", "__pycache__"}
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


def _resolve_main_tex(source: Path) -> Path:
    if source.is_file():
        return source
    candidates = sorted(source.rglob("*.tex"))
    for candidate in candidates:
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        if "\\documentclass" in text and "\\begin{document}" in text:
            return candidate
    if candidates:
        return candidates[0]
    raise FileNotFoundError(f"no .tex files found under {source}")


def _discover_inputs(tex_text: str) -> list[str]:
    matches = re.findall(r"\\(?:input|include)\{([^}]+)\}", tex_text)
    return [match.strip() for match in matches]


def _resolve_include(base_dir: Path, value: str, extensions: tuple[str, ...]) -> Path | None:
    candidate = (base_dir / value).resolve()
    if candidate.exists():
        return candidate
    for extension in extensions:
        with_extension = candidate.with_suffix(extension)
        if with_extension.exists():
            return with_extension
    return None


def _extract_abstract(tex_text: str) -> str | None:
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex_text, re.DOTALL)
    if not match:
        return None
    return match.group(1).strip() + "\n"


def _split_monolithic_sections(tex_text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"\\section\{([^}]+)\}", tex_text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tex_text)
        title = match.group(1).strip()
        body = tex_text[start:end].strip()
        sections.append((title, body + "\n"))
    return sections


def _section_filename(title: str, audience: str) -> str:
    lowered = title.lower()
    mapping = {
        "abstract": "abstract.tex",
        "introduction": "introduction.tex",
        "related work": "related_work.tex",
        "literature review": "related_work.tex",
        "background": "background.tex",
        "preliminaries": "background.tex",
        "method": "methodology.tex",
        "methodology": "methodology.tex",
        "model": "methodology.tex",
        "theory": "theory.tex",
        "experiment": "experiments.tex",
        "results": "experiments.tex" if audience == "ml" else "empirics.tex",
        "empirics": "empirics.tex",
        "conclusion": "conclusion.tex",
        "discussion": "conclusion.tex",
        "appendix": "appendix_proofs.tex",
        "proof": "appendix_proofs.tex",
    }
    for needle, filename in mapping.items():
        if needle in lowered:
            return filename
    return f"{_slugify(title)}.tex"


def import_paper(
    repo_root: Path,
    *,
    source: Path,
    title: str,
    topic: str,
    contributions: list[str],
    venue_key: str,
    paper_type: str,
    import_mode: str = "review",
) -> str:
    main_tex = _resolve_main_tex(source.resolve())
    config = _load_config(repo_root)
    target = _target_metadata(config, venue_key)
    stage = "outlining" if import_mode == "revise" else "drafting"
    target_name = initialize_workspace(
        repo_root,
        title=title,
        topic=topic,
        contributions=contributions,
        venue_key=venue_key,
        paper_type=paper_type,
        source_map=scan_source_map(repo_root),
        stage=stage,
        imported_from=str(main_tex),
        import_mode=import_mode,
        target_name=target["name"],
    )
    target_root = repo_root / "paper" / target_name
    sections_root = target_root / "sections"
    source_root = main_tex.parent
    tex_text = main_tex.read_text(encoding="utf-8", errors="ignore")

    abstract_text = _extract_abstract(tex_text)
    if abstract_text:
        (sections_root / "abstract.tex").write_text(abstract_text, encoding="utf-8")

    include_paths = [_resolve_include(source_root, item, (".tex",)) for item in _discover_inputs(tex_text)]
    include_tex = [path for path in include_paths if path is not None]
    if include_tex:
        for tex_file in include_tex:
            destination = sections_root / tex_file.name
            shutil.copy2(tex_file, destination)
    else:
        seen: set[str] = set()
        for title_text, body in _split_monolithic_sections(tex_text):
            filename = _section_filename(title_text, str(target["audience"]))
            if filename in seen:
                stem = Path(filename).stem
                filename = f"{stem}_{len(seen) + 1}.tex"
            seen.add(filename)
            (sections_root / filename).write_text(body, encoding="utf-8")

    bib_contents: list[str] = []
    for bib_file in sorted(source_root.rglob("*.bib")):
        bib_contents.append(bib_file.read_text(encoding="utf-8", errors="ignore").strip())
    merged_bib = "\n\n".join(part for part in bib_contents if part) + ("\n" if bib_contents else "")
    (repo_root / "paper/shared/references-master.bib").write_text(merged_bib, encoding="utf-8")
    (target_root / "references.bib").write_text(merged_bib, encoding="utf-8")

    figure_root = target_root / "figures"
    figure_root.mkdir(parents=True, exist_ok=True)
    figure_matches = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex_text)
    for raw_value in figure_matches:
        resolved = _resolve_include(source_root, raw_value, GRAPHIC_EXTENSIONS)
        if resolved is not None:
            shutil.copy2(resolved, figure_root / resolved.name)

    shutil.copy2(main_tex, target_root / "main.tex")
    return target_name


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


def _title_from_context(context_path: Path) -> str:
    if not context_path.exists():
        return "Untitled Paper"
    text = context_path.read_text(encoding="utf-8")
    match = re.search(r"## Title\s+(.+)", text)
    return match.group(1).strip() if match else "Untitled Paper"


def _outline_filename_map(outline_path: Path) -> dict[str, str]:
    if not outline_path.exists():
        return {}
    mapping: dict[str, str] = {}
    text = outline_path.read_text(encoding="utf-8")
    for match in re.finditer(r"###\s+.+?([A-Za-z /-]+)\s+\(filename:\s*([^)]+\.tex)\)", text):
        heading = match.group(1).strip().lower()
        filename = match.group(2).strip()
        mapping[heading] = filename
    return mapping


def _ordered_section_inputs(target_root: Path, audience: str) -> list[str]:
    sections_root = target_root / "sections"
    outline_map = _outline_filename_map(target_root / "outline.md")
    ordered: list[str] = []
    custom_candidates = {
        "abstract": outline_map.get("abstract"),
        "introduction": outline_map.get("introduction"),
        "related work": outline_map.get("related work") or outline_map.get("literature review"),
        "background": outline_map.get("background") or outline_map.get("model setup"),
        "methodology": outline_map.get("methodology") or outline_map.get("method"),
        "theory": outline_map.get("theory"),
        "experiments": outline_map.get("experiments") or outline_map.get("empirics"),
        "conclusion": outline_map.get("conclusion"),
        "appendix proofs": outline_map.get("appendix proofs"),
        "appendix experiments": outline_map.get("appendix experiments"),
    }
    default_names = [
        custom_candidates["abstract"] or "abstract.tex",
        custom_candidates["introduction"] or "introduction.tex",
        custom_candidates["related work"] or "related_work.tex",
        custom_candidates["background"] or "background.tex",
        custom_candidates["methodology"] or "methodology.tex",
        custom_candidates["theory"] or "theory.tex",
        custom_candidates["experiments"] or ("experiments.tex" if audience == "ml" else "empirics.tex"),
        custom_candidates["conclusion"] or "conclusion.tex",
        custom_candidates["appendix proofs"] or "appendix_proofs.tex",
        custom_candidates["appendix experiments"] or "appendix_experiments.tex",
    ]
    for name in default_names:
        if (sections_root / name).exists():
            ordered.append(name)
    remaining = sorted(
        path.name for path in sections_root.glob("*.tex") if path.name not in ordered and path.name not in {"abstract.tex"}
    )
    ordered.extend(remaining)
    return ordered


def assemble_paper(repo_root: Path, *, compile_pdf: bool = False, target_name: str | None = None) -> Path:
    target = target_name or active_target(repo_root)
    target_root = repo_root / "paper" / target
    target_data = _load_yaml(target_root / "target.yaml")
    title = _title_from_context(repo_root / "paper/shared/context.md")
    audience = str(target_data.get("audience", "ml"))
    ordered_sections = _ordered_section_inputs(target_root, audience)
    section_inputs: list[str] = []
    appendix_inputs: list[str] = []
    for filename in ordered_sections:
        line = f"\\input{{sections/{Path(filename).stem}}}"
        if filename.startswith("appendix_"):
            appendix_inputs.append(line)
        elif filename != "abstract.tex":
            section_inputs.append(line)

    abstract_block = "\\input{sections/abstract}\n" if (target_root / "sections/abstract.tex").exists() else "% Abstract pending\n"
    bibliography_style = target_data.get("bibstyle") or "plainnat"
    template_name = target_data.get("template", "custom")
    main_tex = textwrap.dedent(
        f"""\
        % Generated by Pepper's deterministic assembler.
        % Target template: {template_name}
        % Copy venue style files into `.pepper/templates/{template_name}/` before final compilation.
        \\documentclass{{article}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[T1]{{fontenc}}
        \\usepackage{{amsmath,amssymb,amsthm}}
        \\usepackage{{graphicx}}
        \\usepackage{{booktabs}}
        \\usepackage{{threeparttable}}
        \\usepackage{{natbib}}
        \\usepackage{{hyperref}}
        \\title{{{title}}}
        \\author{{Anonymous Author(s)}}
        \\date{{}}
        \\begin{{document}}
        \\maketitle
        \\begin{{abstract}}
        {abstract_block.rstrip()}
        \\end{{abstract}}
        {chr(10).join(section_inputs)}
        \\bibliographystyle{{{bibliography_style}}}
        \\bibliography{{references}}
        """
    )
    if appendix_inputs:
        main_tex += "\n\\appendix\n" + "\n".join(appendix_inputs) + "\n"
    main_tex += "\\end{document}\n"
    main_path = target_root / "main.tex"
    main_path.write_text(main_tex, encoding="utf-8")

    state = _load_state(repo_root)
    state.setdefault("targets", {}).setdefault(target, {})["stage"] = "drafting"
    _save_state(repo_root, state)

    if compile_pdf:
        _run_latex_sequence(target_root)
    return main_path


def _copy_tree_contents(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def _run_latex_sequence(target_root: Path) -> None:
    commands = (
        ["pdflatex", "main.tex"],
        ["bibtex", "main"],
        ["pdflatex", "main.tex"],
        ["pdflatex", "main.tex"],
    )
    for command in commands:
        subprocess.run(command, cwd=target_root, check=True, capture_output=True, text=True)


def camera_ready(repo_root: Path, *, compile_pdf: bool = False, target_name: str | None = None) -> Path:
    target = target_name or active_target(repo_root)
    target_root = repo_root / "paper" / target
    if not (target_root / "main.tex").exists():
        assemble_paper(repo_root, compile_pdf=False, target_name=target)
    camera_root = target_root / "camera-ready"
    camera_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target_root / "main.tex", camera_root / "main.tex")
    if (target_root / "references.bib").exists():
        shutil.copy2(target_root / "references.bib", camera_root / "references.bib")
    _copy_tree_contents(target_root / "figures", camera_root / "figures")

    target_data = _load_yaml(target_root / "target.yaml")
    template_name = str(target_data.get("template", ""))
    if template_name:
        _copy_tree_contents(repo_root / f".pepper/templates/{template_name}", camera_root)

    verification = textwrap.dedent(
        f"""\
        # Camera-Ready Verification

        - Target: `{target}`
        - Venue: `{target_data.get('venue', 'unknown')}`
        - Generated: `{_today()}`
        - Main manuscript: `main.tex`
        - Bibliography copied: `{'yes' if (camera_root / 'references.bib').exists() else 'no'}`
        """
    )
    (camera_root / "VERIFICATION.md").write_text(verification, encoding="utf-8")
    submission_notes = textwrap.dedent(
        """\
        # Submission Notes

        Review the generated package, confirm that official venue style files are present,
        and resolve any remaining placeholders before submission.
        """
    )
    (camera_root / "SUBMISSION_NOTES.md").write_text(submission_notes, encoding="utf-8")

    if compile_pdf:
        _run_latex_sequence(camera_root)

    zip_path = target_root / "submission.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(camera_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(camera_root))

    state = _load_state(repo_root)
    state.setdefault("targets", {}).setdefault(target, {})["stage"] = "camera-ready"
    _save_state(repo_root, state)
    return zip_path


def write_workflow_brief(
    repo_root: Path,
    workflow_slug: str,
    *,
    guidance: str = "",
    target_name: str | None = None,
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
    if guidance.strip():
        brief_text += f"\n\n## Extra Guidance\n\n{guidance.strip()}\n"
    output_path.write_text(brief_text + "\n", encoding="utf-8")
    return output_path


def _format_brief_steps(items: tuple[str, ...]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)
