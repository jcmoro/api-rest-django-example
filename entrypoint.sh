#!/bin/sh
set -e

echo "📦 Iniciando contenedor Django API..."

# Esperar a la base de datos
echo "⏳ Esperando a la base de datos..."
until python -c "import psycopg2; psycopg2.connect(host='db', user='todo_user', password='todo_pass', dbname='todo_db')" 2>/dev/null; do
  echo "   Base de datos no lista, reintentando..."
  sleep 2
done

# Aplicar migraciones
echo "🔄 Ejecutando migraciones..."
python main.py migrate --noinput

# Recoger estáticos si procede
if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  echo "🗂  Recogiendo archivos estáticos..."
  python main.py collectstatic --noinput
fi

# Ejecutar tests si procede
if [ "$RUN_TESTS" = "1" ]; then
  echo "🧪 Ejecutando tests..."
  pytest -q
fi

# Ejecutar comando personalizado o servidor
if [ "$#" -gt 0 ]; then
  echo "⚙️  Ejecutando comando personalizado: $@"
  exec "$@"
else
  echo "🚀 Iniciando servidor Django en 0.0.0.0:8000"
  exec python main.py runserver 0.0.0.0:8000
fi
