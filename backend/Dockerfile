FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r astra && useradd -r -g astra astra && chown -R astra:astra /app
USER astra

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
