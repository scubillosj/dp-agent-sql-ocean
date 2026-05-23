# Deploy en DigitalOcean App Platform

## Requisitos previos

- Proyecto en **GitHub** (sin `.env` ni `credentials/*.json`)
- Cuenta en [DigitalOcean](https://www.digitalocean.com)
- Variables del `.env` listas (OpenAI, GCP, Supabase)

## 1. Subir a GitHub

```powershell
cd "ruta\al\proyecto"
git init
git add .
git status   # verifica que NO aparezcan .env ni credentials/*.json
git commit -m "Agente CitiBike - deploy DigitalOcean"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## 2. Crear la App en DigitalOcean

1. **Apps** → **Create App** → **GitHub** → elige el repositorio.
2. Tipo de deploy: **Dockerfile** (no buildpack Python suelto).
3. **HTTP Port:** `8000`
4. **Instance size:** el más bajo suele bastar para demo académica.

## 3. Variables de entorno (todas como **Encrypt / Secret**)

| Variable | Valor |
|----------|--------|
| `OPENAI_API_KEY` | Tu API key de OpenAI |
| `GOOGLE_CLOUD_PROJECT` | ID del proyecto GCP |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` (o tu región) |
| `GOOGLE_CREDENTIALS_JSON` | **Contenido completo** del JSON de la service account (una variable, todo el `{...}`) |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | Contraseña de Supabase |
| `DB_HOST` | `db.xxxx.supabase.co` |
| `DB_PORT` | `5432` o `6543` (pooler) |
| `DB_NAME` | `postgres` |
| `DB_SCHEMA` | `agent_text_to_sql` |

**No configures** `GOOGLE_APPLICATION_CREDENTIALS` en DO: el `entrypoint.sh` crea `/tmp/gcp-service-account.json` automáticamente desde `GOOGLE_CREDENTIALS_JSON`.

### Cómo pegar el JSON en `GOOGLE_CREDENTIALS_JSON`

1. Abre tu archivo local `credentials/tu-archivo.json`.
2. Copia **todo** (desde `{` hasta `}`).
3. Pégalo en el valor del secreto en DigitalOcean.
4. Puede ir en una sola línea o multilínea según permita el panel.

## 4. Deploy y prueba

1. **Deploy** y espera a que el build termine en verde.
2. Abre la URL pública (`https://tu-app-xxxxx.ondigitalocean.app`).
3. En el sidebar: OpenAI ✅, BigQuery ✅, Histórico ✅.
4. Prueba: *¿Cuántos viajes en total hay?*

## 5. Entrega al docente

```
Link: https://tu-app-xxxxx.ondigitalocean.app
Repositorio: https://github.com/TU_USUARIO/TU_REPO
```

## Probar el contenedor en local (opcional)

```powershell
docker build -t citibike-agent .
docker run --rm -p 8000:8000 `
  -e OPENAI_API_KEY="..." `
  -e GOOGLE_CLOUD_PROJECT="..." `
  -e GOOGLE_CREDENTIALS_JSON="$(Get-Content -Raw credentials\tu-archivo.json)" `
  -e DB_USER="postgres" `
  -e DB_PASSWORD="..." `
  -e DB_HOST="db.xxxx.supabase.co" `
  -e DB_PORT="5432" `
  -e DB_NAME="postgres" `
  -e DB_SCHEMA="agent_text_to_sql" `
  citibike-agent
```

Abre `http://localhost:8000`.

## Notas

- **No** uses GitHub Actions para secretos; van en el panel de DO.
- Si cambias código: `git push` y DO redeploya solo (si activaste auto-deploy).
- El histórico de chat y las tablas de LangGraph se crean solos en Supabase al primer arranque.
