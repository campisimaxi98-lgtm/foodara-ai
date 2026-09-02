#!/bin/bash

# FOODARA AI - Startup Script
# Script para iniciar FOODARA de manera rápida

set -e

echo "🚀 FOODARA AI - Iniciando..."
echo ""

# Verificar que .env exista
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📋 Copiando .env.example a .env..."
    cp .env.example .env
    echo "✅ Hecho. Edita .env con tus valores."
fi

# Opción 1: Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "🐳 Iniciando con Docker Compose..."
    docker compose up --build
else
    echo "📦 Docker no encontrado. Iniciando localmente..."
    
    # Verificar Python
    if ! command -v python3.12 &> /dev/null; then
        echo "❌ Python 3.12 no encontrado"
        exit 1
    fi
    
    # Crear venv si no existe
    if [ ! -d venv ]; then
        echo "🔧 Creando virtual environment..."
        python3.12 -m venv venv
    fi
    
    # Activar venv
    source venv/bin/activate
    
    # Instalar dependencias
    echo "📚 Instalando dependencias..."
    pip install -r requirements.txt
    
    # Verificar que PostgreSQL esté corriendo
    echo "🗄️  Verificando PostgreSQL..."
    
    # Iniciar servidor
    echo "🚀 Iniciando servidor FastAPI..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
