from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


CORE_REFERENCE_FILES = (
    ".pepper/config.yaml",
    ".pepper/shared-agent-protocols.md",
    ".pepper/writing-style.md",
    "paper/state.yaml",
    "paper/shared/context.md",
    "paper/shared/session-log.md",
    "paper/<active_target>/target.yaml",
)

SYSTEM_OVERVIEW = """# Academic Paper Writing System

Pepper is a project-local academic paper writing framework for machine learning,
economics, marketing, operations research, and quant finance.

The canonical interface is the `pepper` CLI. Runtime adapters such as Claude Code
and Codex consume the same workflow and role definitions rendered into their
preferred local files.

## Canonical Workflows

- `pepper new-paper`
- `pepper import-paper`
- `pepper literature-search`
- `pepper draft-paper`
- `pepper draft-section`
- `pepper edit-section`
- `pepper review-paper`
- `pepper revise-paper`
- `pepper set-target`
- `pepper create-journal-version`
- `pepper assemble`
- `pepper polish`
- `pepper camera-ready`

## Context Resolution

All workflows and roles resolve context through:

1. `paper/state.yaml` for the active target and stage
2. `paper/shared/context.md` for title, topic, contributions, and source map
3. `paper/<active_target>/target.yaml` for venue metadata
4. Repo-local source paths from the source map

Deterministic repo operations belong in the CLI. Role-driven work is reserved for
literature synthesis, outlining, drafting, review, and revision planning.
"""


@dataclass(frozen=True, slots=True)
class RoleSpec:
    slug: str
    summary: str
    capabilities: tuple[str, ...]
    outputs: tuple[str, ...]
    instructions: str


@dataclass(frozen=True, slots=True)
class WorkflowSpec:
    slug: str
    summary: str
    cli_command: str
    deterministic_steps: tuple[str, ...]
    role_steps: tuple[str, ...]
    instructions: str


ROLE_SPECS: tuple[RoleSpec, ...] = (
    RoleSpec(
        slug="literature-reviewer",
        summary="Search, verify, and synthesize related academic literature.",
        capabilities=("read_files", "write_files", "search_web"),
        outputs=(
            "paper/shared/literature/<topic>-survey.md",
            "paper/shared/references-master.bib",
        ),
        instructions="""Read the shared context, venue metadata, and existing literature files.
Search systematically across relevant academic sources. Only include verifiable papers.
Produce concise synthesis, identify gaps, and append clean BibTeX entries to the shared
bibliography without inventing citations.""",
    ),
    RoleSpec(
        slug="paper-outliner",
        summary="Create or reconstruct the paper's narrative structure and section plan.",
        capabilities=("read_files", "write_files"),
        outputs=("paper/<active_target>/outline.md",),
        instructions="""Use the shared context, literature surveys, and venue conventions to
produce a section plan, narrative arc, contribution framing, notation table, and figure/table
plan. If section files already exist, switch into retrospective mode and document the current
structure accurately before proposing changes.""",
    ),
    RoleSpec(
        slug="intro-writer",
        summary="Write and revise the abstract and introduction.",
        capabilities=("read_files", "write_files"),
        outputs=(
            "paper/<active_target>/sections/abstract.tex",
            "paper/<active_target>/sections/introduction.tex",
        ),
        instructions="""Follow the shared writing guide, the outline, and the literature survey.
Keep the abstract concise and citation-free. Make the introduction motivate the problem, explain
the gap, and state concrete contributions without revealing unverified results.""",
    ),
    RoleSpec(
        slug="technical-writer",
        summary="Write technical, theoretical, methodological, and conclusion sections.",
        capabilities=("read_files", "write_files"),
        outputs=(
            "paper/<active_target>/sections/related_work.tex",
            "paper/<active_target>/sections/background.tex",
            "paper/<active_target>/sections/methodology.tex",
            "paper/<active_target>/sections/theory.tex",
            "paper/<active_target>/sections/appendix_proofs.tex",
            "paper/<active_target>/sections/conclusion.tex",
        ),
        instructions="""Write rigorous technical prose with explicit notation, assumptions, and
plain-English explanations for formal results. Keep proofs and theorem references consistent with
the model assumptions and use appendix files for long derivations.""",
    ),
    RoleSpec(
        slug="empirics-writer",
        summary="Write experiments, empirics, robustness checks, and result interpretation.",
        capabilities=("read_files", "write_files"),
        outputs=(
            "paper/<active_target>/sections/experiments.tex",
            "paper/<active_target>/sections/empirics.tex",
            "paper/<active_target>/sections/appendix_experiments.tex",
        ),
        instructions="""Read result sources directly before writing. Verify every data-derived
number against source files. Use explicit warnings for any mismatch or missing evidence. Keep the
result narrative aligned with tables, figures, and the source map.""",
    ),
    RoleSpec(
        slug="citation-manager",
        summary="Audit citations and produce a clean target-local BibTeX file.",
        capabilities=("read_files", "write_files", "search_text"),
        outputs=(
            "paper/<active_target>/references.bib",
            "paper/<active_target>/citation-report.md",
        ),
        instructions="""Extract cited keys from target sections, verify them against the shared
bibliography, preserve only referenced entries, and report missing or suspicious citations without
inventing records.""",
    ),
    RoleSpec(
        slug="latex-assembler",
        summary="Assemble target sections into a compilable LaTeX manuscript.",
        capabilities=("read_files", "write_files", "run_shell"),
        outputs=("paper/<active_target>/main.tex",),
        instructions="""Use the target metadata, section files, and bibliography to produce a
coherent `main.tex`. Respect outline-defined custom filenames and keep appendix inputs explicit.
Compilation is deterministic CLI work when possible; use shell access only when requested by the
workflow.""",
    ),
    RoleSpec(
        slug="venue-formatter",
        summary="Prepare the target-specific submission package and formatting checks.",
        capabilities=("read_files", "write_files", "run_shell"),
        outputs=(
            "paper/<active_target>/camera-ready/",
            "paper/<active_target>/camera-ready/VERIFICATION.md",
        ),
        instructions="""Use the venue template manifest and target metadata to prepare the final
submission package, ensure anonymization mode is correct, and surface formatting or artifact gaps
before packaging.""",
    ),
    RoleSpec(
        slug="peer-reviewer",
        summary="Review the current draft as a rigorous conference or journal referee.",
        capabilities=("read_files", "write_files"),
        outputs=(
            "paper/<active_target>/review.md",
            "paper/<active_target>/revision-plan.md",
        ),
        instructions="""Review the assembled paper or section set against the outline and writing
rules. Produce a severity-ranked review and a concrete revision plan. Avoid empty encouragement;
prioritize correctness, novelty positioning, and evidence quality.""",
    ),
    RoleSpec(
        slug="revision-planner",
        summary="Map review feedback or updated results to concrete section-level changes.",
        capabilities=("read_files", "write_files"),
        outputs=("paper/<active_target>/revisions/round-<N>/revision-plan.md",),
        instructions="""Read the revision input, existing sections, outline, and shared claims.
Produce a per-section action map with explicit agent ownership, minimal scope, prerequisites, and
cross-section consistency notes. Every review comment must be mapped or explicitly rejected.""",
    ),
    RoleSpec(
        slug="copyeditor",
        summary="Sentence-level polish: grammar, clarity, flow, and style compliance without changing content.",
        capabilities=("read_files", "write_files"),
        outputs=("paper/<active_target>/sections/*.tex",),
        instructions="""Read each section file and apply four editing passes in order:

1. Grammar and mechanics — subject-verb agreement, tense consistency, article usage,
   punctuation (comma splices, missing hyphens), spelling, and common academic
   malapropisms.

2. Clarity — flag and fix ambiguous referents ("this", "it" without clear antecedent),
   excessive nominalization ("perform the computation of" to "compute"), and overly
   long sentences (40+ words) that should be split.

3. Flow and transitions — fix consecutive sentences that repeat the same
   subject or structure, abrupt paragraph transitions, and logical connectors that
   do not match the actual relationship ("however" with no contrast).

4. Style compliance — enforce `.pepper/writing-style.md` rules (no em-dashes,
   citation style with citet/citep, notation consistency, American/British English
   consistency, "Figure" vs "Fig." consistency).

Hard constraints:
- Do NOT restructure, reorder, or remove paragraphs.
- Do NOT change technical claims, arguments, or math.
- Do NOT touch content inside equation, align, algorithm, or other math environments;
  only edit the surrounding prose.
- Preserve all \\label{}, \\ref{}, \\cite{}, \\citet{}, and \\citep{} commands exactly.
- Add a `% POLISHED` LaTeX comment at the top of each edited section for traceability.""",
    ),
)


WORKFLOW_SPECS: tuple[WorkflowSpec, ...] = (
    WorkflowSpec(
        slug="new-paper",
        summary="Scan the repo and initialize a new paper workspace.",
        cli_command="pepper new-paper",
        deterministic_steps=(
            "scan the repository using source category patterns from `.pepper/config.yaml`",
            "create the `paper/` directory structure and state files",
            "write shared context, claims, figure plan, table plan, and bibliography stubs",
        ),
        role_steps=(),
        instructions="""Use CLI flags or upstream runtime inputs for title, topic, contributions,
venue, and paper type. The CLI owns source-map generation and state-file writes.""",
    ),
    WorkflowSpec(
        slug="import-paper",
        summary="Ingest an existing LaTeX project into the Pepper workspace.",
        cli_command="pepper import-paper",
        deterministic_steps=(
            "locate the main TeX file, bibliography files, and referenced figures",
            "create the target workspace and import notes",
            "copy or split source materials into the Pepper runtime layout",
        ),
        role_steps=("paper-outliner in retrospective mode",),
        instructions="""The CLI handles file discovery, copying, and basic structure inference.
Use the outliner only after files are imported to reconstruct the current narrative.""",
    ),
    WorkflowSpec(
        slug="literature-search",
        summary="Run structured literature search and consolidate the bibliography.",
        cli_command="pepper literature-search",
        deterministic_steps=("ensure the target workspace exists and load active target metadata",),
        role_steps=("literature-reviewer", "paper-outliner"),
        instructions="""Use one or more literature-reviewer tasks to search by topic, method,
data, and venue. Consolidate results into the shared bibliography, then update the stage to
`literature` or `outlining` depending on whether outlining is invoked.""",
    ),
    WorkflowSpec(
        slug="draft-paper",
        summary="Draft the full paper, then assemble the LaTeX manuscript.",
        cli_command="pepper draft-paper",
        deterministic_steps=("prepare target section paths and sibling context for the writers",),
        role_steps=("intro-writer", "technical-writer", "empirics-writer", "citation-manager"),
        instructions="""Use role parallelism where supported. The deterministic assembler should
be invoked after section files and bibliography are ready.""",
    ),
    WorkflowSpec(
        slug="draft-section",
        summary="Draft or revise specific sections with optional custom guidance.",
        cli_command="pepper draft-section",
        deterministic_steps=("resolve the requested section names, filenames, and write/revise mode",),
        role_steps=("intro-writer", "technical-writer", "empirics-writer"),
        instructions="""Section routing, filename overrides, and sibling-context collection are
deterministic. Role invocation is only for the actual prose generation.""",
    ),
    WorkflowSpec(
        slug="edit-section",
        summary="Apply surgical edits to specific sections without rewriting unaffected content.",
        cli_command="pepper edit-section",
        deterministic_steps=(
            "resolve the target section file and verify it exists on disk",
            "collect sibling section labels for cross-reference context",
        ),
        role_steps=("intro-writer", "technical-writer", "empirics-writer"),
        instructions="""This workflow uses the Edit Mode Protocol from shared-agent-protocols.md.
The user specifies a section file and edit instructions (e.g., line range, paragraph description,
or specific change request). The agent must read the entire file, apply ONLY the requested
changes, and leave all other content byte-identical. Never rewrite paragraphs that are not
mentioned in the edit instructions.""",
    ),
    WorkflowSpec(
        slug="review-paper",
        summary="Review the current draft and record a revision plan.",
        cli_command="pepper review-paper",
        deterministic_steps=("verify that the target manuscript exists",),
        role_steps=("peer-reviewer",),
        instructions="""After review completion, update the target stage to `review` and keep the
review output in the target directory.""",
    ),
    WorkflowSpec(
        slug="revise-paper",
        summary="Plan and apply revisions from feedback or updated results.",
        cli_command="pepper revise-paper",
        deterministic_steps=(
            "determine revision mode and round number",
            "persist revision input and backup the current sections",
        ),
        role_steps=("revision-planner", "intro-writer", "technical-writer", "empirics-writer"),
        instructions="""Use the planner to map work first. After user confirmation, invoke only
the required writers, then run deterministic assembly and bookkeeping.""",
    ),
    WorkflowSpec(
        slug="set-target",
        summary="Switch the active paper target.",
        cli_command="pepper set-target",
        deterministic_steps=("validate the target name and update `paper/state.yaml`",),
        role_steps=(),
        instructions="""This workflow is fully deterministic and should not require role help.""",
    ),
    WorkflowSpec(
        slug="create-journal-version",
        summary="Create a journal target alongside the conference target.",
        cli_command="pepper create-journal-version",
        deterministic_steps=(
            "create the journal target structure and metadata",
            "optionally activate the journal target",
        ),
        role_steps=("paper-outliner when bootstrap help is needed",),
        instructions="""The CLI owns the target creation. The outliner is only used when the user
wants a bootstrap outline derived from the conference structure.""",
    ),
    WorkflowSpec(
        slug="assemble",
        summary="Build `main.tex` and optionally compile the target paper.",
        cli_command="pepper assemble",
        deterministic_steps=(
            "read target metadata and section files",
            "write `paper/<active_target>/main.tex`",
            "optionally run LaTeX commands when requested",
        ),
        role_steps=(),
        instructions="""Assembly should be deterministic. If compilation is requested, use shell
execution but keep manuscript generation itself in the CLI.""",
    ),
    WorkflowSpec(
        slug="camera-ready",
        summary="Prepare the camera-ready package and submission archive.",
        cli_command="pepper camera-ready",
        deterministic_steps=(
            "copy the assembled manuscript, bibliography, figures, and style assets into the camera-ready directory",
            "optionally compile and then create `submission.zip`",
            "update the target stage to `camera-ready`",
        ),
        role_steps=(),
        instructions="""Formatting checks may be aided by a role runtime, but packaging, copying,
and state updates are deterministic CLI work.""",
    ),
    WorkflowSpec(
        slug="polish",
        summary="Copyedit sections for grammar, clarity, and flow without changing content.",
        cli_command="pepper polish",
        deterministic_steps=(
            "resolve target manuscript and section list",
            "back up current sections before edits",
        ),
        role_steps=("copyeditor",),
        instructions="""Back up sections before editing. Run the copyeditor on each requested
section. After all edits, do the mandatory post-writing review from writing-style.md:
re-read the full paper to verify internal consistency (notation, terminology, cross-references)
was not broken by the edits.""",
    ),
)


def role_map() -> dict[str, RoleSpec]:
    return {spec.slug: spec for spec in ROLE_SPECS}


def workflow_map() -> dict[str, WorkflowSpec]:
    return {spec.slug: spec for spec in WORKFLOW_SPECS}


# -- External instructions resolution -----------------------------------------

_INSTRUCTIONS_ROOT = Path(__file__).parent / "instructions"


def resolve_role_instructions(spec: RoleSpec) -> str:
    path = _INSTRUCTIONS_ROOT / "roles" / f"{spec.slug}.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return spec.instructions


def resolve_workflow_instructions(spec: WorkflowSpec) -> str:
    path = _INSTRUCTIONS_ROOT / "workflows" / f"{spec.slug}.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return spec.instructions
