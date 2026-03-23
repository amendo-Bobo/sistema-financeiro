#!/bin/bash

# Script de build para Render - Backend + Frontend

echo "🚀 Iniciando build completo..."

# Instalar dependências do backend
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Build do Frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Verificar se o build foi criado
if [ -d "backend/static" ]; then
    echo "✅ Frontend buildado com sucesso!"
    echo "📁 Arquivos em backend/static:"
    ls -la backend/static/
else
    echo "❌ Erro: Frontend não foi buildado"
    exit 1
fi

echo "🎉 Build completo finalizado!"
