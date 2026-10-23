# ROOTS & SKY — isolated Railway deployment

This directory is a deployment bundle for a **separate ROOTS & SKY service**. It does not modify or replace Institut, its Railway service, domain, environment variables or branch.

## Payload and transport

The static payload is an exact byte-for-byte snapshot of the existing ROOTS & SKY `dist/` directory, including both public corresponding-source downloads. `payload-manifest.json` records every file's SHA256 and size, the complete archive SHA256 and every chunk's checksum. `payload.part-*` are deterministic tar/gzip slices of at most 20 MiB each, suitable for the browser's per-file upload limit. The archive is reconstructed and verified during the Docker build; no archive or part files are exposed by the web server.

Included are only this application, its seven existing illustrations, browser calculation runtime, offline data, licences and published source archives. No hosting identity, repository metadata, credentials, customer reports or other school interfaces are included. Fictional regression fixtures already in the corresponding-source archive remain part of that unchanged archive.

## Dedicated deployment

1. Use the dedicated `roots-and-sky` branch of `Lockwood2000/stjernerne-horoskop`, whose root contains only this bundle. Do not connect the Institut production branch or change its service.
2. Upload **all** `payload.part-*` files, `payload-manifest.json`, `restore_payload.py`, `server.py` and `Dockerfile` at the repository root. Keep each browser-upload commit below 25 MB; commit each payload part separately and deploy only after all parts are present. The README, packaging script and tests can accompany them. `.dockerignore` is recommended but optional: Docker copies only explicitly named inputs.
3. In Railway, create a new service connected to that repository/branch. Select Dockerfile as the builder in Railway’s service settings, with the Dockerfile at the root. Set the health-check path to `/` and the timeout to 120 seconds in the UI. New services do not support the deprecated configuration-as-code workflow, so this bundle deliberately does not rely on a `railway.json` file. Do not create a second service by modifying Institut's existing service settings. The service needs no secrets or API keys.
4. Railway provides `PORT`; the server binds to `0.0.0.0` on that port and defaults to 8080 locally. The health check requests `/`.
5. Generate the new service's own public Railway domain, then verify it over HTTPS before sharing. Use only a verified address whose complete URL passes the user's link rule. This bundle contains no invented production URL. A custom domain can be configured for this new service separately.

## Local checks

Use Python 3.12 or later. No third-party Python packages are needed.

```sh
python3 -m unittest -v test_bundle.py
python3 restore_payload.py
PORT=8080 python3 server.py
```

After reconstruction, open `http://localhost:8080/`. Reconstruction refuses to overwrite an existing `dist` directory. For a test directory instead, pass `--destination /tmp/roots-sky-verified-dist` to `restore_payload.py` (choose a path that does not already exist).

With Docker available:

```sh
docker build -t roots-and-sky .
docker run --rm -p 8080:8080 -e PORT=8080 roots-and-sky
```

The final container runs as a dedicated unprivileged user. It serves only `dist`, returns correct JavaScript-module and WebAssembly MIME types, disallows directory listings, traversal, hidden paths and symlinks, and disables request logging. Assets are revalidated using content SHA256 ETags so a new deployment cannot leave a stale unversioned application cached. Birth details are processed by the existing browser worker; the server supplies static files only.

## Refreshing the bundle

Run `package_payload.py` with the reviewed app's `dist` directory as its source. Do not pass a repository root. Regenerate the application's corresponding-source archives in its own source project first if its implementation has changed. Then rerun the tests and commit all changed chunks and the manifest together.

```sh
python3 package_payload.py /absolute/path/to/roots-and-sky/dist
python3 -m unittest -v test_bundle.py
```

Determinism uses sorted file paths, fixed tar ownership/modes/timestamps, and gzip without a filename or current timestamp. The Docker base is the standard `python:3.12-slim` tag and can receive upstream security updates; full image-byte reproducibility is not claimed.
