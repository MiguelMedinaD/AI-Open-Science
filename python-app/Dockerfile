FROM python:3.8-slim

WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script principal
# COPY keyword_cloud_generator.py .

# El contenedor se ejecutará con el comando definido en el docker-compose