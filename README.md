# Stjernerne · Horoskopgenerator


Selvstændig dansk horoskopgenerator med fødselshoroskop, transitter med afspilning,
solretur, sekundære progressioner, synastri, fødselstidskorrektion med begivenhedssammenligning, Chiron, Ceres, Eris, Haumea og Makemake.


Hele den redigerbare kildekode, data, tests, byggevejledning og licensnotices
ligger i **stjernerne-source.zip**. Udpak arkivet for at udvikle videre.
Dockerfile bygger præcis denne kildepakke, og den kørende app tilbyder den via `/source`.


AGPL-3.0 med bevarede tredjepartsnotices; se LICENSE, COPYING og THIRD_PARTY.md i
arkivet. Stjernernes brandrettigheder gives ikke videre. Ingen garanti.


Frontend: HTML/CSS/JavaScript/SVG. Server: Python 3.12/FastAPI. Beregning:
Swiss Ephemeris 2.10.03 med lokale efemerider. 175 Python- og 31 JavaScript-tests
bestået før udgivelse. Ingen API-nøgler eller lagring af fødselsdata på serveren.


Render: separat Docker-webservice, Free, port 8765, health path `/api/health`.
Appen aflæser Render-URL automatisk. Gratis drift har kvoter og kan gå i dvale.
Historiske tidszoner før 1970 kræver konkret kontrol; Placidus understøttes
kun under 66° nord/syd. Kildepakken indeholder 189 offentlige arkivposter fra Astrologi-Arkaden; ingen private brugerdata.


Mine horoskoper: lokalt bibliotek med tidskandidater, livsbegivenheder, backup/import og papirkurv. Ingen konto eller serverlagring.


Forenklet navigation med seks horoskopvalg, sammenfoldelige indstillinger og stort horoskophjul med zoom. Mobilvisningen giver hjulet mere plads.



Vælg en kendt dansker: søg i 189 gennemgåede arkivposter, se rating og kilder, og udfyld fødselsoplysninger automatisk. Alternative tider bevares som separate valg. Ukendte tider (X) udfyldes ikke; datoer før 1500 og manglende koordinater markeres som utilgængelige. Se docs/FAMOUS-DANES.md i kildepakken.


Kündigs metode: beregn snittidspunkter omkring originalen, vis dem i hjulet, behold dem som tidskandidater og sammenlign med livsbegivenheder. Sekunder bevares i bibliotek og backup/import. Traditionelle MC/IC-herskere og ekliptiske meridiankonjunktioner; se docs/KUNDIG.md for metode og afgrænsning. Kündigs individuelle solnøgle kan vælges til progressive akser og begivenhedssammenligning. Nøglen bruger den hele zodiakgrad, fødselssolen står i, omregnet til rektascension. Metodevalg følger bibliotek og backup/import; ældre gemte valg bevares. Se docs/SOLAR-KEY.md for præcis konvention og afgrænsning. Bonatti-snit kan vises alene eller sammen med Kündig-snit. Aksekonjunktioner for Solen til Pluto markeres med planet og AC/DC/MC/IC. Sammenfald samles til ét sekund med begge mærker; mærkerne følger kandidater, begivenhedstabeller og backup/import. Se docs/BONATTI.md for metodekonvention og kontrol.
