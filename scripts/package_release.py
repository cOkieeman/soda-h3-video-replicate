#!/usr/bin/env python3
"""Build reproducible distribution files without repository history or local state."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOT_FILES = (
    "plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
    ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
    "README.md", "LICENSE", "NOTICE", ".gitignore",
)


def collect(directory: Path) -> list[Path]:
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not included in releases: {path.relative_to(ROOT)}")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
            files.append(path)
    return files


def write_zip(path: Path, entries: dict[str, Path]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, source in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())


def package_release(output: Path) -> list[Path]:
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    name, version = manifest["name"], manifest["version"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Invalid plugin name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Release version must have three numeric components")
    skill = ROOT / "skills" / name
    subprocess.run([sys.executable, "-I", str(skill / "scripts" / "build_single.py")], check=True)
    plugin_files = [ROOT / rel for rel in ROOT_FILES]
    for directory in (ROOT / "assets", ROOT / "scripts", ROOT / "tests", skill):
        plugin_files.extend(collect(directory))
    for path in plugin_files:
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"Release source must be a file inside the repository: {path}")
    output.mkdir(parents=True, exist_ok=True)
    plugin_zip = output / f"{name}-{version}-plugin.zip"
    skill_zip = output / f"{name}-{version}-skill.zip"
    standalone = output / f"{name}.single.md"
    write_zip(plugin_zip, {path.relative_to(ROOT).as_posix(): path for path in plugin_files})
    skill_entries = {f"{name}/{path.relative_to(skill).as_posix()}": path for path in collect(skill)}
    skill_entries.update({f"{name}/{rel}": ROOT / rel for rel in ("LICENSE", "NOTICE")})
    write_zip(skill_zip, skill_entries)
    shutil.copyfile(skill / "dist" / f"{name}.single.md", standalone)
    for rel in ("LICENSE", "NOTICE"):
        shutil.copyfile(ROOT / rel, output / rel)
    artifacts = [plugin_zip, skill_zip, standalone, output / "LICENSE", output / "NOTICE"]
    checksums = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in artifacts)
    checksum_file = output / "SHA256SUMS.txt"
    checksum_file.write_bytes(checksums.encode("utf-8"))
    return [*artifacts, checksum_file]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for path in package_release(args.output_dir.resolve()):
        print(f"Created {path.name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
