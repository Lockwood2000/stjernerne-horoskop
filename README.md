# Stjernerne · Horoskopgenerator

Selvstændig dansk horoskopgenerator med fødselshoroskop, transitter med afspilning,
solretur, sekundære progressioner, synastri, fødselstidskorrektion med begivenhedssammenligning, Chiron, Ceres, Eris, Haumea og Makemake.

Hele den redigerbare kildekode, data, tests, byggevejledning og licensnotices
ligger i **stjernerne-source.zip**. Udpak arkivet for at udvikle videre.
Dockerfile bygger præcis denne kildepakke, og den kørende app tilbyder den via `/source`.

AGPL-3.0 med bevarede tredjepartsnotices; se LICENSE, COPYING og THIRD_PARTY.md i
arkivet. Stjernernes brandrettigheder gives ikke videre. Ingen garanti.

Frontend: HTML/CSS/JavaScript/SVG. Server: Python 3.12/FastAPI. Beregning:
Swiss Ephemeris 2.10.03 med lokale efemerider. 123 Python- og 7 JavaScript-tests
bestået før udgivelse. Ingen API-nøgler eller lagring af fødselsdata.

Render: separat Docker-webservice, Free, port 8765, health path `/api/health`.
Appen aflæser Render-URL automatisk. Gratis drift har kvoter og kan gå i dvale.
Historiske tidszoner før 1970 kræver konkret kontrol; Placidus understøttes
kun under 66° nord/syd. Ingen personlige fødselsdata er med i kildepakken.
