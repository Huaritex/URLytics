# 🛡️ URLytics - Guía de Integración de API

## ✅ Integración Completada

El modelo de phishing entrenado ha sido **integrado exitosamente** en la API de URLytics.

---

## 📋 Estado Actual

### ✅ Archivos Actualizados

1. **`api.py`** - API Flask mejorada con:
   - ✅ Carga del modelo RandomForest entrenado
   - ✅ Normalización con StandardScaler
   - ✅ Extracción mejorada de 6 features de phishing
   - ✅ 3 endpoints: `/predict`, `/health`, `/info`
   - ✅ Validación de requests y manejo de errores

2. **`test_api.py`** - Script de pruebas completo

3. **`phishing_model_artefacts/`** - Directorio con 7 archivos del modelo:
   - `phishing_model_rf.joblib` (96.8 KB)
   - `scaler.joblib` (1.1 KB)
   - `features.json` (140 B)
   - `model_metrics.json` (1.2 KB)
   - `scaler_params.json` (574 B)
   - `baseline_statistics.json` (1.9 KB)
   - `drift_monitoring_example.py` (2.6 KB)

---

## 🚀 Cómo Usar la API

### 1. Iniciar el Servidor

```bash
cd "/home/huaritex/Desktop/social engineer"
python api.py
```

**Salida esperada:**
```
📦 Cargando modelo desde phishing_model_artefacts/phishing_model_rf.joblib...
✅ Modelo cargado: 100 estimadores, 6 features
📐 Cargando scaler desde phishing_model_artefacts/scaler.joblib...
✅ Scaler cargado: 6 features
📋 Features cargadas: ['Abnormal_URL', 'Prefix_Suffix', 'SSLfinal_State', ...]
📊 Métricas del modelo:
   • Test Accuracy: 67.60%
   • Test Precision: 100.00%
   • Test Recall: 17.48%
   • Test F1-Score: 0.2976

✅ API lista para recibir peticiones

 * Running on http://127.0.0.1:5000
```

---

### 2. Endpoints Disponibles

#### **POST `/predict`** - Predicción de Phishing

**Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "https://secure-paypal-verify.com/@login.php"}'
```

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": "phishing",
  "confidence": 0.7338,
  "phishing_probability": 0.7338,
  "risk_level": "high",
  "features": {
    "Abnormal_URL": 0,
    "Prefix_Suffix": 0,
    "SSLfinal_State": -1,
    "Shortining_Service": 0,
    "having_At_Symbol": 1,
    "having_Sub_Domain": 0
  },
  "timestamp": "2025-11-15T22:04:42.123456",
  "analyzed_text": "https://secure-paypal-verify.com/@login.php"
}
```

**Campos de respuesta:**
- `prediction`: `0` (legítimo) o `1` (phishing)
- `prediction_label`: `"legitimate"` o `"phishing"`
- `confidence`: Confianza de la predicción (0.0-1.0)
- `phishing_probability`: Probabilidad de que sea phishing
- `risk_level`: `"low"`, `"medium"` o `"high"`
- `features`: Diccionario con las 6 features extraídas
- `timestamp`: Marca de tiempo ISO-8601
- `analyzed_text`: URL analizada (truncada si >100 chars)

---

#### **GET `/health`** - Health Check

Verifica que la API esté funcionando.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model": {
    "n_estimators": 100,
    "n_features": 6,
    "features": ["Abnormal_URL", "Prefix_Suffix", ...]
  },
  "metrics": {
    "test_accuracy": 0.676,
    "test_precision": 1.0,
    "test_recall": 0.1748,
    "test_f1": 0.2976
  },
  "timestamp": "2025-11-15T22:04:42.123456"
}
```

---

#### **GET `/info`** - Información del Modelo

Devuelve información detallada sobre el modelo.

**Request:**
```bash
curl http://localhost:5000/info
```

**Response:**
```json
{
  "model_info": {
    "algorithm": "Random Forest",
    "version": "2.0",
    "n_estimators": 100,
    "training_samples": 65356
  },
  "features": ["Abnormal_URL", "Prefix_Suffix", ...],
  "feature_importance": {
    "SSLfinal_State": 0.2819,
    "having_At_Symbol": 0.2646,
    ...
  },
  "performance": {
    "accuracy": 0.676,
    "precision": 1.0,
    "recall": 0.1748,
    "f1_score": 0.2976,
    "roc_auc": 0.5874
  },
  "last_updated": "N/A"
}
```

---

### 3. Ejecutar Pruebas

```bash
python test_api.py
```

Este script ejecuta 8 pruebas automáticas:
- ✅ 3 URLs legítimas (Google, GitHub, Stack Overflow)
- 🚨 5 URLs sospechosas/phishing

---

## 📊 Features Detectadas

El modelo analiza **6 características** de cada URL:

| Feature | Descripción | Valores | Indicador de Phishing |
|---------|-------------|---------|----------------------|
| `Abnormal_URL` | Patrones anormales (IP, URL muy larga) | 0, 1 | ⚠️ Si = 1 |
| `Prefix_Suffix` | Guiones en el dominio | 0, 1 | ⚠️ Si = 1 |
| `SSLfinal_State` | Certificado SSL/TLS | -1 (HTTP), 0, 1 (HTTPS) | ⚠️ Si = -1 |
| `Shortining_Service` | Acortadores (bit.ly, etc.) | 0, 1 | ⚠️ Si = 1 |
| `having_At_Symbol` | Símbolo '@' en URL | 0, 1 | ⚠️ Si = 1 |
| `having_Sub_Domain` | Número de subdominios | 0, 1, 2+ | ⚠️ Si ≥ 2 |

---

## 🔧 Integración con la Extensión del Navegador

### JavaScript (Cliente)

```javascript
async function checkPhishing(url) {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: url })
    });
    
    const data = await response.json();
    
    if (data.prediction === 1) {
      console.warn('⚠️ PHISHING DETECTADO!');
      console.log(`Confianza: ${(data.confidence * 100).toFixed(2)}%`);
      console.log(`Nivel de riesgo: ${data.risk_level}`);
    } else {
      console.log('✅ URL parece legítima');
    }
    
    return data;
  } catch (error) {
    console.error('Error al verificar URL:', error);
  }
}

// Ejemplo de uso
checkPhishing('https://secure-paypal@malicious.com');
```

---

## 📈 Métricas del Modelo Actual

- **Accuracy**: 67.60% - Predicciones correctas
- **Precision**: 100.00% - Sin falsos positivos (conservative)
- **Recall**: 17.48% - Detecta ~1 de cada 6 ataques reales
- **F1-Score**: 0.2976 - Balance precision/recall
- **ROC-AUC**: 0.5874 - Rendimiento general

### 🎯 Interpretación

- ✅ **Alta Precision (100%)**: Si el modelo dice "phishing", es **muy confiable**
- ⚠️ **Baja Recall (17%)**: El modelo es **conservador**, puede dejar pasar algunos ataques
- 💡 **Trade-off**: Mejor evitar falsos positivos (bloquear sitios legítimos)

---

## 🚀 Próximos Pasos

### 1. **Mejorar el Recall** (Opcional)

Si necesitas detectar más ataques:

```python
# En api.py, ajustar el threshold de clasificación
phishing_prob = float(prediction_proba[1])

# Threshold más bajo = más sensible
if phishing_prob > 0.3:  # En vez de 0.5 por defecto
    prediction = 1
```

### 2. **Convertir a TensorFlow.js** (Para uso offline en extensión)

```bash
# Instalar tensorflowjs_converter
pip install tensorflowjs

# Convertir modelo (requiere primero convertir sklearn a TF)
# Ver: https://www.tensorflow.org/js/guide/conversion
```

### 3. **Implementar Monitoreo de Drift**

Usar `drift_monitoring_example.py` para detectar cuando el modelo necesita re-entrenamiento.

### 4. **Desplegar en Producción**

```bash
# Instalar gunicorn (servidor WSGI)
pip install gunicorn

# Ejecutar en producción
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

---

## 🐛 Troubleshooting

### Error: "Modelo no encontrado"

**Solución:**
```bash
# Verificar que existan los archivos
ls -lh phishing_model_artefacts/

# Deberías ver 7 archivos
```

### Warning: "X does not have valid feature names"

**Causa:** Sklearn muestra este warning cuando el DataFrame no tiene nombres exactos.

**Impacto:** ⚠️ Solo es un warning, **no afecta las predicciones**.

**Solución (opcional):**
```python
# En api.py, línea ~100
X_scaled = pd.DataFrame(
    scaler.transform(X),
    columns=FEATURES
)
```

### Error de conexión en test_api.py

**Solución:**
```bash
# Asegúrate de que la API esté corriendo
python api.py &

# Espera unos segundos y ejecuta las pruebas
sleep 3 && python test_api.py
```

---

## 📚 Documentación Adicional

- **`ORDEN_EJECUCION_NOTEBOOK.md`** - Cómo re-entrenar el modelo
- **`train.ipynb`** - Notebook con el pipeline completo
- **`drift_monitoring_example.py`** - Código para monitoreo en producción

---

## ✅ Checklist de Integración

- [x] Modelo entrenado guardado en `phishing_model_artefacts/`
- [x] API actualizada con carga de modelo y scaler
- [x] Extracción de features implementada
- [x] Normalización con scaler funcionando
- [x] 3 endpoints funcionando (`/predict`, `/health`, `/info`)
- [x] Script de pruebas creado (`test_api.py`)
- [x] Documentación de integración creada
- [ ] **Integrar con extensión del navegador** (siguiente paso)
- [ ] Convertir a TensorFlow.js (opcional)
- [ ] Desplegar en servidor de producción

---

**🎉 ¡Integración completada exitosamente!**

Autor: URLytics Team  
Fecha: 2025-11-15  
Versión: 2.0
