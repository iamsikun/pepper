# venue-formatter

Prepare the target-specific submission package and formatting checks.

## Expected Outputs

- `paper/<active_target>/camera-ready/`
- `paper/<active_target>/camera-ready/VERIFICATION.md`

## Capability Contract

- `read_files`
- `write_files`
- `run_shell`

## Instructions

Use the venue template manifest and target metadata to prepare the final
submission package, ensure anonymization mode is correct, and surface formatting or artifact gaps
before packaging.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.
