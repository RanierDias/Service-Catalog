#!/bin/bash

echo "Iniciando o processo de build..."

echo "Criando ambiente virtual!"

python -m venv venv
source venv/bin/activate

echo "Instalando as dependências..."

pip install -r requirements.txt

echo "Iniciando servidor wsgi!"

gunicorn 'wsgi:run_app()'

echo "Build concluído com sucesso!"
