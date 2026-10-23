"""Verify split transport payload and safely restore its exact static files."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile


def sha256(path):
    with Path(path).open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def restore(bundle, destination):
    bundle, destination = Path(bundle).resolve(), Path(destination).resolve()
    manifest = json.loads((bundle / 'payload-manifest.json').read_text())
    if destination.exists():
        raise ValueError('Destination already exists; refusing to overwrite it')
    entries = {entry['path']: entry for entry in manifest['files']}
    if len(entries) != len(manifest['files']):
        raise ValueError('Duplicate manifest paths')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='roots-sky-restore-', dir=destination.parent) as temporary:
        temporary = Path(temporary)
        archive = temporary / 'payload.tar.gz'
        with archive.open('wb') as target:
            for chunk in manifest['chunks']:
                name = chunk['name']
                if Path(name).name != name or not name.startswith('payload.part-'):
                    raise ValueError('Invalid chunk name')
                path = bundle / name
                if path.stat().st_size != chunk['size'] or sha256(path) != chunk['sha256']:
                    raise ValueError('Chunk checksum mismatch: ' + name)
                with path.open('rb') as source:
                    shutil.copyfileobj(source, target)
        if sha256(archive) != manifest['archive_sha256']:
            raise ValueError('Reconstructed archive checksum mismatch')
        staging = temporary / 'dist'
        staging.mkdir()
        seen = set()
        with tarfile.open(archive, 'r:gz') as tar:
            for member in tar:
                path = Path(member.name)
                if (not member.isfile() or path.is_absolute() or any(part.startswith('.') for part in path.parts)
                        or '\\' in member.name or member.name not in entries or member.name in seen):
                    raise ValueError('Unsafe or unexpected archive entry: ' + member.name)
                expected = entries[member.name]
                if member.size != expected['size']:
                    raise ValueError('Archive entry size mismatch')
                target = staging / path
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, target.open('wb') as output:
                    shutil.copyfileobj(source, output)
                target.chmod(0o644)
                if sha256(target) != expected['sha256']:
                    raise ValueError('File checksum mismatch: ' + member.name)
                seen.add(member.name)
        if seen != set(entries):
            raise ValueError('Archive is missing manifest entries')
        staging.rename(destination)
    return len(entries)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', type=Path, default=Path(__file__).resolve().parent / 'dist')
    args = parser.parse_args()
    count = restore(Path(__file__).resolve().parent, args.destination)
    print(f'Verified and restored {count} static files.')
