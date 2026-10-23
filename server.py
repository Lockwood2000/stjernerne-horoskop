"""A deliberately small, read-only ROOTS & SKY static server (standard library)."""
from __future__ import annotations
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
import os
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent / 'dist'
MIME = {'.mjs': 'text/javascript; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
        '.wasm': 'application/wasm', '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
        '.zip': 'application/zip', '.gz': 'application/gzip', '.data': 'application/octet-stream'}

class StaticHandler(BaseHTTPRequestHandler):
    server_version = 'RootsSky'
    sys_version = ''

    def log_message(self, *_args):
        # No request logs: the app has no server-side visitor or report store.
        pass

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        super().end_headers()

    def do_GET(self):
        self.serve(head=False)

    def do_HEAD(self):
        self.serve(head=True)

    def do_POST(self):
        self.send_error(405, 'Read-only static service')

    do_PUT = do_DELETE = do_PATCH = do_POST

    def serve(self, head=False):
        try:
            path = unquote(urlsplit(self.path).path, errors='strict')
            if not path.startswith('/') or '\\' in path or '%' in path or '\x00' in path:
                raise ValueError('Invalid path')
            parts = [part for part in path.split('/') if part]
            if any(part.startswith('.') for part in parts):
                raise ValueError('Private path')
            root = Path(self.server.document_root).resolve()
            target = root.joinpath(*parts)
            cursor = root
            for part in parts:
                cursor = cursor / part
                if cursor.is_symlink():
                    raise ValueError('Symbolic link')
            target.resolve().relative_to(root)
            if target.is_dir():
                if not path.endswith('/'):
                    # Relative resource paths in directory index pages need a trailing slash.
                    self.send_response(308)
                    self.send_header('Location', path + '/')
                    self.send_header('Content-Length', '0')
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    return
                target = target / 'index.html'
            if not target.is_file() or target.is_symlink():
                raise ValueError('Missing file')
        except (ValueError, UnicodeError, OSError):
            self.send_error(404, 'File not found')
            return
        try:
            stat = target.stat()
            key = (str(target), stat.st_size, stat.st_mtime_ns)
            etag = self.server.etags.get(key)
            if etag is None:
                with target.open('rb') as source:
                    etag = '"' + hashlib.file_digest(source, 'sha256').hexdigest() + '"'
                self.server.etags[key] = etag
            if self.headers.get('If-None-Match') == etag:
                self.send_response(304)
                self.send_header('ETag', etag)
                self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
                self.end_headers()
                return
            with target.open('rb') as source:
                self.send_response(200)
                self.send_header('Content-Type', MIME.get(target.suffix.lower(), mimetypes.guess_type(target.name)[0] or 'application/octet-stream'))
                self.send_header('Content-Length', str(stat.st_size))
                self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
                self.send_header('ETag', etag)
                self.end_headers()
                if not head:
                    shutil.copyfileobj(source, self.wfile, 64 * 1024)
        except (BrokenPipeError, ConnectionResetError):
            pass


def make_server(host='0.0.0.0', port=8080, root=ROOT):
    server = ThreadingHTTPServer((host, port), StaticHandler)
    server.daemon_threads = True
    server.document_root = Path(root).resolve()
    server.etags = {}
    return server


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    if not 1 <= port <= 65535:
        raise SystemExit('PORT must be between 1 and 65535')
    if not (ROOT / 'index.html').is_file():
        raise SystemExit('Missing dist/index.html; reconstruct the payload first')
    make_server(port=port).serve_forever()
