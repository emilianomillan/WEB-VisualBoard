#!/bin/bash

echo "🚀 Iniciando Visual Board - Stack Completo..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend
echo -e "${YELLOW}📦 Iniciando Backend (FastAPI)...${NC}"
cd backend
source venv/bin/activate 2>/dev/null || {
    echo -e "${RED}⚠️  Creando entorno virtual...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

echo -e "${GREEN}✅ Backend iniciando en http://localhost:8000${NC}"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 3

# Frontend
echo -e "${YELLOW}🎨 Iniciando Frontend (React + Vite)...${NC}"
cd ../frontend

echo -e "${GREEN}✅ Frontend iniciando en http://localhost:5174${NC}"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✨ Visual Board está ejecutándose!${NC}"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:5174"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔍 Para verificar el estado:"
echo "   curl http://localhost:8000/health"
echo ""
echo -e "${YELLOW}Presiona CTRL+C para detener todos los servicios...${NC}"

# Función para limpiar al salir
cleanup() {
    echo ""
    echo -e "${RED}🛑 Deteniendo servicios...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Capturar CTRL+C
trap cleanup INT

# Esperar
wait