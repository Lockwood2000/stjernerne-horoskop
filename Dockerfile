FROM python:3.12-slim AS payload
WORKDIR /build
COPY restore_payload.py payload-manifest.json payload.part-* ./
RUN python restore_payload.py --destination /build/dist

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /app
RUN groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app --no-create-home app
COPY --from=payload --chown=app:app /build/dist /app/dist
COPY --chown=app:app server.py /app/server.py
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8080')+'/',timeout=4).close()"
CMD ["python", "server.py"]
