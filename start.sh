#!/bin/bash

echo "🚀 Iniciando Visual Board..."
echo ""

# Frontend
echo "📦 Instalando dependencias del frontend..."
cd frontend
npm install

echo "✅ Frontend listo"
echo ""

# Iniciar frontend
echo "🎨 Iniciando frontend en http://localhost:5173..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✨ Visual Board está ejecutándose!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo ""
echo "⚠️  NOTA: El backend necesita Python 3.11 o menor (no funciona con Python 3.13)"
echo "Para iniciar el backend manualmente:"
echo "  cd backend"
echo "  python3.11 -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  uvicorn main:app --reload"
echo ""
echo "Presiona CTRL+C para detener..."

# Esperar
wait $FRONTEND_PID