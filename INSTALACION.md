# 📦 Guía de Instalación - SocialGuard ML v2.0

## ✅ Instalación Completada

¡Todas las librerías necesarias han sido instaladas exitosamente! 🎉

---

## 🔧 Configuración del Entorno

### 1️⃣ Entorno Virtual Creado

Se ha creado un entorno virtual en:
```
/home/huaritex/Desktop/social engineer/venv/
```

### 2️⃣ Librerías Instaladas

✅ **Core ML Libraries:**
- scikit-learn 1.7.2
- numpy 2.3.4
- pandas 2.3.3
- scipy 1.16.3

✅ **Model Persistence:**
- joblib 1.5.2

✅ **Data Acquisition:**
- kagglehub 0.3.13

✅ **Visualization:**
- matplotlib 3.10.7
- seaborn 0.13.2

✅ **API / Web Framework:**
- flask 3.1.2
- flask-cors 6.0.1

✅ **Jupyter Notebook:**
- jupyter 1.1.1
- notebook 7.4.7
- ipykernel 7.1.0
- jupyterlab 4.4.10

✅ **Development Tools:**
- pytest 9.0.1
- black 25.11.0
- flake8 7.3.0

---

## 🚀 Cómo Usar el Entorno Virtual

### Opción 1: Script de Activación (Recomendado)

```bash
cd "/home/huaritex/Desktop/social engineer"
source activate_env.sh
```

### Opción 2: Activación Manual

```bash
cd "/home/huaritex/Desktop/social engineer"
source venv/bin/activate
```

### Verificar Activación

Cuando el entorno esté activado, verás `(venv)` al inicio de tu prompt:

```bash
(venv) usuario@host:~/Desktop/social engineer$
```

### Desactivar el Entorno

```bash
deactivate
```

---

## 📓 Ejecutar el Notebook

### Opción 1: VS Code

1. Abrir `train.ipynb` en VS Code
2. Seleccionar el kernel del entorno virtual:
   - Click en "Select Kernel" (arriba a la derecha)
   - Elegir: `Python 3.13.x ('venv': venv)`
3. Ejecutar las celdas

### Opción 2: Jupyter Notebook

```bash
source venv/bin/activate
jupyter notebook train.ipynb
```

### Opción 3: JupyterLab

```bash
source venv/bin/activate
jupyter lab
```

---

## 🧪 Verificar Instalación

Ejecuta este comando para verificar que todo esté instalado:

```bash
source venv/bin/activate
python -c "
import sklearn
import numpy as np
import pandas as pd
import scipy
import joblib
import matplotlib
import seaborn as sns
import flask

print('✅ Todas las librerías importadas correctamente!')
print(f'scikit-learn: {sklearn.__version__}')
print(f'numpy: {np.__version__}')
print(f'pandas: {pd.__version__}')
print(f'scipy: {scipy.__version__}')
"
```

**Salida esperada:**
```
✅ Todas las librerías importadas correctamente!
scikit-learn: 1.7.2
numpy: 2.3.4
pandas: 2.3.3
scipy: 1.16.3
```

---

## 🐍 Ejecutar Scripts Python

Con el entorno activado:

```bash
# Activar entorno
source venv/bin/activate

# Ejecutar script de drift monitoring
python drift_monitoring_example.py

# Ejecutar API
python api.py

# Ejecutar tests (si tienes)
pytest
```

---

## 📦 Gestión de Paquetes

### Instalar paquetes adicionales:

```bash
source venv/bin/activate
pip install nombre-del-paquete
```

### Actualizar requirements.txt:

```bash
source venv/bin/activate
pip freeze > requirements.txt
```

### Reinstalar todo desde requirements.txt:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Actualizar Paquetes

Para actualizar todas las librerías a sus últimas versiones:

```bash
source venv/bin/activate
pip install --upgrade scikit-learn numpy pandas scipy matplotlib seaborn flask
```

---

## 🛠️ Solución de Problemas

### Problema: "No module named 'sklearn'"

**Solución:**
```bash
source venv/bin/activate
pip install scikit-learn
```

### Problema: "Jupyter kernel not found"

**Solución:**
```bash
source venv/bin/activate
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

### Problema: "Permission denied" al ejecutar activate_env.sh

**Solución:**
```bash
chmod +x activate_env.sh
source activate_env.sh
```

### Problema: El entorno no se activa

**Solución:**
```bash
# Recrear el entorno virtual
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Siguiente Paso

Ahora que tienes todo instalado, puedes:

1. **Ejecutar el notebook mejorado:**
   ```bash
   source venv/bin/activate
   jupyter notebook train.ipynb
   ```

2. **Leer la documentación:**
   - [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Guía rápida
   - [ML_BEST_PRACTICES.md](ML_BEST_PRACTICES.md) - Mejores prácticas
   - [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - Resumen de mejoras

3. **Ejecutar validaciones:**
   - El notebook ejecutará automáticamente las 4 validaciones anti-leakage

---

## 💡 Tips Útiles

### Alias para activación rápida

Agrega esto a tu `~/.zshrc` o `~/.bashrc`:

```bash
alias socialguard='cd "/home/huaritex/Desktop/social engineer" && source venv/bin/activate'
```

Luego solo ejecuta:
```bash
socialguard
```

### Verificar qué Python está usando

```bash
which python
# Debe mostrar: /home/huaritex/Desktop/social engineer/venv/bin/python
```

### Ver paquetes instalados

```bash
source venv/bin/activate
pip list
```

### Limpiar cache de pip

```bash
pip cache purge
```

---

## 🎯 Checklist de Instalación

- [x] Entorno virtual creado
- [x] Pip actualizado
- [x] Todas las librerías instaladas
- [x] Script de activación creado
- [x] Requirements.txt generado
- [ ] Verificación de imports ejecutada
- [ ] Jupyter kernel configurado (opcional)
- [ ] Notebook ejecutado exitosamente

---

## 📞 Soporte

Si encuentras algún problema:

1. Verifica que el entorno virtual esté activado
2. Consulta la sección "Solución de Problemas" arriba
3. Revisa los logs de instalación
4. Abre un issue en GitHub con el error completo

---

## 🔐 Seguridad

El entorno virtual está aislado del sistema:
- ✅ No afecta paquetes del sistema
- ✅ No requiere permisos de administrador
- ✅ Fácil de eliminar si es necesario

Para eliminar completamente:
```bash
rm -rf venv
```

---

## 📊 Resumen de Comandos

```bash
# Activar entorno
source venv/bin/activate

# Verificar instalación
python -c "import sklearn, numpy, pandas; print('OK')"

# Ejecutar notebook
jupyter notebook train.ipynb

# Ejecutar script
python drift_monitoring_example.py

# Desactivar
deactivate
```

---

**¡Listo para entrenar tu modelo! 🚀**

Ejecuta:
```bash
source venv/bin/activate
jupyter notebook train.ipynb
```

---

**Versión:** 2.0  
**Fecha:** 2025-11-15  
**Sistema:** Linux (Arch)  
**Python:** 3.13
