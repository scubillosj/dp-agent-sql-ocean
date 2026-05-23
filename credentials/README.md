# Carpeta de credenciales (solo local)

Coloca aquí el JSON de tu **service account** de Google Cloud.

Ejemplo de nombre: `datapath-prueba-0e2600ec5dc4.json`

En tu `.env`:

```env
GOOGLE_APPLICATION_CREDENTIALS=credentials/tu-archivo.json
```

**No subas archivos `.json` a Git.** Esta carpeta está ignorada por `.gitignore`.
