from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .manifest import InstallManifest
from .sync import MANIFEST_PATH, dev_sync_root, find_repo_root, install_or_sync, package_version
from .validate import validate_repo


def _print_conflicts(conflicts: list[str]) -> None:
    print("conflicts detected in managed files:")
    for relative in conflicts:
        print(f"  - {relative}")


def _cmd_install(args: argparse.Namespace) -> int:
    repo_root = find_repo_root(Path.cwd())
    manifest_path = repo_root / MANIFEST_PATH
    if manifest_path.exists() and not args.force:
        print("pepper scaffold is already installed in this repo.")
        print("use 'pepper sync' to update, or 'pepper install --force' to reinstall.")
        return 1
    result = install_or_sync(repo_root, force=args.force, write_manifest=True)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        print("rerun with --force to overwrite managed-file conflicts")
        return 1
    print(f"installed pepper scaffold into {repo_root}")
    return 0


def _cmd_sync(args: argparse.Namespace) -> int:
    repo_root = find_repo_root(Path.cwd())
    manifest_path = repo_root / MANIFEST_PATH
    if not manifest_path.exists():
        print("pepper scaffold is not installed in this repo.")
        print("run 'pepper install' first.")
        return 1
    result = install_or_sync(repo_root, force=args.force, write_manifest=True)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        print("rerun with --force to overwrite managed-file conflicts")
        return 1
    print(f"synchronized pepper scaffold in {repo_root}")
    return 0


def _cmd_validate(_: argparse.Namespace) -> int:
    repo_root = find_repo_root(Path.cwd())
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
    repo_root = find_repo_root(Path.cwd())
    manifest = InstallManifest.load(repo_root / MANIFEST_PATH)
    current = package_version()
    print(f"package version: {current}")
    if manifest is None:
        print("installed scaffold version: not installed")
        return 0
    print(f"installed scaffold version: {manifest.package_version}")
    print(f"in sync: {'yes' if manifest.package_version == current else 'no'}")
    return 0


def _cmd_dev_sync_root(_: argparse.Namespace) -> int:
    repo_root = find_repo_root(Path.cwd())
    result = dev_sync_root(repo_root)
    if result.conflicts:
        _print_conflicts(result.conflicts)
        return 1
    print(f"synchronized root scaffold mirror in {repo_root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pepper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install the scaffold into the current repo")
    install_parser.add_argument("--force", action="store_true", help="Overwrite managed-file conflicts")
    install_parser.set_defaults(func=_cmd_install)

    sync_parser = subparsers.add_parser("sync", help="Sync scaffold files in the current repo")
    sync_parser.add_argument("--force", action="store_true", help="Overwrite managed-file conflicts")
    sync_parser.set_defaults(func=_cmd_sync)

    validate_parser = subparsers.add_parser("validate", help="Validate the scaffold and runtime state")
    validate_parser.set_defaults(func=_cmd_validate)

    version_parser = subparsers.add_parser("version", help="Show package and installed scaffold versions")
    version_parser.set_defaults(func=_cmd_version)

    dev_parser = subparsers.add_parser("dev-sync-root", help="Sync packaged assets back into this repo root")
    dev_parser.set_defaults(func=_cmd_dev_sync_root)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))
