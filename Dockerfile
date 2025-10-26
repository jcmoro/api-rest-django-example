# Imagen base ligera y rápida
FROM python:3.11-alpine

# Evita la creación de archivos pyc y buffers en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev bash

# Copia dependencias e instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . /app/

# 🔑 Da permisos de ejecución al script de entrada
RUN chmod +x /app/entrypoint.sh

# Define el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
