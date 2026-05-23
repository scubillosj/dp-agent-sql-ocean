# Este comando solo se instala si tienes python 3.11
pip install -U "langgraph-cli[inmem]"

# Corre el siguiente comando para lanzar LangGraph Studio
langgraph dev --allow-blocking

# Crear su Virtual Environment:
LangGraph-Agente-Texto-SQL

# Activa tu Virtual Environment:
conda activate LangGraph-Agente-Texto-SQL


# Deploy en DigitalOcean (recomendado: App Platform + GitHub)
# Guía paso a paso: ver DEPLOY-DIGITALOCEAN.md
# Secretos (OpenAI, GOOGLE_CREDENTIALS_JSON, Supabase) se configuran en el panel de DO, NO en GitHub Actions.

# Alternativa: imagen manual en Docker Hub
# docker login
# docker buildx build --platform linux/amd64 -t TU_USUARIO/citibike-agent:latest --push .

# Preguntas que le puedes hacer al agente:
- hola
- ¿Cuáles son las 10 rutas de bicicleta más populares, agrupando por estación de inicio y fin? Devuelve el nombre de la estación de inicio, el nombre de la estación de fin, un conteo de cuántos viajes se hicieron en esa ruta y la duración típica de esos viajes
- cuantos datos tienes, es decir cuantas filas.
- Cuantas de estos viajes inician y terminan en el mismo lugar