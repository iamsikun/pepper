from __future__ import annotations

import re
from pathlib import Path

from pepper.core_specs import (
    ROLE_SPECS,
    WORKFLOW_SPECS,
    RoleSpec,
    WorkflowSpec,
    _INSTRUCTIONS_ROOT,
    resolve_role_instructions,
    resolve_workflow_instructions,
    role_map,
    workflow_map,
)
from pepper.renderers import _CAPABILITY_TOOL_MAP

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]+$")


def test_role_slugs_are_unique() -> None:
    slugs = [spec.slug for spec in ROLE_SPECS]
    assert len(slugs) == len(set(slugs))


def test_workflow_slugs_are_unique() -> None:
    slugs = [spec.slug for spec in WORKFLOW_SPECS]
    assert len(slugs) == len(set(slugs))


def test_role_slugs_are_valid() -> None:
    for spec in ROLE_SPECS:
        assert SLUG_RE.match(spec.slug), f"invalid role slug: {spec.slug!r}"


def test_workflow_slugs_are_valid() -> None:
    for spec in WORKFLOW_SPECS:
        assert SLUG_RE.match(spec.slug), f"invalid workflow slug: {spec.slug!r}"


def test_role_specs_have_required_fields() -> None:
    for spec in ROLE_SPECS:
        assert spec.slug
        assert spec.summary
        assert spec.capabilities
        assert spec.outputs
        assert spec.instructions


def test_workflow_specs_have_required_fields() -> None:
    for spec in WORKFLOW_SPECS:
        assert spec.slug
        assert spec.summary
        assert spec.cli_command
        assert spec.instructions
        assert spec.deterministic_steps or spec.role_steps, (
            f"workflow {spec.slug!r} has neither deterministic nor role steps"
        )


def test_role_map_matches_tuple() -> None:
    rmap = role_map()
    assert set(rmap.keys()) == {spec.slug for spec in ROLE_SPECS}
    for spec in ROLE_SPECS:
        assert rmap[spec.slug] is spec


def test_workflow_map_matches_tuple() -> None:
    wmap = workflow_map()
    assert set(wmap.keys()) == {spec.slug for spec in WORKFLOW_SPECS}
    for spec in WORKFLOW_SPECS:
        assert wmap[spec.slug] is spec


def test_all_role_capabilities_are_known() -> None:
    known = set(_CAPABILITY_TOOL_MAP.keys())
    for spec in ROLE_SPECS:
        for cap in spec.capabilities:
            assert cap in known, f"role {spec.slug!r} has unknown capability {cap!r}"


def test_specs_are_frozen() -> None:
    spec = ROLE_SPECS[0]
    try:
        spec.slug = "modified"  # type: ignore[misc]
        raise AssertionError("RoleSpec should be frozen")
    except AttributeError:
        pass

    wspec = WORKFLOW_SPECS[0]
    try:
        wspec.slug = "modified"  # type: ignore[misc]
        raise AssertionError("WorkflowSpec should be frozen")
    except AttributeError:
        pass


# -- Instruction resolution ---------------------------------------------------


def test_resolve_role_instructions_falls_back_to_inline() -> None:
    spec = ROLE_SPECS[0]
    assert resolve_role_instructions(spec) == spec.instructions


def test_resolve_workflow_instructions_falls_back_to_inline() -> None:
    spec = WORKFLOW_SPECS[0]
    assert resolve_workflow_instructions(spec) == spec.instructions


def test_resolve_role_instructions_prefers_external_file(tmp_path: Path) -> None:
    import pepper.core_specs as mod

    original_root = mod._INSTRUCTIONS_ROOT
    try:
        mod._INSTRUCTIONS_ROOT = tmp_path
        roles_dir = tmp_path / "roles"
        roles_dir.mkdir()
        spec = ROLE_SPECS[0]
        override = "Custom role instructions from external file."
        (roles_dir / f"{spec.slug}.md").write_text(override, encoding="utf-8")
        assert resolve_role_instructions(spec) == override
    finally:
        mod._INSTRUCTIONS_ROOT = original_root


def test_resolve_workflow_instructions_prefers_external_file(tmp_path: Path) -> None:
    import pepper.core_specs as mod

    original_root = mod._INSTRUCTIONS_ROOT
    try:
        mod._INSTRUCTIONS_ROOT = tmp_path
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()
        spec = WORKFLOW_SPECS[0]
        override = "Custom workflow instructions from external file."
        (workflows_dir / f"{spec.slug}.md").write_text(override, encoding="utf-8")
        assert resolve_workflow_instructions(spec) == override
    finally:
        mod._INSTRUCTIONS_ROOT = original_root
