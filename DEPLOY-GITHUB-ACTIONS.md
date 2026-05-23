# Credenciales GCP vía GitHub Actions (recomendado en EasyPanel)

Flujo:

```text
GitHub Secret (Base64)  →  SSH al Droplet  →  /app/.env.gcp en el contenedor
                                                      ↓
                                            bootstrap escribe gcp-sa.json
                                                      ↓
                                                 BigQuery OK
```

**No pegues** el JSON ni el Base64 largo en el editor de EasyPanel (se trunca). EasyPanel solo lleva OpenAI, Supabase y `GOOGLE_CLOUD_PROJECT`.

---

## Paso 1 — Generar el secret Base64 (en tu PC)

PowerShell, desde la raíz del proyecto:

```powershell
$json = Get-Content -Raw "credentials\datapath-prueba-0e2600ec5dc4.json"
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
$b64.Length   # debe ser ~3000+, no cientos
$b64 | Set-Clipboard
```

---

## Paso 2 — Secrets en GitHub

Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Valor |
|--------|--------|
| `GCP_CREDENTIALS_B64` | La línea Base64 del paso 1 (pega desde portapapeles) |
| `DROPLET_HOST` | `157.230.91.250` (tu IP) |
| `DROPLET_USER` | `root` (o el usuario SSH que uses) |
| `DROPLET_SSH_KEY` | Contenido **completo** de la clave privada (`digitalocean_dp_agent` o similar) |
| `DOCKER_CONTAINER_NAME` | *(opcional)* Nombre exacto del contenedor; si no, el workflow lo busca |

Alternativa: en lugar de `GCP_CREDENTIALS_B64` puedes usar `GOOGLE_APPLICATION_CREDENTIALS` con el **JSON completo**; el workflow lo codifica solo.

---

## Paso 3 — Clave SSH en el Droplet

En el servidor (como root):

```bash
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys   # pega la clave PÚBLICA (.pub) que generaste en Windows
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Prueba desde tu PC:

```powershell
ssh -i $env:USERPROFILE\.ssh\digitalocean_dp_agent root@157.230.91.250
```

---

## Paso 4 — EasyPanel `.env` (sin credencial GCP)

En el panel de la app, **solo**:

```env
OPENAI_API_KEY=sk-...
GOOGLE_CLOUD_PROJECT=datapath-prueba
GOOGLE_CLOUD_LOCATION=us-central1
DB_USER=postgres
DB_PASSWORD=...
DB_HOST=db.xxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_SCHEMA=agent_text_to_sql
```

**No** incluyas `GOOGLE_CREDENTIALS_B64` ni `GOOGLE_APPLICATION_CREDENTIALS=credentials/...`.

Guarda y haz **Deploy** del código (pull desde GitHub).

---

## Paso 5 — Subir cambios y ejecutar el workflow

En tu PC:

```powershell
cd "ruta\al\proyecto"
git add .
git commit -m "Sync GCP credentials via GitHub Actions"
git push
```

En GitHub: **Actions** → **Sync GCP credentials** → **Run workflow** → **Run workflow**.

Si sale verde: el archivo quedó en el contenedor como `/app/.env.gcp` y el contenedor se reinició.

---

## Paso 6 — Comprobar

1. Abre la app en el navegador.
2. Sidebar: **OpenAI ✅**, **BigQuery ✅**, **Histórico ✅**.
3. Pregunta: *¿Cuántos viajes en total hay?*

Si BigQuery sigue ❌, en el Droplet:

```bash
docker ps
# sustituye NOMBRE_CONTENEDOR
docker exec -it NOMBRE_CONTENEDOR sh -c 'test -f /app/.env.gcp && test -f /app/credentials/gcp-sa.json && echo OK'
docker logs NOMBRE_CONTENEDOR --tail 80
```

---

## Después de cada Redeploy en EasyPanel

Un redeploy **borra** `/app/.env.gcp` dentro del contenedor.

Vuelve a ejecutar: **Actions** → **Sync GCP credentials** → **Run workflow**.

### Opcional: que sobreviva al redeploy

En EasyPanel, monta volumen (si tu plan lo permite):

| Host | Contenedor |
|------|------------|
| `/opt/dp-agent-sql-ocean/gcp-runtime.env` | `/app/.env.gcp` |

El workflow ya deja el archivo en el host; con el volumen solo necesitas el workflow la **primera** vez (o al rotar la clave).

---

## Errores frecuentes

| Síntoma | Causa |
|---------|--------|
| `secret GCP_CREDENTIALS_B64 vacío` | No creaste el secret en GitHub |
| `no se encontró contenedor` | App parada o nombre distinto → define `DOCKER_CONTAINER_NAME` |
| SSH failed | Clave pública no en `authorized_keys` o IP/firewall |
| BigQuery ❌ tras redeploy | Vuelve a correr el workflow (paso anterior) |
