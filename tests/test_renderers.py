from __future__ import annotations

import json
import re

import pytest
import yaml

from pepper.core_specs import ROLE_SPECS, WORKFLOW_SPECS
from pepper.renderers import (
    _CAPABILITY_TOOL_MAP,
    _claude_tools_for_role,
    normalize_adapters,
    render_claude_role,
    render_claude_settings,
    render_claude_workflow,
    render_codex_role,
    render_codex_workflow,
    rendered_adapter_assets,
    rendered_marker_files,
)


# -- normalize_adapters -------------------------------------------------------


def test_normalize_adapters_defaults() -> None:
    assert normalize_adapters(None) == ("claude", "codex")


def test_normalize_adapters_single_string() -> None:
    assert normalize_adapters("claude") == ("claude",)


def test_normalize_adapters_csv_string() -> None:
    assert normalize_adapters("codex,claude") == ("codex", "claude")


def test_normalize_adapters_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unsupported adapters"):
        normalize_adapters("bogus")


def test_normalize_adapters_deduplicates() -> None:
    assert normalize_adapters("claude,claude") == ("claude",)


# -- render_claude_role --------------------------------------------------------


@pytest.mark.parametrize("spec", ROLE_SPECS, ids=lambda s: s.slug)
def test_render_claude_role_has_valid_yaml_frontmatter(spec):
    rendered = render_claude_role(spec)
    assert rendered.startswith("---\n")
    parts = rendered.split("---", 2)
    # parts[0] is empty string before first ---, parts[1] is frontmatter
    fm = yaml.safe_load(parts[1])
    assert fm["name"] == spec.slug
    assert "description" in fm
    assert "tools" in fm


@pytest.mark.parametrize("spec", ROLE_SPECS, ids=lambda s: s.slug)
def test_render_claude_role_tools_match_capabilities(spec):
    rendered = render_claude_role(spec)
    parts = rendered.split("---", 2)
    fm = yaml.safe_load(parts[1])
    expected_tools = _claude_tools_for_role(spec)
    # The YAML tools field is a comma-separated string
    actual_tools = tuple(t.strip() for t in fm["tools"].split(","))
    assert actual_tools == expected_tools


@pytest.mark.parametrize("spec", ROLE_SPECS, ids=lambda s: s.slug)
def test_render_claude_role_references_shared_protocols(spec):
    rendered = render_claude_role(spec)
    assert ".pepper/shared-agent-protocols.md" in rendered
    assert ".pepper/writing-style.md" in rendered


# -- render_codex_role ---------------------------------------------------------


@pytest.mark.parametrize("spec", ROLE_SPECS, ids=lambda s: s.slug)
def test_render_codex_role_structure(spec):
    rendered = render_codex_role(spec)
    assert rendered.startswith(f"# {spec.slug}\n")
    assert "## Expected Outputs" in rendered
    assert "## Capability Contract" in rendered
    assert "## Instructions" in rendered


# -- render_claude_workflow ----------------------------------------------------


@pytest.mark.parametrize("spec", WORKFLOW_SPECS, ids=lambda s: s.slug)
def test_render_claude_workflow_structure(spec):
    rendered = render_claude_workflow(spec)
    assert rendered.startswith(f"# /{spec.slug}\n")
    assert "## What This Does" in rendered
    assert "## Deterministic Steps" in rendered
    assert "## Role Steps" in rendered
    assert "## Implementation Guidance" in rendered
    assert "$ARGUMENTS" in rendered


# -- render_codex_workflow -----------------------------------------------------


@pytest.mark.parametrize("spec", WORKFLOW_SPECS, ids=lambda s: s.slug)
def test_render_codex_workflow_structure(spec):
    rendered = render_codex_workflow(spec)
    assert rendered.startswith(f"# {spec.slug}\n")
    assert "## Summary" in rendered
    assert "## Deterministic Steps" in rendered
    assert "## Role Steps" in rendered
    assert "## Guidance" in rendered


# -- render_claude_settings ----------------------------------------------------


def test_render_claude_settings_is_valid_json() -> None:
    text = render_claude_settings()
    payload = json.loads(text)
    assert isinstance(payload["permissions"]["allow"], list)
    assert len(payload["permissions"]["allow"]) > 0
    assert "env" in payload


# -- rendered_adapter_assets ---------------------------------------------------


def test_rendered_adapter_assets_claude_only() -> None:
    assets = rendered_adapter_assets(("claude",))
    assert ".claude/settings.json" in assets
    assert all(k.startswith(".claude/") for k in assets)


def test_rendered_adapter_assets_codex_only() -> None:
    assets = rendered_adapter_assets(("codex",))
    assert all(k.startswith(".pepper/adapters/codex/") for k in assets)


def test_rendered_adapter_assets_both_adapters() -> None:
    assets = rendered_adapter_assets(("claude", "codex"))
    claude_keys = [k for k in assets if k.startswith(".claude/")]
    codex_keys = [k for k in assets if k.startswith(".pepper/adapters/codex/")]
    assert len(claude_keys) > 0
    assert len(codex_keys) > 0
    # Should have one agent + one command per role/workflow, plus settings
    expected_claude = 1 + len(ROLE_SPECS) + len(WORKFLOW_SPECS)
    assert len(claude_keys) == expected_claude


def test_rendered_adapter_assets_path_patterns() -> None:
    assets = rendered_adapter_assets(("claude", "codex"))
    for key in assets:
        assert re.match(
            r"^\.claude/(agents|commands)/[a-z][a-z0-9-]+\.md$"
            r"|^\.claude/settings\.json$"
            r"|^\.pepper/adapters/codex/(roles|workflows)/[a-z][a-z0-9-]+\.md$",
            key,
        ), f"unexpected asset path: {key!r}"


# -- rendered_marker_files -----------------------------------------------------


def test_rendered_marker_files_both() -> None:
    markers = rendered_marker_files(("claude", "codex"))
    assert set(markers.keys()) == {"CLAUDE.md", "AGENTS.md"}


def test_rendered_marker_files_claude_only() -> None:
    markers = rendered_marker_files(("claude",))
    assert set(markers.keys()) == {"CLAUDE.md"}


def test_rendered_marker_files_codex_only() -> None:
    markers = rendered_marker_files(("codex",))
    assert set(markers.keys()) == {"AGENTS.md"}
