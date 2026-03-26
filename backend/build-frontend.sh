#!/bin/bash

# Build do frontend para Render
echo "🚀 Iniciando build do frontend..."

# Entrar na pasta do frontend
cd frontend

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

# Build do frontend
echo "🔨 Buildando frontend..."
npm run build

# Verificar se o build foi criado
if [ -d "dist" ]; then
    echo "✅ Frontend buildado com sucesso!"
    echo "📁 Arquivos em frontend/dist:"
    ls -la dist/
else
    echo "❌ Erro: Frontend não foi buildado"
    exit 1
fi

echo "🎉 Build do frontend finalizado!"
