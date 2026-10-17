# Five horoscope generators — isolated combined trial

One Uvicorn process serves five preserved UIs from four frozen public source releases:
`/da/`, `/en/`, `/school/institut`, `/school/university`, `/evolution/`.
`/flyt` imports existing input-only JSON backups into the correct browser stores.
No server-side chart database or new external service is required.

Each engine retains its Python code, ephemerides and separate native Swiss library.
The assembly script changes root-relative browser URLs only. Existing designs,
teaching profiles, timing methods, archive picker, print and download features remain.
Institute PWA URLs and scope are adapted to `/school/institut`.

## Reproduce

Unzip `host-source.zip`, then put the other four `*-source.zip` archives in `inputs/`.
Their SHA256 values and observed public branch heads are in `inputs/provenance.json`.
Python 3.12, a C compiler, and the pinned requirements are needed.

```
python -m pip install -r requirements.lock
python scripts/assemble.py
PUBLIC_ORIGIN=http://127.0.0.1:8786 python -m uvicorn host.main:app --host 127.0.0.1 --port 8786 --no-access-log --no-proxy-headers
python -m pytest tests/test_host.py -q
node --test tests/transfer.test.mjs
python scripts/benchmark.py http://127.0.0.1:8786 --label local
```

For Docker, put all five ZIPs alongside the Dockerfile. The new Render service must
use its own branch; do not redirect or remove any original service. The intended
paid plan is 0.5 CPU/512 MB ($7/month base compute at preparation). A Free deployment
or local benchmark does not establish performance on that paid allocation. Check
the actual Render compute setting, cgroup observations, latency and memory report.
Bandwidth, build quotas and applicable taxes are separate from base compute.

## Transfer guarantees and limits

Original browser storage is origin-bound. The old sites cannot be read from the
trial. Users export from the old site and select the files themselves. DA and EN
use the same backup format and require an explicit destination selection. Their
existing database names remain distinct; the school profiles retain their shared,
profile-filtered database. Imports create records, never update existing records.
Exact duplicates are skipped. Evolutionary imports retain input, view and notes,
discard supplied results and keep a separate transfer history before activating a
selected saved chart. Keep original JSON files. Capacity/storage failure may stop
a batch after some completed writes; the UI reports the completed count and retry
skips identical records. This is not cloud synchronization or automatic migration.

The host and adaptations are AGPL-3.0-or-later. Every original archive retains its
LICENSE, COPYING and third-party notices, including Swiss Ephemeris and font/data
licences. `/source` offers all five archives required to reproduce the running app.
