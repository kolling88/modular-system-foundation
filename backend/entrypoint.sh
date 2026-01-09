#!/bin/bash

set -e

# Aguardar o banco de dados estar pronto
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_SERVER 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Rodar migrações
echo "Running migrations..."
alembic upgrade head

# Rodar script de prestart (seed)
echo "Running prestart script..."
python app/prestart.py

# Iniciar a aplicação
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
