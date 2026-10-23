"""Meaningful transport and HTTP regression checks; standard library only."""
import hashlib
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from package_payload import package, CHUNK_SIZE
from restore_payload import restore, sha256
from server import make_server

BUNDLE = Path(__file__).resolve().parent

class TransportTests(unittest.TestCase):
    def test_real_payload_restore_and_full_inventory(self):
        manifest=json.loads((BUNDLE/'payload-manifest.json').read_text())
        self.assertGreater(len(manifest['files']), 50)
        self.assertTrue(all(0 < chunk['size'] <= CHUNK_SIZE for chunk in manifest['chunks']))
        with tempfile.TemporaryDirectory() as temporary:
            target=Path(temporary)/'dist'
            self.assertEqual(restore(BUNDLE,target),len(manifest['files']))
            self.assertEqual({p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}, {e['path'] for e in manifest['files']})
            for entry in manifest['files']:
                self.assertEqual(sha256(target/entry['path']),entry['sha256'])
            self.assertTrue((target/'source/roots-and-sky-source.zip').is_file())
            self.assertTrue((target/'source/roots-and-sky-runtime.zip').is_file())
            with self.assertRaisesRegex(ValueError,'already exists'):restore(BUNDLE,target)

    def test_deterministic_package_and_corruption_rejection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'source';(source/'source').mkdir(parents=True)
            (source/'index.html').write_text('ROOTS & SKY')
            (source/'source/release-manifest.json').write_text('{}')
            first=package(source,root/'one');second=package(source,root/'two')
            self.assertEqual(first,second)
            self.assertEqual((root/'one/payload.part-000').read_bytes(),(root/'two/payload.part-000').read_bytes())
            chunk=root/'one/payload.part-000';data=bytearray(chunk.read_bytes());data[10]^=1;chunk.write_bytes(data)
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):restore(root/'one',root/'rejected')
            self.assertFalse((root/'rejected').exists())

    def test_packer_rejects_dotfiles_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'source';(source/'source').mkdir(parents=True)
            (source/'index.html').write_text('ROOTS & SKY');(source/'source/release-manifest.json').write_text('{}')
            (source/'.env').write_text('not a real secret')
            with self.assertRaisesRegex(ValueError,'hidden'):package(source,root/'out')
            (source/'.env').unlink();(source/'linked').symlink_to(source/'index.html')
            with self.assertRaisesRegex(ValueError,'Symlink'):package(source,root/'out')

    def test_docker_build_contract(self):
        docker=(BUNDLE/'Dockerfile').read_text()
        self.assertIn('FROM python:3.12-slim AS payload',docker)
        self.assertIn('python restore_payload.py',docker)
        self.assertIn('USER app',docker)
        self.assertIn('COPY --from=payload',docker)
        self.assertNotIn('pip install',docker)
        self.assertIn('HEALTHCHECK',docker)
        self.assertIn('PORT=8080',docker)

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();root=Path(cls.temp.name);cls.root=root/'dist';cls.root.mkdir()
        for name,content in [('index.html',b'<h1>ROOTS & SKY</h1>'),('app.mjs',b'export{}'),('engine.wasm',b'\x00asm'),('pack.zip',b'PK'),('.env',b'private')]:
            (cls.root/name).write_bytes(content)
        (cls.root/'source').mkdir();(cls.root/'source/index.html').write_text('Source and licences')
        (cls.root/'empty').mkdir();(root/'secret').write_text('private');(cls.root/'link').symlink_to(root/'secret')
        cls.server=make_server('127.0.0.1',0,cls.root)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.temp.cleanup()
    def request(self,path,method='GET',headers=None):
        connection=http.client.HTTPConnection(*self.server.server_address)
        connection.request(method,path,headers=headers or {})
        response=connection.getresponse();result=(response.status,dict(response.getheaders()),response.read());connection.close();return result
    def test_root_head_mime_and_safe_caching(self):
        for path,mime in [('/','text/html'),('/app.mjs','text/javascript'),('/engine.wasm','application/wasm'),('/pack.zip','application/zip')]:
            status,headers,body=self.request(path)
            self.assertEqual(status,200);self.assertIn(mime,headers['Content-Type'])
            self.assertEqual(headers['Cache-Control'],'public, max-age=0, must-revalidate')
            self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
            self.assertEqual(int(headers['Content-Length']),len(body))
            self.assertEqual(self.request(path,headers={'If-None-Match':headers['ETag']})[0],304)
        status,headers,body=self.request('/','HEAD');self.assertEqual(status,200);self.assertEqual(body,b'')
    def test_directory_index_and_no_listing(self):
        self.assertEqual(self.request('/source')[0],308)
        self.assertEqual(self.request('/source')[1]['Location'],'/source/')
        self.assertEqual(self.request('/source/')[0],200)
        self.assertEqual(self.request('/empty/')[0],404)
    def test_private_files_traversal_and_links_rejected(self):
        for path in ['/.env','/../secret','/%2e%2e/secret','/%252e%252e/secret','/source/../index.html','/link','/%5c../secret','/%00','/.git/config']:
            self.assertEqual(self.request(path)[0],404,path)
    def test_no_mutations(self):
        for method in ['POST','PUT','PATCH','DELETE']:
            self.assertEqual(self.request('/',method)[0],405)

if __name__=='__main__':unittest.main(verbosity=2)
