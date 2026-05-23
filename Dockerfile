# Imagen para DigitalOcean App Platform (y Docker en general)
# Puerto HTTP: 8000 — configurarlo igual en el panel de DO

FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema mínimas (certificados SSL para Supabase, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENV PORT=8000

ENTRYPOINT ["/entrypoint.sh"]
