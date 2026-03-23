#!/bin/bash

# Script de build para Render - Backend + Frontend

echo "🚀 Iniciando build completo..."

# Build do Frontend
echo "📦 Building frontend..."
cd ../frontend
npm install
npm run build
cd ../backend

# Verificar se o build foi criado
if [ -d "static" ]; then
    echo "✅ Frontend buildado com sucesso!"
    echo "📁 Arquivos em static:"
    ls -la static/
else
    echo "❌ Erro: Frontend não foi buildado"
    exit 1
fi

echo "🎉 Build completo finalizado!"
