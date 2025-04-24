#!/usr/bin/env bash

# Salir si algo falla
set -o errexit

# Entrar a la carpeta del proyecto Django
cd sistema_reportes_ppda

# Instala las dependencias
pip install --upgrade pip
pip install -r ../requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput