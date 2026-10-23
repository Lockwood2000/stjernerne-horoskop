"""Create deterministic <=20 MiB chunks from this app's exact dist directory."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
from restore_payload import sha256

CHUNK_SIZE = 20 * 1024 * 1024

def package(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not (source / 'index.html').is_file() or not (source / 'source/release-manifest.json').is_file():
        raise ValueError('Expected ROOTS & SKY dist with public source downloads')
    files = []
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if path.is_symlink() or any(part.startswith('.') for part in relative.parts):
            raise ValueError('Symlink or hidden path is not allowed: ' + str(relative))
        if path.is_file():
            files.append({'path':relative.as_posix(), 'size':path.stat().st_size, 'sha256':sha256(path)})
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='roots-sky-package-') as temporary:
        archive = Path(temporary) / 'payload.tar.gz'
        with archive.open('wb') as file, gzip.GzipFile(filename='', fileobj=file, mode='wb', mtime=0, compresslevel=9) as compressed:
            with tarfile.open(fileobj=compressed, mode='w', format=tarfile.USTAR_FORMAT) as tar:
                for entry in files:
                    info = tarfile.TarInfo(entry['path'])
                    info.size = entry['size']; info.mode = 0o644; info.mtime = 0; info.uid = info.gid = 0
                    with (source / entry['path']).open('rb') as content:
                        tar.addfile(info, content)
        chunks = []
        with archive.open('rb') as file:
            for index in range(10000):
                data = file.read(CHUNK_SIZE)
                if not data: break
                name = f'payload.part-{index:03d}'
                (output / name).write_bytes(data)
                chunks.append({'name':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        for old in output.glob('payload.part-*'):
            if old.name not in {chunk['name'] for chunk in chunks}:old.unlink()
        manifest = {'format':'roots-and-sky-static-split-v1', 'chunk_limit_bytes':CHUNK_SIZE,
                    'archive_format':'deterministic tar+gzip', 'archive_sha256':sha256(archive),
                    'archive_size':archive.stat().st_size, 'chunks':chunks, 'files':files}
        (output / 'payload-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    manifest=package(args.source,args.output)
    print(f"Packed {len(manifest['files'])} files into {len(manifest['chunks'])} chunks; archive SHA256 {manifest['archive_sha256']}")
