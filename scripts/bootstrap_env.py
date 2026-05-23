"""
Arranque en producción: .env de EasyPanel + ruta GCP desde GitHub Actions.
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("/app/.env")
if Path("/app/.env.google").exists():
    load_dotenv("/app/.env.google")
load_dotenv()

cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path or not Path(cred_path).is_file():
    print(
        "ERROR: Falta el archivo en GOOGLE_APPLICATION_CREDENTIALS "
        f"({cred_path!r}). Ejecuta el workflow de GitHub Actions.",
        file=sys.stderr,
    )
    sys.exit(1)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path(cred_path).resolve())

port = os.getenv("PORT", "8000")
os.execvp(
    "streamlit",
    [
        "streamlit",
        "run",
        "main.py",
        f"--server.port={port}",
        "--server.address=0.0.0.0",
        "--server.headless=true",
    ],
)
