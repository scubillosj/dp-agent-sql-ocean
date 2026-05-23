"""
Arranque en producción: carga env de EasyPanel + .env.gcp (GitHub Actions) y escribe GCP JSON.
"""
import base64
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_CRED_PATH = "/app/credentials/gcp-sa.json"


def resolve_gcp_json_text() -> str | None:
    """Obtiene el JSON de la service account desde env (Base64 o texto plano)."""
    b64 = (os.getenv("GOOGLE_CREDENTIALS_B64") or "").strip()
    if b64:
        try:
            return base64.b64decode(b64).decode("utf-8")
        except Exception as exc:
            print(f"ERROR: GOOGLE_CREDENTIALS_B64 inválido: {exc}", file=sys.stderr)
            sys.exit(1)

    raw = (os.getenv("GOOGLE_CREDENTIALS_JSON") or "").strip()
    if raw:
        return raw

    return None


def setup_google_credentials() -> None:
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or DEFAULT_CRED_PATH
    gcp_json = resolve_gcp_json_text()

    if gcp_json:
        path = Path(cred_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(gcp_json, encoding="utf-8")
        path.chmod(0o600)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(path.resolve())
    elif cred_path and Path(cred_path).is_file():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path(cred_path).resolve())
    else:
        print(
            "ERROR: Falta credencial GCP. Opciones:\n"
            "  1) Ejecuta el workflow 'Sync GCP credentials' en GitHub Actions, o\n"
            "  2) En EasyPanel agrega GOOGLE_CREDENTIALS_B64 al .env.",
            file=sys.stderr,
        )
        sys.exit(1)


load_dotenv("/app/.env")
load_dotenv("/app/.env.gcp")
load_dotenv()
setup_google_credentials()

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
