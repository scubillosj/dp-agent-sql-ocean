#!/bin/sh
# EasyPanel guarda variables en /app/.env; Python las carga antes de Streamlit.
set -e
exec python3 /app/scripts/bootstrap_env.py
