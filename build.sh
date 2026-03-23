#!/bin/bash

# Script de build para Render - Backend + Frontend

echo "🚀 Iniciando build completo..."

# Descobrir onde estamos
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📍 Script directory: $SCRIPT_DIR"

# Instalar dependências do backend
echo "📦 Installing backend dependencies..."
pip install --no-cache-dir -r "$SCRIPT_DIR/backend/requirements.txt"

# Build do Frontend
echo "📦 Building frontend..."
cd "$SCRIPT_DIR/frontend"
npm ci --silent
npm run build
cd "$SCRIPT_DIR"

# Verificar se o build foi criado
if [ -d "$SCRIPT_DIR/backend/static" ]; then
echo "✅ Frontend buildado com sucesso!"
echo "📁 Arquivos em backend/static:"
ls -la "$SCRIPT_DIR/backend/static/"
else
echo "❌ Erro: Frontend não foi buildado"
exit 1
fi

echo "🎉 Build completo finalizado!"
