# Stjernerne Chart Workshop · English test

A separate English edition with the same design, wheel and numerical calculations.
The Danish public birth-data archive is excluded. No saved production charts are copied.

Includes birth charts, transit playback, solar returns, secondary progressions,
synastry, birth-time rectification, Kündig/Bonatti sections, both solar-key variants,
candidate/event comparison and a local library with backup/import.

See docs/ENGLISH-STAGING.md for isolation, numerical parity, test scope and hosting.
The demonstration uses fictional birth details in London.

## Run locally

Requires Python 3.12 and a C compiler. From this directory:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock
.venv/bin/python scripts/build_native.py
PUBLIC_ORIGIN=http://127.0.0.1:8771 .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8771 --no-access-log --no-proxy-headers
```

Open http://127.0.0.1:8771 . No API key is required. Calculations are not stored
on the server. Charts are saved in the browser only when the user chooses Save.

## Test and package

```sh
.venv/bin/python -m pytest -q
node --test tests/*.test.mjs
.venv/bin/python scripts/package_source.py
```

The ZIP uses an explicit allowlist excluding credentials, environments, private files,
browser libraries and the removed Danish archive. deploy/Dockerfile builds this ZIP.

## Licence and precision

AGPL-3.0-or-later with retained third-party notices: LICENSE, COPYING, THIRD_PARTY.md.
Brand and third-party data rights remain with their owners. The running app offers
corresponding source at /source. Swiss Ephemeris 2.10.03, tropical geocentric apparent
positions, Placidus and True Node. Historical time zones require source checking,
particularly before 1970. Dates are Gregorian; Placidus is limited to latitudes below
66 degrees north/south. Rectification candidates do not prove an actual birth time.
The published ARGUS reference has minute precision; a direct key/angle comparison
is pending. There is no automatic personal interpretation.

## Separate deployment

Use branch english-test and a separate Free Docker service, keeping production on main.
Port 8765, health path /api/health. The app adopts RENDER_EXTERNAL_URL for its origin.
No paid service or database is needed. Render Free has shared quotas and sleeps after
inactivity. This test app is not linked from the production website or its menu.
