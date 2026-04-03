from __future__ import annotations

import json
from collections import defaultdict

from .core_specs import (
    CORE_REFERENCE_FILES,
    ROLE_SPECS,
    SYSTEM_OVERVIEW,
    WORKFLOW_SPECS,
    RoleSpec,
    WorkflowSpec,
    resolve_role_instructions,
    resolve_workflow_instructions,
)

SUPPORTED_ADAPTERS = ("claude", "codex")
DEFAULT_ADAPTERS = SUPPORTED_ADAPTERS
CORE_SCOPE = "_core"

_CAPABILITY_TOOL_MAP = {
    "read_files": ("Read",),
    "write_files": ("Write",),
    "search_web": ("WebSearch", "WebFetch"),
    "search_text": ("Grep",),
    "run_shell": ("Bash",),
}


def normalize_adapters(adapters: str | list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if adapters is None:
        return DEFAULT_ADAPTERS
    if isinstance(adapters, str):
        raw = [part.strip() for part in adapters.split(",")]
    else:
        raw = [str(part).strip() for part in adapters]
    normalized = tuple(dict.fromkeys(part for part in raw if part))
    invalid = sorted(set(normalized) - set(SUPPORTED_ADAPTERS))
    if invalid:
        supported = ", ".join(SUPPORTED_ADAPTERS)
        invalid_text = ", ".join(invalid)
        raise ValueError(f"unsupported adapters: {invalid_text}; supported adapters: {supported}")
    return normalized or DEFAULT_ADAPTERS


def _claude_tools_for_role(spec: RoleSpec) -> tuple[str, ...]:
    tools: list[str] = []
    for capability in spec.capabilities:
        tools.extend(_CAPABILITY_TOOL_MAP.get(capability, ()))
    return tuple(dict.fromkeys(tools))


def _format_role_outputs(spec: RoleSpec) -> str:
    return "\n".join(f"- `{output}`" for output in spec.outputs)


def _format_capabilities(spec: RoleSpec) -> str:
    return "\n".join(f"- `{capability}`" for capability in spec.capabilities)


def render_claude_role(spec: RoleSpec) -> str:
    tools = ", ".join(_claude_tools_for_role(spec))
    return f"""---
name: {spec.slug}
description: >
  {spec.summary}
tools: {tools}
---

You are the `{spec.slug}` role in the Pepper academic paper writing system.

{resolve_role_instructions(spec)}

## Expected Outputs

{_format_role_outputs(spec)}

## Neutral Capability Contract

{_format_capabilities(spec)}

## Shared References

Follow:
- `.pepper/shared-agent-protocols.md`
- `.pepper/writing-style.md`
"""


def render_codex_role(spec: RoleSpec) -> str:
    return f"""# {spec.slug}

{spec.summary}

## Expected Outputs

{_format_role_outputs(spec)}

## Capability Contract

{_format_capabilities(spec)}

## Instructions

{resolve_role_instructions(spec)}

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.
"""


def _format_workflow_steps(items: tuple[str, ...]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


_BRIEF_FIRST_WORKFLOWS = frozenset({"draft-section", "edit-section", "polish", "revise-paper"})


def render_claude_workflow(spec: WorkflowSpec) -> str:
    if spec.slug in _BRIEF_FIRST_WORKFLOWS:
        return f"""# /{spec.slug}

Canonical entrypoint: `{spec.cli_command}`

## What This Does

{spec.summary}

## How to Execute

1. Run: `pepper workflow-brief {spec.slug} --guidance "$ARGUMENTS"` to generate a self-contained brief.
2. Read the generated brief at `.pepper/runtime-briefs/{spec.slug}.md`.
3. Follow the brief's instructions using the embedded section content and session decisions as context.

The brief includes current file content, sibling section labels, and session decisions automatically.
Use `$ARGUMENTS` to pass freeform user guidance (e.g., section name, edit instructions).

## Deterministic Steps

{_format_workflow_steps(spec.deterministic_steps)}

## Role Steps

{_format_workflow_steps(spec.role_steps)}

## Implementation Guidance

{resolve_workflow_instructions(spec)}
"""
    return f"""# /{spec.slug}

Canonical entrypoint: `{spec.cli_command}`

## What This Does

{spec.summary}

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

{_format_workflow_steps(spec.deterministic_steps)}

## Role Steps

{_format_workflow_steps(spec.role_steps)}

## Implementation Guidance

{resolve_workflow_instructions(spec)}
"""


def render_codex_workflow(spec: WorkflowSpec) -> str:
    return f"""# {spec.slug}

Canonical entrypoint: `{spec.cli_command}`

## Summary

{spec.summary}

## Deterministic Steps

{_format_workflow_steps(spec.deterministic_steps)}

## Role Steps

{_format_workflow_steps(spec.role_steps)}

## Guidance

{resolve_workflow_instructions(spec)}

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.
"""


def render_claude_settings() -> str:
    payload = {
        "permissions": {
            "allow": [
                "Bash(pdflatex:*)",
                "Bash(bibtex:*)",
                "Bash(xelatex:*)",
                "Bash(lualatex:*)",
                "Bash(grep:*)",
                "Bash(find:*)",
                "Bash(zip:*)",
                "Bash(cp:*)",
                "Bash(mkdir:*)",
                "Bash(cat:*)",
                "Bash(mv:*)",
                "Bash(rm:*)",
                "Bash(ls:*)",
                "Bash(pepper:*)",
                "WebSearch(*)",
                "WebFetch(*)",
            ],
            "deny": [],
        },
        "env": {
            "PAPER_SYSTEM_VERSION": "3.0",
            "PEPPER_CANONICAL_INTERFACE": "pepper-cli",
        },
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def render_claude_system_prompt() -> str:
    references = "\n".join(f"- `{path}`" for path in CORE_REFERENCE_FILES)
    return f"""{SYSTEM_OVERVIEW}

## Runtime Adapter

This file is the Claude Code adapter. The canonical workflow contract still lives in the
Pepper core spec and the `pepper` CLI.

Use repo-local slash commands as convenience wrappers around the canonical CLI workflows.
When a workflow requires deterministic repository changes, prefer the CLI over ad hoc manual edits.

## Key References

{references}
"""


def render_codex_system_prompt() -> str:
    workflow_links = "\n".join(
        f"- [{spec.slug}](./.pepper/adapters/codex/workflows/{spec.slug}.md)"
        for spec in WORKFLOW_SPECS
    )
    role_links = "\n".join(
        f"- [{spec.slug}](./.pepper/adapters/codex/roles/{spec.slug}.md)"
        for spec in ROLE_SPECS
    )
    return f"""{SYSTEM_OVERVIEW}

## Runtime Adapter

This file is the Codex adapter. Treat the `pepper` CLI as the canonical interface for
deterministic repo work. Use the role documents only for judgment-heavy writing and review tasks.

## Workflow Guides

{workflow_links}

## Role Guides

{role_links}
"""


def rendered_adapter_assets(adapters: tuple[str, ...]) -> dict[str, bytes]:
    assets: dict[str, bytes] = {}
    if "claude" in adapters:
        assets[".claude/settings.json"] = render_claude_settings().encode("utf-8")
        for spec in ROLE_SPECS:
            assets[f".claude/agents/{spec.slug}.md"] = render_claude_role(spec).encode("utf-8")
        for spec in WORKFLOW_SPECS:
            assets[f".claude/commands/{spec.slug}.md"] = render_claude_workflow(spec).encode("utf-8")
    if "codex" in adapters:
        for spec in ROLE_SPECS:
            assets[f".pepper/adapters/codex/roles/{spec.slug}.md"] = render_codex_role(spec).encode("utf-8")
        for spec in WORKFLOW_SPECS:
            assets[f".pepper/adapters/codex/workflows/{spec.slug}.md"] = render_codex_workflow(spec).encode("utf-8")
    return assets


def rendered_marker_files(adapters: tuple[str, ...]) -> dict[str, str]:
    files: dict[str, str] = {}
    if "claude" in adapters:
        files["CLAUDE.md"] = render_claude_system_prompt()
    if "codex" in adapters:
        files["AGENTS.md"] = render_codex_system_prompt()
    return files


def managed_files_by_scope(adapters: tuple[str, ...], asset_paths: list[str]) -> dict[str, list[str]]:
    scoped: dict[str, list[str]] = defaultdict(list)
    for path in asset_paths:
        if path.startswith(".claude/"):
            scoped["claude"].append(path)
        elif path.startswith(".pepper/adapters/codex/"):
            scoped["codex"].append(path)
        else:
            scoped[CORE_SCOPE].append(path)
    for adapter in adapters:
        scoped.setdefault(adapter, [])
    scoped.setdefault(CORE_SCOPE, [])
    return {scope: sorted(paths) for scope, paths in scoped.items()}
