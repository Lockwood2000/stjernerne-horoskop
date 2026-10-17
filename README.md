# Stjernerne · School chart workspaces

Two teaching workspaces built on the existing Stjernerne Chart Workshop and its
Swiss Ephemeris engine. School demonstration release, 2026-10-17. The school profiles
are proposals, not school-approved defaults.

- `/institut`: Danish, Raleway/Mulish and warm colours.
- `/university`: English, Libre Baskerville/Montserrat and blue.
- `/`: the preserved English workshop with its existing rectification tools.

The Institut profile includes four personal study rooms under **Fordybelse**:
Venus Star Point, the lunar-node workshop, a life-event timeline and Louise
Kirsebom’s planetary-loop method. Open `/institut#sloejfer` for the loop room. See
[their method and verification notes](docs/INSTITUT-WORKSHOPS.md).

See [the current status](docs/SCHOOL-STATUS.md) for coverage, conventions,
reference checks and unfinished features. [SCHOOL-BASELINE.json](docs/SCHOOL-BASELINE.json)
records the original source and hashes. Earlier staging documents describe that baseline.

Both school workspaces include **Print / PDF**: a branded A4 preview for the
chart, current study room, reference tables and personal notes. Choose school
colours or monochrome, then print or save as PDF. See the
[print edition notes](docs/SCHOOL_PRINT.md) for content and layout details.

Placidus, Equal House and Regiomontanus, secondary progressions, true solar arc
and relocated solar returns are available in both school entries. Date, place
and method choices follow saved work and printed study pages. See the
[timing conventions and verification](docs/SCHOOL-TIMING.md).

## Run locally

Requires Python 3.12 and a C compiler. From this directory:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock
.venv/bin/python scripts/build_native.py
PUBLIC_ORIGIN=http://127.0.0.1:8772 .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8772 --no-access-log --no-proxy-headers
```

Open <http://127.0.0.1:8772/institut> or <http://127.0.0.1:8772/university>.
On macOS, `Start locally.command` starts the configured environment and opens both.
The development checkout reuses the existing Python environment through a local
`.venv` link, excluded from the source archive.

No API key is required. Calculations are not saved on the server. Explicitly
saved study work stays in this browser and origin, in a separate school library.
JSON export/import transfers study records between browsers. Original workshop
backup files use a different format and are not yet imported here.

## Test and package

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
node --test tests/*.test.mjs
.venv/bin/python scripts/package_source.py
```

The source archive at `/source` uses an explicit allowlist excluding credentials,
environments, browser libraries and private chart data. `deploy/Dockerfile`
builds the source archive. See [school hosting](docs/SCHOOL-DEPLOYMENT.md) for the
separate publication configuration.

## Licence and precision

AGPL-3.0-or-later; retained notices in LICENSE, COPYING and THIRD_PARTY.md.
School names and third-party material remain with their owners. Font files include
OFL licences and a source/hash manifest.

Swiss Ephemeris 2.10.03; tropical geocentric apparent positions. House system,
node, orbs and progression angles are explicit settings. Gregorian dates,
1500–2099; historical time-zone evidence needs checking. Placidus and Koch are
restricted below 66° latitude here, without silent substitution. Rectification
candidates do not prove a birth time. The direct ARGUS solar-key comparison
remains pending. The workspace supports the student's own interpretation.


### Astrology University study rooms

The existing `/university` workspace now includes its own blue/green visual
identity and four course-informed study rooms: Chart Synthesis, Your Year Ahead,
Prenatal Lunation and Relationship Dynamics. Notes and the second natal chart
travel with saved/exported study files. Open `/university#study-rooms` locally.
See [methods, sources and limitations](docs/UNIVERSITY-WORKSHOPS.md).
