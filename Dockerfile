FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*
COPY host-source.zip /tmp/host-source.zip
RUN python -m zipfile -e /tmp/host-source.zip /src
WORKDIR /src/combined-trial
COPY da-source.zip en-source.zip school-source.zip evolution-source.zip ./inputs/
RUN mkdir -p reports && python scripts/assemble.py

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /src/combined-trial/requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock && useradd --uid 10001 --create-home stjernerne
COPY --from=build /src/combined-trial/editions ./editions
COPY --from=build /src/combined-trial/host ./host
COPY --from=build /src/combined-trial/inputs ./inputs
COPY host-source.zip ./inputs/host-source.zip
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8765
CMD ["python","-m","uvicorn","host.main:app","--host","0.0.0.0","--port","8765","--no-access-log","--no-proxy-headers"]
