#!/bin/bash

# =====================================================
# Script de Activación del Entorno Virtual
# =====================================================
# Uso: source activate_env.sh
# =====================================================

echo "🚀 Activando entorno virtual de URLytics..."

# Detectar el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activar el entorno virtual
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "✅ Entorno virtual activado"
    echo ""
    echo "📦 Python: $(python --version)"
    echo "📦 Pip: $(pip --version)"
    echo ""
    echo "💡 Para desactivar: deactivate"
else
    echo "❌ Error: No se encontró el entorno virtual"
    echo "💡 Ejecuta: python -m venv venv"
fi
