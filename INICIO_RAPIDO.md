# 🚀 Guía Rápida de Inicio - SocialGuard ML v2.0

## ⚡ Inicio Rápido en 5 Pasos

### 1️⃣ Ejecutar el Notebook Mejorado

```bash
# Abrir train.ipynb en Google Colab o Jupyter
# Ejecutar todas las celdas en orden
```

**Lo que hace automáticamente:**
- ✅ Carga y combina datasets de Kaggle
- ✅ Ejecuta 4 validaciones anti-leakage
- ✅ Entrena modelo con división 70/15/15
- ✅ Genera baseline para monitoreo
- ✅ Exporta modelo y artefactos

**Tiempo estimado:** 5-10 minutos

---

### 2️⃣ Verificar Validaciones Pasadas

Busca este output en el notebook:

```
======================================================================
✅ TODAS LAS VALIDACIONES PASADAS
✅ El modelo está protegido contra leakage y drift
======================================================================
```

**Si ves advertencias:**
- 🔍 Leer detalles de la validación que falló
- 📖 Consultar `ML_BEST_PRACTICES.md` para soluciones

---

### 3️⃣ Descargar Artefactos Generados

El notebook genera estos archivos:

```
phishing_model_artefacts/
├── phishing_model_rf.joblib      ← Modelo entrenado
├── scaler.joblib                  ← Normalizador
├── features.json                  ← Lista de features
├── model_metrics.json             ← Métricas completas
├── baseline_statistics.json       ← 🆕 Para drift detection
└── drift_monitoring_example.py    ← 🆕 Código de monitoreo
```

---

### 4️⃣ Integrar en tu Aplicación

#### Ejemplo básico de predicción:

```python
import joblib
import numpy as np

# Cargar modelo y scaler
model = joblib.load('phishing_model_rf.joblib')
scaler = joblib.load('scaler.joblib')

# Nueva URL para analizar
new_url_features = np.array([[
    -1,  # Abnormal_URL
    -1,  # Prefix_Suffix
     1,  # SSLfinal_State
    -1,  # Shortining_Service
     1,  # having_At_Symbol
    -1   # having_Sub_Domain
]])

# Normalizar y predecir
new_url_scaled = scaler.transform(new_url_features)
prediction = model.predict(new_url_scaled)
probability = model.predict_proba(new_url_scaled)

print(f"Predicción: {'🚨 Phishing' if prediction[0] == 1 else '✅ Legítimo'}")
print(f"Probabilidad phishing: {probability[0][1]*100:.2f}%")
```

---

### 5️⃣ Configurar Monitoreo de Drift

```python
from drift_monitoring_example import check_drift_simple

# Cada día/semana, ejecutar:
drift_info = check_drift_simple(
    new_data=production_predictions,
    baseline_path='baseline_statistics.json'
)

if drift_info['drift_detected']:
    print(f"⚠️ Drift detectado: {drift_info['features_with_drift']}")
    print(f"Severidad: {drift_info['severity']}")
    # Enviar alerta al equipo
```

---

## 📚 Documentos Clave (en orden de lectura)

### Para Empezar:
1. **📄 Este archivo** - Inicio rápido ← ESTÁS AQUÍ
2. **📓 train.ipynb** - Notebook mejorado
3. **✅ CHECKLIST_VALIDACION.md** - Verificar que todo esté bien

### Para Profundizar:
4. **📖 ML_BEST_PRACTICES.md** - Guía completa (leer primero)
5. **📊 PIPELINE_DIAGRAMS.md** - Diagramas visuales del flujo
6. **📝 MEJORAS_ML_V2.md** - Resumen técnico detallado

### Para Producción:
7. **🐍 drift_monitoring_example.py** - Código helper
8. **📋 RESUMEN_EJECUTIVO.md** - Para stakeholders

---

## 🎯 Las 4 Mejoras Clave (Resumen Ultra-Rápido)

### 1️⃣ Data Leakage Prevention
**Problema:** Scaler veía datos de test  
**Solución:** Scaler entrenado SOLO con training  
**Validación:** ✅ Overlap = 0, media val/test ≠ 0

### 2️⃣ Test Contamination Prevention
**Problema:** Tunear con test contamina evaluación  
**Solución:** División 70/15/15 (Train/Val/Test)  
**Validación:** ✅ Test tocado UNA VEZ al final

### 3️⃣ Data/Concept Drift Detection
**Problema:** Datos cambian con el tiempo  
**Solución:** KS test + baseline + monitoreo  
**Validación:** ✅ Drift analysis ejecutado

### 4️⃣ Hidden Feature Leakage Detection
**Problema:** Features "mágicas" hacen trampa  
**Solución:** Análisis de correlación + varianza  
**Validación:** ✅ Correlaciones < 0.95

---

## 🔥 Comandos Más Importantes

### Entrenar Modelo:
```python
# En train.ipynb, ejecutar todas las celdas
# O desde terminal:
jupyter nbconvert --execute train.ipynb
```

### Verificar Drift:
```python
python drift_monitoring_example.py
```

### Cargar Modelo:
```python
import joblib
model = joblib.load('phishing_model_rf.joblib')
scaler = joblib.load('scaler.joblib')
```

---

## 🚨 Alertas Importantes

### ⚠️ Si ves "LEAKAGE DETECTADO":
1. 🔍 Revisar correlaciones de features
2. 📖 Consultar sección 4 de `ML_BEST_PRACTICES.md`
3. 🔧 Eliminar features problemáticas
4. 🔄 Re-ejecutar notebook

### ⚠️ Si ves "DRIFT DETECTADO":
1. 📊 Revisar features afectadas
2. 🤔 ¿Es esperado? (datos evolucionan)
3. 📅 Programar re-entrenamiento si severity > MODERATE
4. 🔄 Si severity = HIGH → re-entrenar YA

### ⚠️ Si Test >> Validation:
1. 🚨 Posible test contamination o suerte
2. 🔍 Verificar uso correcto de conjuntos
3. 📖 Consultar sección 2 de `ML_BEST_PRACTICES.md`

### ⚠️ Si Accuracy > 99%:
1. 🚨 Demasiado bueno para ser verdad
2. 🔍 Investigar feature leakage
3. 📊 Revisar correlaciones
4. 🤔 Validar con conocimiento del dominio

---

## 📊 Métricas Objetivo

| Métrica | Mínimo Aceptable | Objetivo | Excelente |
|---------|------------------|----------|-----------|
| Accuracy | 85% | 90% | 95%+ |
| Precision | 80% | 85% | 90%+ |
| Recall | 80% | 85% | 90%+ |
| F1-Score | 80% | 85% | 90%+ |
| ROC-AUC | 0.85 | 0.90 | 0.95+ |

**Diferencia Val-Test:** < 5% (si > 10% → investigar overfitting)

---

## 🔄 Flujo de Trabajo Típico

### Desarrollo (Primera Vez):
```
1. Ejecutar train.ipynb completo
   ↓
2. Verificar validaciones pasadas
   ↓
3. Revisar métricas (accuracy, F1, etc.)
   ↓
4. Si OK → Descargar artefactos
   ↓
5. Integrar en aplicación
   ↓
6. Configurar monitoreo
   ↓
7. Deploy a producción
```

### Mantenimiento (Periódico):
```
1. Ejecutar drift detection (semanal)
   ↓
2. ¿Drift detectado?
   │
   ├─ NO → Continuar monitoreando
   │
   └─ SÍ → ¿Severity?
          │
          ├─ LOW → Watch & monitor
          ├─ MODERATE → Schedule retraining
          └─ HIGH → Retrain NOW!
```

### Re-entrenamiento:
```
1. Recolectar datos frescos
   ↓
2. Agregar al dataset
   ↓
3. Re-ejecutar train.ipynb
   ↓
4. Comparar métricas con v anterior
   ↓
5. A/B testing (opcional)
   ↓
6. Deploy nueva versión
   ↓
7. Actualizar baseline
```

---

## 💡 Tips Pro

### ✅ Mejores Prácticas:

1. **Siempre revisar validaciones**
   - No skipear la celda de validaciones
   - Investigar cualquier warning

2. **Guardar todo**
   - Modelo, scaler, baseline, metrics
   - Versionar con fecha/version number

3. **Monitorear desde día 1**
   - No esperar a que haya problemas
   - Revisar drift semanalmente

4. **Documentar decisiones**
   - Por qué elegiste estos hiperparámetros
   - Por qué eliminaste/agregaste features

5. **A/B testing para cambios grandes**
   - Nueva versión vs versión actual
   - Medir impacto en usuarios reales

### ❌ Errores Comunes a Evitar:

1. **Normalizar antes de split**
   ```python
   # ❌ MAL
   X_scaled = scaler.fit_transform(X)
   X_train, X_test = train_test_split(X_scaled)
   
   # ✅ BIEN
   X_train, X_test = train_test_split(X)
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)
   ```

2. **Tunear con test**
   ```python
   # ❌ MAL
   for param in params:
       score = model.score(X_test, y_test)
   
   # ✅ BIEN
   for param in params:
       score = model.score(X_val, y_val)
   ```

3. **Ignorar drift warnings**
   ```python
   # ❌ MAL
   if drift_detected:
       pass  # "Lo revisaré después"
   
   # ✅ BIEN
   if drift_detected:
       log_alert()
       investigate_cause()
       plan_retraining()
   ```

---

## 🆘 Troubleshooting Rápido

### Problema: "baseline_statistics.json not found"
**Solución:** Ejecutar train.ipynb completo, genera automáticamente

### Problema: "ValueError: Feature names mismatch"
**Solución:** Verificar que uses las mismas features que el modelo entrenado

### Problema: "Drift detectado en todas las features"
**Solución:** Datos de producción muy diferentes, necesitas re-entrenar urgente

### Problema: "Accuracy muy baja en producción"
**Solución:** 
1. Verificar que features se calculen igual
2. Verificar que scaler se aplique
3. Revisar drift detection

---

## 📞 Recursos de Ayuda

### Documentación:
- 📖 **ML_BEST_PRACTICES.md** - Referencia completa
- 📊 **PIPELINE_DIAGRAMS.md** - Visualizaciones
- ✅ **CHECKLIST_VALIDACION.md** - Checklist paso a paso

### Código:
- 📓 **train.ipynb** - Notebook principal
- 🐍 **drift_monitoring_example.py** - Scripts helper

### Referencias Externas:
- [Google ML Best Practices](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Kaggle Data Leakage](https://www.kaggle.com/learn/data-leakage)
- [Evidently AI Docs](https://docs.evidentlyai.com/)

---

## 🎯 Siguiente Paso Recomendado

### Si eres nuevo en el proyecto:
👉 **Leer:** `ML_BEST_PRACTICES.md` (10-15 minutos)

### Si vas a entrenar:
👉 **Ejecutar:** `train.ipynb` (5-10 minutos)

### Si vas a integrar:
👉 **Revisar:** Sección "Integrar en tu Aplicación" arriba

### Si ya está en producción:
👉 **Configurar:** `drift_monitoring_example.py`

---

## ✅ Checklist Mínimo para Empezar

- [ ] Ejecutar `train.ipynb` completo
- [ ] Verificar que todas las validaciones pasen
- [ ] Descargar artefactos generados
- [ ] Probar predicción con modelo cargado
- [ ] Configurar drift monitoring
- [ ] Leer `ML_BEST_PRACTICES.md`

**¿Todos los ítems marcados?** → 🚀 ¡Listo para producción!

---

**Versión:** 2.0  
**Autor:** SocialGuard ML Team  
**Última actualización:** 2025-11-15

**¿Preguntas?** Consultar documentos listados arriba o abrir issue en GitHub.

---

## 🎉 ¡Estás Listo!

Ahora tienes:
- ✅ Modelo protegido contra leakage
- ✅ Pipeline validado correctamente
- ✅ Sistema de monitoreo de drift
- ✅ Documentación completa
- ✅ Código de ejemplo

**¡Buena suerte con tu modelo! 🚀**
