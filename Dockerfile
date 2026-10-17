# Build the exact AGPL source release stored alongside this file.
FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*
COPY stjernerne-source.zip /tmp/stjernerne-source.zip
RUN python -m zipfile -e /tmp/stjernerne-source.zip /src
WORKDIR /src/stjernerne-chart
RUN python scripts/build_native.py && python scripts/verify_native_threads.py

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /src/stjernerne-chart/requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock && useradd --uid 10001 --create-home stjernerne
COPY --from=build /src/stjernerne-chart/build ./build
COPY --from=build /src/stjernerne-chart/app ./app
COPY --from=build /src/stjernerne-chart/static ./static
COPY --from=build /src/stjernerne-chart/data ./data
COPY --from=build /src/stjernerne-chart/LICENSE /src/stjernerne-chart/COPYING /src/stjernerne-chart/THIRD_PARTY.md ./
COPY stjernerne-source.zip /app/source/stjernerne-source.zip
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1 EVOLUTION_HOME=1
EXPOSE 8765
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8765","--no-access-log","--no-proxy-headers"]
