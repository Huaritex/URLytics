#!/bin/bash
# =====================================================
# 🛡️ URLytics - Script para Detener el Proyecto
# =====================================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           🛑 DETENIENDO PROYECTO URLYTICS                        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Directorio del proyecto
PROJECT_DIR="/home/huaritex/Desktop/social engineer"
cd "$PROJECT_DIR"

# =====================================================
# Detener API usando PID guardado
# =====================================================
if [ -f ".api.pid" ]; then
    API_PID=$(cat .api.pid)
    echo -e "${YELLOW}🔍 Deteniendo API (PID: $API_PID)...${NC}"
    
    if kill -0 $API_PID 2>/dev/null; then
        kill $API_PID
        sleep 2
        
        # Verificar que se detuvo
        if kill -0 $API_PID 2>/dev/null; then
            echo -e "${RED}⚠️  API no respondió a SIGTERM, usando SIGKILL...${NC}"
            kill -9 $API_PID
        fi
        
        echo -e "${GREEN}✅ API detenida${NC}"
        rm .api.pid
    else
        echo -e "${YELLOW}⚠️  API ya no está corriendo (PID: $API_PID)${NC}"
        rm .api.pid
    fi
else
    echo -e "${YELLOW}⚠️  Archivo .api.pid no encontrado${NC}"
fi

# =====================================================
# Buscar y detener cualquier proceso de api.py
# =====================================================
echo -e "${YELLOW}🔍 Buscando procesos de api.py...${NC}"

if pgrep -f "python.*api.py" > /dev/null; then
    echo -e "${YELLOW}⏳ Deteniendo todos los procesos de api.py...${NC}"
    pkill -f "python.*api.py"
    sleep 2
    echo -e "${GREEN}✅ Procesos de api.py detenidos${NC}"
else
    echo -e "${GREEN}✅ No hay procesos de api.py corriendo${NC}"
fi

# =====================================================
# Verificación final
# =====================================================
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}VERIFICACIÓN FINAL${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Intentar conectar a la API
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${RED}❌ La API todavía responde en el puerto 5000${NC}"
    echo -e "${YELLOW}💡 Intenta: sudo lsof -i :5000${NC}\n"
else
    echo -e "${GREEN}✅ API completamente detenida${NC}\n"
fi

echo -e "${GREEN}🎉 Proyecto URLytics detenido correctamente${NC}\n"

# =====================================================
# Información adicional
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}💡 COMANDOS ÚTILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}# Ver logs de la última ejecución:${NC}"
echo -e "   tail -50 api.log\n"

echo -e "${YELLOW}# Limpiar logs:${NC}"
echo -e "   > api.log\n"

echo -e "${YELLOW}# Reiniciar el proyecto:${NC}"
echo -e "   ./start_project.sh\n"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
