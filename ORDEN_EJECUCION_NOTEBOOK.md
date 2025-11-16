# 📋 Orden de Ejecución del Notebook - URLytics Training

## 🎯 **Guía de Ejecución Correcta**

Este documento explica el **orden correcto** para ejecutar las celdas del notebook `train.ipynb` y las dependencias entre ellas.

---

## ⚠️ **IMPORTANTE: Error Común**

**❌ ERROR MÁS FRECUENTE:**
```python
NameError: name 'y_train' is not defined
```

**Causa:** Intentar ejecutar la celda de entrenamiento (Cell 7) sin haber ejecutado primero la celda de preprocesamiento (Cell 4).

**Solución:** Seguir el orden de ejecución descrito a continuación.

---

## ✅ **Orden de Ejecución Correcto**

### **1️⃣ Cell 1: Setup y Configuración de Kaggle**
**Propósito:** Configurar el entorno de trabajo

**Acciones:**
- ✅ Instala/verifica librerías necesarias
- ✅ Configura Kaggle API con `kaggle.json`
- ✅ Establece permisos de archivos

**Variables creadas:** Ninguna

**Dependencias:** Ninguna

**Tiempo estimado:** 5-10 segundos

---

### **2️⃣ Cell 2: Carga y Combinación de Datasets**
**Propósito:** Descargar y combinar datasets de phishing

**Acciones:**
- ✅ Descarga 2 datasets de Kaggle
- ✅ Combina múltiples fuentes de datos
- ✅ Elimina duplicados

**Variables creadas:**
- `df_total` - DataFrame combinado (~98K filas)
- `df_alt` - Dataset 1 de Kaggle
- `df_orig` - Dataset 2 de Kaggle

**Dependencias:** Cell 1 (requiere Kaggle configurado)

**Tiempo estimado:** 20-60 segundos (depende de conexión)

---

### **3️⃣ Cell 4: Preprocesamiento y División de Datos** ⚠️ **CRÍTICA**
**Propósito:** Preparar datos para entrenamiento

**Acciones:**
- ✅ Limpia valores `-1` del target
- ✅ Divide datos en Train/Val/Test (70/15/15)
- ✅ Normaliza features con StandardScaler
- ✅ Valida que target solo tenga valores 0 y 1

**Variables creadas:** ⭐ **IMPORTANTE**
- `X_train`, `y_train` - Datos de entrenamiento (65K muestras)
- `X_val`, `y_val` - Datos de validación (14K muestras)
- `X_test`, `y_test` - Datos de test (14K muestras)
- `X_train_scaled`, `X_val_scaled`, `X_test_scaled` - Datos normalizados
- `scaler` - StandardScaler entrenado
- `FEATURES` - Lista de features utilizadas

**Dependencias:** Cell 2 (requiere `df_total`)

**Tiempo estimado:** 5-10 segundos

**⚠️ NOTA CRÍTICA:** Esta celda es **OBLIGATORIA** antes de ejecutar celdas posteriores.

---

### **4️⃣ Cell 6: Validaciones Anti-Leakage**
**Propósito:** Verificar calidad de los datos

**Acciones:**
- ✅ Verifica no haya data leakage
- ✅ Detecta drift entre conjuntos
- ✅ Valida estratificación
- ✅ Analiza correlaciones feature-target

**Variables creadas:** Ninguna (solo validaciones)

**Dependencias:** Cell 4 (requiere todas las variables de train/val/test)

**Tiempo estimado:** 3-5 segundos

---

### **5️⃣ Cell 7: Entrenamiento del Modelo**
**Propósito:** Entrenar y evaluar RandomForest

**Acciones:**
- ✅ Entrena RandomForest (100 estimadores)
- ✅ Evalúa en Validation y Test
- ✅ Genera visualizaciones (Confusion Matrix, ROC, etc.)
- ✅ Calcula métricas (Accuracy, Precision, Recall, F1, ROC-AUC)

**Variables creadas:**
- `model` - RandomForestClassifier entrenado
- `training_time` - Tiempo de entrenamiento
- `val_accuracy`, `val_precision`, `val_recall`, `val_f1`, `val_roc_auc` - Métricas de validación
- `test_accuracy`, `test_precision`, `test_recall`, `test_f1`, `test_roc_auc` - Métricas de test
- `feature_importance` - DataFrame con importancia de features

**Dependencias:** Cell 4 (requiere `X_train_scaled`, `y_train`, etc.)

**Tiempo estimado:** 5-15 segundos

---

### **6️⃣ Cell 9: Guardado de Artefactos**
**Propósito:** Exportar modelo y archivos para producción

**Acciones:**
- ✅ Guarda modelo entrenado (`.joblib`)
- ✅ Guarda scaler (`.joblib`)
- ✅ Exporta features (`.json`)
- ✅ Guarda métricas (`.json`)
- ✅ Exporta parámetros para TensorFlow.js

**Archivos creados:**
- `phishing_model_artefacts/phishing_model_rf.joblib`
- `phishing_model_artefacts/scaler.joblib`
- `phishing_model_artefacts/features.json`
- `phishing_model_artefacts/model_metrics.json`
- `phishing_model_artefacts/scaler_params.json`

**Dependencias:** Cell 7 (requiere `model`, `scaler`, métricas)

**Tiempo estimado:** 2-5 segundos

---

### **7️⃣ Cell 11: Baseline para Drift Monitoring**
**Propósito:** Crear archivos para monitoreo en producción

**Acciones:**
- ✅ Guarda estadísticas baseline
- ✅ Genera código de monitoreo de drift

**Archivos creados:**
- `phishing_model_artefacts/baseline_statistics.json`
- `phishing_model_artefacts/drift_monitoring_example.py`

**Dependencias:** Cell 7 (requiere `X_train`, `y_train`, modelo)

**Tiempo estimado:** 1-2 segundos

---

### **8️⃣ Cell 12: Resumen Final** (Opcional - Solo para Colab)
**Propósito:** Descargar archivos en Google Colab

**Acciones:**
- ⚠️ Intenta descargar archivos con `files.download()`
- ℹ️ **NO funciona en Jupyter local** (solo Colab)

**Dependencias:** Cell 9 y Cell 11

**Tiempo estimado:** Variable

**Nota:** Si trabajas en Jupyter local, omite esta celda o modifica para no usar `files.download()`.

---

## 📊 **Diagrama de Flujo de Ejecución**

```
┌─────────────────────────────────────────────────────────┐
│ Cell 1: Setup                                           │
│ ├─ Instala librerías                                    │
│ └─ Configura Kaggle                                     │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Cell 2: Carga Datasets                                  │
│ ├─ Descarga de Kaggle                                   │
│ └─ Crea: df_total                                       │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Cell 4: Preprocesamiento ⭐ CRÍTICA                     │
│ ├─ Limpia datos                                         │
│ ├─ Divide Train/Val/Test                                │
│ ├─ Normaliza con StandardScaler                         │
│ └─ Crea: X_train, y_train, X_val, y_val, X_test, y_test│
└────────────────┬───────────────────┬────────────────────┘
                 ↓                   ↓
    ┌────────────────────┐  ┌───────────────────────────┐
    │ Cell 6: Validación │  │ Cell 7: Entrenamiento     │
    │ ├─ Anti-leakage    │  │ ├─ Train RandomForest     │
    │ └─ Drift detection │  │ ├─ Evalúa modelo          │
    └────────────────────┘  │ └─ Crea: model, métricas  │
                            └─────┬─────────────────────┘
                                  ↓
                    ┌─────────────────────────────────┐
                    │ Cell 9: Guardar Artefactos      │
                    │ └─ Exporta modelo + scaler      │
                    └───────┬─────────────────────────┘
                            ↓
                    ┌─────────────────────────────────┐
                    │ Cell 11: Baseline Drift         │
                    │ └─ Estadísticas para producción │
                    └─────────────────────────────────┘
```

---

## 🔄 **Dependencias entre Celdas**

| Celda | Requiere | Crea Variables |
|-------|----------|----------------|
| Cell 1 | - | Configuración |
| Cell 2 | Cell 1 | `df_total` |
| Cell 4 | Cell 2 | `X_train`, `y_train`, `X_val`, `y_val`, `X_test`, `y_test`, `scaler`, `FEATURES` |
| Cell 6 | Cell 4 | Validaciones (sin variables) |
| Cell 7 | Cell 4 | `model`, `training_time`, todas las métricas, `feature_importance` |
| Cell 9 | Cell 7 | Archivos exportados |
| Cell 11 | Cell 7 | Archivos baseline |
| Cell 12 | Cell 9, 11 | - |

---

## 🚨 **Errores Comunes y Soluciones**

### **Error 1: `NameError: name 'y_train' is not defined`**

**Causa:** Ejecutaste Cell 7 sin ejecutar Cell 4

**Solución:**
1. Ejecuta Cell 1
2. Ejecuta Cell 2
3. Ejecuta **Cell 4** ← IMPORTANTE
4. Luego ejecuta Cell 7

---

### **Error 2: `ValueError: Target is multiclass but average='binary'`**

**Causa:** El target tiene valores `-1`, `0`, `1` en lugar de solo `0`, `1`

**Solución:** Ejecuta Cell 4 completa (ya incluye limpieza de valores `-1`)

---

### **Error 3: `FileNotFoundError: [Errno 2] No such file or directory: 'kaggle.json'`**

**Causa:** No existe el archivo `kaggle.json`

**Solución:**
1. Descarga `kaggle.json` desde https://www.kaggle.com/
2. Colócalo en el directorio del notebook O en `~/.kaggle/`
3. Ejecuta Cell 1 nuevamente

---

### **Error 4: `ModuleNotFoundError: No module named 'kagglehub'`**

**Causa:** Librerías no instaladas

**Solución:** Cell 1 debería instalarlas automáticamente. Si no, ejecuta:
```bash
pip install kagglehub pandas scikit-learn joblib seaborn matplotlib scipy
```

---

## ⏱️ **Tiempo Total de Ejecución**

| Etapa | Tiempo Estimado |
|-------|-----------------|
| Cell 1: Setup | 5-10 seg |
| Cell 2: Carga datos | 20-60 seg |
| Cell 4: Preprocesamiento | 5-10 seg |
| Cell 6: Validaciones | 3-5 seg |
| Cell 7: Entrenamiento | 5-15 seg |
| Cell 9: Guardar modelo | 2-5 seg |
| Cell 11: Baseline | 1-2 seg |
| **TOTAL** | **~1-2 minutos** |

---

## 📦 **Archivos Generados**

Al finalizar la ejecución completa, tendrás estos archivos en `phishing_model_artefacts/`:

```
phishing_model_artefacts/
├── phishing_model_rf.joblib       # Modelo entrenado (RandomForest)
├── scaler.joblib                   # StandardScaler para normalización
├── features.json                   # Lista de features utilizadas
├── model_metrics.json              # Métricas de evaluación completas
├── scaler_params.json              # Parámetros para TensorFlow.js
├── baseline_statistics.json        # Estadísticas para monitoreo de drift
└── drift_monitoring_example.py     # Código de ejemplo para producción
```

---

## 💡 **Recomendaciones**

1. ✅ **Ejecuta siempre en orden** - No saltes celdas
2. ✅ **Verifica outputs** - Lee los mensajes de cada celda
3. ✅ **Guarda el notebook** - Después de cada ejecución exitosa
4. ✅ **Backup de artefactos** - Copia `phishing_model_artefacts/` a un lugar seguro
5. ⚠️ **No elimines variables** - Mantén el kernel vivo durante toda la sesión
6. ⚠️ **Cell 4 es crítica** - Sin ella, nada funciona después

---

## 🔍 **Verificación de Estado**

Para verificar si ejecutaste correctamente hasta cierto punto:

```python
# Verificar después de Cell 2
print("df_total" in dir())  # Debe ser True

# Verificar después de Cell 4
print("y_train" in dir())   # Debe ser True
print("scaler" in dir())    # Debe ser True

# Verificar después de Cell 7
print("model" in dir())     # Debe ser True
print(hasattr(model, 'feature_importances_'))  # Debe ser True
```

---

## 📚 **Referencias**

- **Notebook:** `train.ipynb`
- **Proyecto:** URLytics - Phishing Detection
- **Autor:** URLytics Team
- **Versión:** 2.0
- **Fecha:** Noviembre 2025

---

## 🆘 **Soporte**

Si encuentras problemas:

1. Revisa este documento
2. Lee los mensajes de error cuidadosamente
3. Verifica que ejecutaste todas las celdas en orden
4. Reinicia el kernel y ejecuta todo de nuevo si es necesario

---

**✅ Última actualización:** 15 de Noviembre, 2025
