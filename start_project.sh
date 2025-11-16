#!/bin/bash
# =====================================================
# 🛡️ SocialGuard - Script de Inicio del Proyecto Completo
# =====================================================
# Este script inicia todos los componentes del proyecto

set -e  # Salir si hay error

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            🛡️  SOCIALGUARD - INICIO DEL PROYECTO                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Directorio del proyecto
PROJECT_DIR="/home/huaritex/Desktop/social engineer"
cd "$PROJECT_DIR"

echo -e "${YELLOW}📍 Directorio del proyecto: $PROJECT_DIR${NC}\n"

# =====================================================
# PASO 1: Verificar entorno virtual
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 1: Verificando entorno virtual${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Entorno virtual encontrado${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Entorno virtual activado${NC}\n"
else
    echo -e "${RED}❌ No se encontró entorno virtual${NC}"
    echo -e "${YELLOW}💡 Ejecuta: python -m venv venv${NC}"
    exit 1
fi

# =====================================================
# PASO 2: Verificar modelo entrenado
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 2: Verificando modelo entrenado${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -f "phishing_model_artefacts/phishing_model_rf.joblib" ]; then
    echo -e "${GREEN}✅ Modelo encontrado${NC}"
    MODEL_SIZE=$(du -h phishing_model_artefacts/phishing_model_rf.joblib | cut -f1)
    echo -e "${GREEN}   📦 Tamaño: $MODEL_SIZE${NC}\n"
else
    echo -e "${RED}❌ Modelo no encontrado${NC}"
    echo -e "${YELLOW}💡 Ejecuta el notebook train.ipynb para entrenar el modelo${NC}"
    exit 1
fi

# =====================================================
# PASO 3: Detener API anterior (si existe)
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 3: Verificando API anterior${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if pgrep -f "python.*api.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  API ya está corriendo, deteniéndola...${NC}"
    pkill -f "python.*api.py"
    sleep 2
    echo -e "${GREEN}✅ API anterior detenida${NC}\n"
else
    echo -e "${GREEN}✅ No hay API corriendo${NC}\n"
fi

# =====================================================
# PASO 4: Iniciar API
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 4: Iniciando API Flask${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Iniciar API en background
nohup python api.py > api.log 2>&1 &
API_PID=$!

echo -e "${YELLOW}⏳ Esperando a que la API se inicie...${NC}"
sleep 4

# Verificar que la API está corriendo
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API iniciada correctamente (PID: $API_PID)${NC}"
    echo -e "${GREEN}   🌐 URL: http://localhost:5000${NC}\n"
else
    echo -e "${RED}❌ Error al iniciar la API${NC}"
    echo -e "${YELLOW}💡 Ver logs: tail -f api.log${NC}"
    exit 1
fi

# =====================================================
# PASO 5: Ejecutar pruebas
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 5: Ejecutando pruebas automáticas${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -f "test_api.py" ]; then
    echo -e "${YELLOW}🧪 Ejecutando test_api.py...${NC}\n"
    python test_api.py
    echo ""
else
    echo -e "${YELLOW}⚠️  test_api.py no encontrado, saltando pruebas${NC}\n"
fi

# =====================================================
# PASO 6: Abrir interfaz web
# =====================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PASO 6: Abriendo interfaz web${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -f "index.html" ]; then
    echo -e "${GREEN}✅ Interfaz web encontrada${NC}"
    
    # Intentar abrir en el navegador
    if command -v xdg-open > /dev/null 2>&1; then
        xdg-open "file://$PROJECT_DIR/index.html" 2>/dev/null &
        echo -e "${GREEN}✅ Interfaz web abierta en el navegador${NC}\n"
    elif command -v firefox > /dev/null 2>&1; then
        firefox "file://$PROJECT_DIR/index.html" 2>/dev/null &
        echo -e "${GREEN}✅ Interfaz web abierta en Firefox${NC}\n"
    elif command -v google-chrome > /dev/null 2>&1; then
        google-chrome "file://$PROJECT_DIR/index.html" 2>/dev/null &
        echo -e "${GREEN}✅ Interfaz web abierta en Chrome${NC}\n"
    else
        echo -e "${YELLOW}⚠️  No se pudo abrir automáticamente${NC}"
        echo -e "${YELLOW}💡 Abre manualmente: file://$PROJECT_DIR/index.html${NC}\n"
    fi
else
    echo -e "${YELLOW}⚠️  index.html no encontrado${NC}\n"
fi

# =====================================================
# RESUMEN FINAL
# =====================================================
echo -e "${GREEN}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          ✅ PROYECTO SOCIALGUARD INICIADO CORRECTAMENTE              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 ESTADO DEL PROYECTO${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${GREEN}✅ API Backend:${NC}"
echo -e "   🌐 http://localhost:5000"
echo -e "   📊 Health: http://localhost:5000/health"
echo -e "   📄 Info: http://localhost:5000/info"
echo -e "   🆔 PID: $API_PID\n"

echo -e "${GREEN}✅ Interfaz Web:${NC}"
echo -e "   📂 file://$PROJECT_DIR/index.html\n"

echo -e "${GREEN}✅ Modelo ML:${NC}"
echo -e "   📦 Modelo: phishing_model_rf.joblib ($MODEL_SIZE)"
echo -e "   🎯 Accuracy: 67.60%"
echo -e "   🎯 Precision: 100.00%\n"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔧 COMANDOS ÚTILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}# Ver logs de la API:${NC}"
echo -e "   tail -f api.log\n"

echo -e "${YELLOW}# Detener la API:${NC}"
echo -e "   kill $API_PID\n"

echo -e "${YELLOW}# Ejecutar pruebas:${NC}"
echo -e "   python test_api.py\n"

echo -e "${YELLOW}# Probar predicción:${NC}"
echo -e "   curl -X POST http://localhost:5000/predict \\"
echo -e "     -H 'Content-Type: application/json' \\"
echo -e "     -d '{\"text\": \"https://ejemplo.com\"}'\n"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${GREEN}🎉 ¡Proyecto listo para usar!${NC}\n"

# Guardar PID para detener después
echo $API_PID > .api.pid

echo -e "${YELLOW}💡 Para detener todo el proyecto:${NC}"
echo -e "   ./stop_project.sh\n"
