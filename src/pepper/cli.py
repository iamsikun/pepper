from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .manifest import InstallManifest
from .assembly import assemble_paper, camera_ready
from .importer import import_paper
from .workspace import clear_session, create_journal_version, log_decision, new_paper, set_target, sync_context, write_workflow_brief
from .renderers import DEFAULT_ADAPTERS
from .sync import MANIFEST_PATH, dev_sync_root, find_repo_root, install_or_sync, package_version
from .validate import validate_repo


def _repo_root() -> Path:
    return find_repo_root(Path.cwd())


def _print_conflicts(conflicts: list[str]) -> None:
    print("conflicts detected in managed files:")
    for relative in conflicts:
        print(f"  - {relative}")


def _cmd_install(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    manifest_path = repo_root / MANIFEST_PATH
    if manifest_path.exists() and not args.force:
        print("pepper scaffold is already installed in this repo.")
        print("use 'pepper sync' to update, or 'pepper install --force' to reinstall.")
        return 1
    result = install_or_sync(repo_root, force=args.force, write_manifest=True, adapters=args.adapters)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        print("rerun with --force to overwrite managed-file conflicts")
        return 1
    print(f"installed pepper scaffold into {repo_root}")
    print(f"adapters: {args.adapters}")
    return 0


def _cmd_sync(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    manifest_path = repo_root / MANIFEST_PATH
    if not manifest_path.exists():
        print("pepper scaffold is not installed in this repo.")
        print("run 'pepper install' first.")
        return 1
    manifest = InstallManifest.load(manifest_path)
    adapters = args.adapters or (",".join(manifest.adapters) if manifest else ",".join(DEFAULT_ADAPTERS))
    result = install_or_sync(repo_root, force=args.force, write_manifest=True, adapters=adapters)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        print("rerun with --force to overwrite managed-file conflicts")
        return 1
    print(f"synchronized pepper scaffold in {repo_root}")
    print(f"adapters: {adapters}")
    return 0


def _cmd_validate(_: argparse.Namespace) -> int:
    repo_root = _repo_root()
    result = validate_repo(repo_root)
    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    if result.ok:
        print("validation passed")
        return 0
    print("validation failed")
    return 1


def _cmd_version(_: argparse.Namespace) -> int:
    repo_root = _repo_root()
    manifest = InstallManifest.load(repo_root / MANIFEST_PATH)
    current = package_version()
    print(f"package version: {current}")
    if manifest is None:
        print("installed scaffold version: not installed")
        return 0
    print(f"installed scaffold version: {manifest.package_version}")
    print(f"installed adapters: {', '.join(manifest.adapters)}")
    print(f"in sync: {'yes' if manifest.package_version == current else 'no'}")
    return 0


def _cmd_dev_sync_root(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    result = dev_sync_root(repo_root, adapters=args.adapters)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        return 1
    print(f"synchronized root scaffold mirror in {repo_root}")
    return 0


def _cmd_new_paper(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    target = new_paper(
        repo_root,
        title=args.title,
        topic=args.topic,
        contributions=args.contribution,
        venue_key=args.venue,
        paper_type=args.paper_type,
    )
    print(f"initialized paper workspace for target '{target}'")
    print("next step: `pepper literature-search` or your runtime adapter's wrapper for that workflow")
    return 0


def _cmd_import_paper(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    target = import_paper(
        repo_root,
        source=Path(args.source),
        title=args.title,
        topic=args.topic,
        contributions=args.contribution,
        venue_key=args.venue,
        paper_type=args.paper_type,
        import_mode=args.import_mode,
    )
    print(f"imported paper into target '{target}'")
    print("next step: `pepper assemble` for deterministic assembly or use the adapter workflow briefs")
    return 0


def _cmd_set_target(args: argparse.Namespace) -> int:
    metadata = set_target(_repo_root(), args.target)
    print(f"active target switched to '{args.target}' (stage: {metadata.get('stage', 'unknown')})")
    return 0


def _cmd_create_journal_version(args: argparse.Namespace) -> int:
    create_journal_version(_repo_root(), venue_key=args.venue, activate=args.activate)
    print(f"created journal target for venue '{args.venue}'")
    if args.activate:
        print("journal is now the active target")
    return 0


def _cmd_assemble(args: argparse.Namespace) -> int:
    main_path = assemble_paper(_repo_root(), compile_pdf=args.compile, target_name=args.target)
    print(f"assembled paper at {main_path}")
    return 0


def _cmd_camera_ready(args: argparse.Namespace) -> int:
    zip_path = camera_ready(_repo_root(), compile_pdf=args.compile, target_name=args.target)
    print(f"created submission archive at {zip_path}")
    return 0


def _cmd_brief(args: argparse.Namespace) -> int:
    path = write_workflow_brief(_repo_root(), args.workflow, guidance=args.guidance, target_name=args.target)
    print(f"wrote workflow brief to {path}")
    return 0


def _cmd_sync_context(args: argparse.Namespace) -> int:
    path = sync_context(_repo_root(), target_name=args.target)
    print(f"updated context at {path}")
    return 0


def _cmd_log_decision(args: argparse.Namespace) -> int:
    path = log_decision(_repo_root(), args.text)
    print(f"logged decision to {path}")
    return 0


def _cmd_clear_session(args: argparse.Namespace) -> int:
    path = clear_session(_repo_root())
    print(f"cleared session log at {path}")
    return 0


def _cmd_workflow_alias(args: argparse.Namespace) -> int:
    workflow = args.workflow_slug
    guidance = getattr(args, "guidance", "") or getattr(args, "request", "")
    section = getattr(args, "section", None)
    lines = getattr(args, "lines", None)
    path = write_workflow_brief(
        _repo_root(), workflow, guidance=guidance, target_name=args.target,
        section=section, lines=lines,
    )
    print(f"prepared workflow brief for '{workflow}' at {path}")
    return 0


def _add_common_metadata_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--title", required=True, help="Working paper title")
    parser.add_argument("--topic", required=True, help="2-3 sentence topic description")
    parser.add_argument("--contribution", action="append", required=True, help="Repeat for each contribution")
    parser.add_argument("--venue", required=True, help="Venue key from .pepper/config.yaml")
    parser.add_argument("--paper-type", required=True, help="Methodology, Theory, Empirical, or Theory+Experiments")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pepper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install the scaffold into the current repo")
    install_parser.add_argument("--force", action="store_true", help="Overwrite managed-file conflicts")
    install_parser.add_argument("--adapters", default="claude,codex", help="Comma-separated adapter list")
    install_parser.set_defaults(func=_cmd_install)

    sync_parser = subparsers.add_parser("sync", help="Sync scaffold files in the current repo")
    sync_parser.add_argument("--force", action="store_true", help="Overwrite managed-file conflicts")
    sync_parser.add_argument("--adapters", help="Comma-separated adapter list; defaults to the installed adapters")
    sync_parser.set_defaults(func=_cmd_sync)

    validate_parser = subparsers.add_parser("validate", help="Validate the scaffold and runtime state")
    validate_parser.set_defaults(func=_cmd_validate)

    version_parser = subparsers.add_parser("version", help="Show package and installed scaffold versions")
    version_parser.set_defaults(func=_cmd_version)

    dev_parser = subparsers.add_parser("dev-sync-root", help="Sync packaged assets back into this repo root")
    dev_parser.add_argument("--adapters", default="claude,codex", help="Comma-separated adapter list")
    dev_parser.set_defaults(func=_cmd_dev_sync_root)

    new_parser = subparsers.add_parser("new-paper", help="Initialize a new paper workspace")
    _add_common_metadata_arguments(new_parser)
    new_parser.set_defaults(func=_cmd_new_paper)

    import_parser = subparsers.add_parser("import-paper", help="Import an existing LaTeX project")
    import_parser.add_argument("source", help="Path to a TeX file or directory")
    import_parser.add_argument("--import-mode", default="review", choices=("review", "revise", "retarget"))
    _add_common_metadata_arguments(import_parser)
    import_parser.set_defaults(func=_cmd_import_paper)

    set_target_parser = subparsers.add_parser("set-target", help="Switch the active paper target")
    set_target_parser.add_argument("target", help="Target name such as conference or journal")
    set_target_parser.set_defaults(func=_cmd_set_target)

    journal_parser = subparsers.add_parser("create-journal-version", help="Create a journal target")
    journal_parser.add_argument("venue", help="Non-ML venue key from .pepper/config.yaml")
    journal_parser.add_argument("--activate", action="store_true", help="Activate the journal target after creation")
    journal_parser.set_defaults(func=_cmd_create_journal_version)

    assemble_parser = subparsers.add_parser("assemble", help="Assemble main.tex deterministically")
    assemble_parser.add_argument("--target", help="Override the active target")
    assemble_parser.add_argument("--compile", action="store_true", help="Run pdflatex/bibtex after writing main.tex")
    assemble_parser.set_defaults(func=_cmd_assemble)

    sync_context_parser = subparsers.add_parser("sync-context", help="Update context.md from actual .tex files")
    sync_context_parser.add_argument("--target", help="Override the active target")
    sync_context_parser.set_defaults(func=_cmd_sync_context)

    log_decision_parser = subparsers.add_parser("log-decision", help="Append an editorial decision to the session log")
    log_decision_parser.add_argument("text", help="Decision text to log")
    log_decision_parser.set_defaults(func=_cmd_log_decision)

    clear_session_parser = subparsers.add_parser("clear-session", help="Clear the session decisions log")
    clear_session_parser.set_defaults(func=_cmd_clear_session)

    camera_parser = subparsers.add_parser("camera-ready", help="Build the camera-ready package")
    camera_parser.add_argument("--target", help="Override the active target")
    camera_parser.add_argument("--compile", action="store_true", help="Compile the camera-ready directory before zipping")
    camera_parser.set_defaults(func=_cmd_camera_ready)

    literature_parser = subparsers.add_parser("literature-search", help="Prepare the literature-search workflow brief")
    literature_parser.add_argument("--guidance", default="", help="Extra search guidance")
    literature_parser.add_argument("--target", help="Override the active target")
    literature_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="literature-search")

    draft_parser = subparsers.add_parser("draft-paper", help="Prepare the draft-paper workflow brief")
    draft_parser.add_argument("--guidance", default="", help="Extra drafting guidance")
    draft_parser.add_argument("--target", help="Override the active target")
    draft_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="draft-paper")

    draft_section_parser = subparsers.add_parser("draft-section", help="Prepare the draft-section workflow brief")
    draft_section_parser.add_argument("request", help="Section request and optional guidance")
    draft_section_parser.add_argument("--section", help="Section filename (e.g., introduction.tex)")
    draft_section_parser.add_argument("--target", help="Override the active target")
    draft_section_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="draft-section")

    edit_section_parser = subparsers.add_parser("edit-section", help="Prepare the edit-section workflow brief")
    edit_section_parser.add_argument("request", help="Section file and edit instructions")
    edit_section_parser.add_argument("--section", help="Section filename (e.g., introduction.tex)")
    edit_section_parser.add_argument("--lines", help="Line range to focus on (e.g., 15-30)")
    edit_section_parser.add_argument("--target", help="Override the active target")
    edit_section_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="edit-section")

    review_parser = subparsers.add_parser("review-paper", help="Prepare the review-paper workflow brief")
    review_parser.add_argument("--guidance", default="", help="Extra review focus guidance")
    review_parser.add_argument("--target", help="Override the active target")
    review_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="review-paper")

    revise_parser = subparsers.add_parser("revise-paper", help="Prepare the revise-paper workflow brief")
    revise_parser.add_argument("--guidance", default="", help="Review feedback or results-update guidance")
    revise_parser.add_argument("--target", help="Override the active target")
    revise_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="revise-paper")

    polish_parser = subparsers.add_parser("polish", help="Prepare the polish workflow brief")
    polish_parser.add_argument("request", nargs="?", default="", help="Polish guidance or section focus")
    polish_parser.add_argument("--target", help="Override the active target")
    polish_parser.set_defaults(func=_cmd_workflow_alias, workflow_slug="polish")

    brief_parser = subparsers.add_parser("workflow-brief", help="Write a workflow brief for adapter runtimes")
    brief_parser.add_argument("workflow", help="Workflow slug such as literature-search or revise-paper")
    brief_parser.add_argument("--guidance", default="", help="Extra user guidance to include in the brief")
    brief_parser.add_argument("--target", help="Override the active target for the brief")
    brief_parser.set_defaults(func=_cmd_brief)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))
