from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(slots=True)
class InstallManifest:
    package_version: str
    installed_at: str
    managed_files: list[str]
    hashes: dict[str, str]

    @classmethod
    def create(cls, package_version: str, hashes: dict[str, str]) -> "InstallManifest":
        return cls(
            package_version=package_version,
            installed_at=datetime.now(UTC).isoformat(),
            managed_files=sorted(hashes),
            hashes=hashes,
        )

    @classmethod
    def load(cls, path: Path) -> "InstallManifest | None":
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            package_version=data["package_version"],
            installed_at=data["installed_at"],
            managed_files=list(data["managed_files"]),
            hashes=dict(data["hashes"]),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "package_version": self.package_version,
            "installed_at": self.installed_at,
            "managed_files": self.managed_files,
            "hashes": self.hashes,
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
