# GitHub Actions — solo `GOOGLE_APPLICATION_CREDENTIALS`

Todo lo demás (**OpenAI**, **Supabase**, **`GOOGLE_CLOUD_PROJECT`**, etc.) va en el **`.env` de EasyPanel**, como en local.

## Secret de Google (en GitHub)

| Secret | Valor |
|--------|--------|
| `GOOGLE_APPLICATION_CREDENTIALS` | **Contenido completo** del JSON del service account (copiar/pegar el archivo entero) |

No es la ruta `credentials/...`; es el **texto del JSON**.

## Secrets para conectar al Droplet (SSH)

| Secret | Valor |
|--------|--------|
| `DROPLET_HOST` | IP del Droplet |
| `DROPLET_USER` | `root` |
| `DROPLET_SSH_KEY` | Clave privada SSH |
| `DOCKER_CONTAINER_NAME` | Nombre del contenedor (`docker ps`) |

## EasyPanel

En el `.env` del panel deja lo normal, por ejemplo:

```env
OPENAI_API_KEY=...
GOOGLE_CLOUD_PROJECT=datapath-prueba
GOOGLE_CLOUD_LOCATION=us-central1
DB_USER=postgres
...
```

**No pongas** en EasyPanel:

- `GOOGLE_APPLICATION_CREDENTIALS=...` (lo pone Actions en `/app/credentials/gcp-sa.json`)

## Ejecutar el workflow

1. `git push` (con el workflow en el repo).
2. GitHub → **Actions** → **Deploy Google credentials** → **Run workflow**.

## Subir cambios

```powershell
git add .github/workflows/deploy.yml scripts/bootstrap_env.py DEPLOY-GITHUB-ACTIONS.md
git commit -m "Actions: solo GOOGLE_APPLICATION_CREDENTIALS"
git push origin main
```
