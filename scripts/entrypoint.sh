#!/bin/sh
# Arranque en producción (DigitalOcean, Docker, etc.)
# - Local: usa GOOGLE_APPLICATION_CREDENTIALS apuntando a credentials/*.json
# - Nube: pega el JSON completo en GOOGLE_CREDENTIALS_JSON (secreto en DO)

set -e

GCP_KEY_FILE="${GOOGLE_APPLICATION_CREDENTIALS:-/tmp/gcp-service-account.json}"

if [ -n "$GOOGLE_CREDENTIALS_JSON" ]; then
  printf '%s' "$GOOGLE_CREDENTIALS_JSON" > "$GCP_KEY_FILE"
  chmod 600 "$GCP_KEY_FILE"
  export GOOGLE_APPLICATION_CREDENTIALS="$GCP_KEY_FILE"
elif [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ] && [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
  echo "ERROR: GOOGLE_APPLICATION_CREDENTIALS no existe y GOOGLE_CREDENTIALS_JSON está vacío." >&2
  exit 1
fi

exec streamlit run main.py \
  --server.port="${PORT:-8000}" \
  --server.address=0.0.0.0 \
  --server.headless=true
