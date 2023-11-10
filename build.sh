#!/bin/bash

echo "Iniciando o processo de build..."

echo "Criando ambiente virtual!"

python -m venv venv
source venv/bin/activate

echo "Instalando as dependências..."

pip install --upgrade pip
pip install -r requirements.txt

echo "Build concluído com sucesso!"
