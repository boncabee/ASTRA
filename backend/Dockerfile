FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

RUN groupadd -g 1001 astra && useradd -u 1001 -g astra -m astra && chown -R astra:astra /app
USER astra

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request, urllib.error, sys; exec(\"try: urllib.request.urlopen('http://localhost:8000/api/v1/health')\nexcept urllib.error.HTTPError as e: sys.exit(0 if e.code == 200 else 1)\nexcept Exception: sys.exit(1)\")" || exit 1

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
