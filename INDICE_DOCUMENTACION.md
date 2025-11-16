# 📚 Índice de Documentación - URLytics ML v2.0

## 🎯 Por Dónde Empezar

### 🚀 Si quieres empezar RÁPIDO:
👉 **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** (5 minutos)
- Guía paso a paso para ejecutar el modelo
- Comandos esenciales
- Troubleshooting básico

### 📖 Si quieres ENTENDER las mejoras:
👉 **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** (10 minutos)
- Qué problemas se resolvieron
- Por qué son importantes
- Impacto de las mejoras

### 🔬 Si quieres PROFUNDIZAR:
👉 **[ML_BEST_PRACTICES.md](ML_BEST_PRACTICES.md)** (30 minutos)
- Guía completa de mejores prácticas
- Ejemplos de código detallados
- Referencias y recursos

---

## 📂 Estructura de la Documentación

### 📘 Documentos Principales

| Documento | Descripción | Audiencia | Tiempo |
|-----------|-------------|-----------|--------|
| **[INSTALACION_COMPLETADA.md](INSTALACION_COMPLETADA.md)** | ✨ Estado de instalación | Todos | 2 min |
| **[INSTALACION.md](INSTALACION.md)** | Guía completa de instalación | Todos | 5 min |
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Guía de inicio rápido | Todos | 5 min |
| **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** | Resumen de mejoras y resultados | Todos | 10 min |
| **[ML_BEST_PRACTICES.md](ML_BEST_PRACTICES.md)** | Guía completa de mejores prácticas | Desarrolladores | 30 min |
| **[MEJORAS_ML_V2.md](MEJORAS_ML_V2.md)** | Resumen técnico detallado | ML Engineers | 15 min |
| **[PIPELINE_DIAGRAMS.md](PIPELINE_DIAGRAMS.md)** | Diagramas visuales del flujo | Visual learners | 15 min |
| **[CHECKLIST_VALIDACION.md](CHECKLIST_VALIDACION.md)** | Checklist paso a paso | Desarrolladores | Ref. |

### 📓 Notebooks y Código

| Archivo | Descripción | Tipo |
|---------|-------------|------|
| **train.ipynb** | Notebook principal mejorado | Jupyter Notebook |
| **drift_monitoring_example.py** | Script de monitoreo de drift | Python |
| **verify_installation.py** | ✨ Verificación de instalación | Python |
| **activate_env.sh** | ✨ Script de activación del entorno | Bash |
| **api.py** | API de predicción | Python |

### 📊 Archivos del Modelo

| Archivo | Descripción | Generado por |
|---------|-------------|--------------|
| `phishing_model_rf.joblib` | Modelo entrenado | train.ipynb |
| `scaler.joblib` | StandardScaler | train.ipynb |
| `features.json` | Lista de features | train.ipynb |
| `model_metrics.json` | Métricas completas | train.ipynb |
| `baseline_statistics.json` | Stats para drift detection | train.ipynb |

---

## 🗺️ Mapa de Navegación por Caso de Uso

### 🎓 "Soy nuevo en el proyecto"
```
1. README.md                 (Visión general del proyecto)
   ↓
2. INICIO_RAPIDO.md         (Cómo empezar)
   ↓
3. train.ipynb              (Ejecutar entrenamiento)
   ↓
4. RESUMEN_EJECUTIVO.md     (Entender las mejoras)
   ↓
5. ML_BEST_PRACTICES.md     (Profundizar conocimiento)
```

### 🔧 "Voy a entrenar el modelo"
```
1. CHECKLIST_VALIDACION.md  (Revisar checklist)
   ↓
2. train.ipynb              (Ejecutar entrenamiento)
   ↓
3. Verificar validaciones   (En salida del notebook)
   ↓
4. MEJORAS_ML_V2.md         (Si hay problemas)
```

### 🚀 "Voy a deployar a producción"
```
1. INICIO_RAPIDO.md         (Sección "Integrar en tu Aplicación")
   ↓
2. drift_monitoring_example.py (Configurar monitoreo)
   ↓
3. CHECKLIST_VALIDACION.md  (Sección "Producción")
   ↓
4. ML_BEST_PRACTICES.md     (Sección "Monitoreo de Drift")
```

### 🔍 "Hay drift detectado"
```
1. drift_monitoring_example.py (Ejecutar análisis)
   ↓
2. PIPELINE_DIAGRAMS.md     (Sección "Matriz de Decisión")
   ↓
3. ML_BEST_PRACTICES.md     (Sección "Data/Concept Drift")
   ↓
4. train.ipynb              (Re-entrenar si necesario)
```

### 📊 "Necesito entender los diagramas"
```
1. PIPELINE_DIAGRAMS.md     (Visualizaciones completas)
   ↓
2. MEJORAS_ML_V2.md         (Sección "Nuevas Celdas")
   ↓
3. train.ipynb              (Ver implementación)
```

---

## 📖 Guías por Tema

### 1️⃣ Data Leakage

**Qué es:**
- 📖 ML_BEST_PRACTICES.md → Sección 1
- 📊 PIPELINE_DIAGRAMS.md → "Las 4 Capas"
- ✅ CHECKLIST_VALIDACION.md → "Data Leakage Check"

**Cómo prevenirlo:**
- 📓 train.ipynb → Celda de validación anti-leakage
- 📝 MEJORAS_ML_V2.md → Sección "Validaciones"
- 🚀 INICIO_RAPIDO.md → "Las 4 Mejoras Clave"

### 2️⃣ Test Contamination

**Qué es:**
- 📖 ML_BEST_PRACTICES.md → Sección 2
- 📊 PIPELINE_DIAGRAMS.md → "Comparación: Antes vs Después"
- 📋 RESUMEN_EJECUTIVO.md → Mejora 2

**Cómo prevenirlo:**
- 📓 train.ipynb → División 70/15/15
- ✅ CHECKLIST_VALIDACION.md → "Test Contamination Check"
- 🚀 INICIO_RAPIDO.md → Mejora 2

### 3️⃣ Data/Concept Drift

**Qué es:**
- 📖 ML_BEST_PRACTICES.md → Sección 3
- 📊 PIPELINE_DIAGRAMS.md → "Ciclo de Vida en Producción"
- 📋 RESUMEN_EJECUTIVO.md → Mejora 3

**Cómo detectarlo:**
- 🐍 drift_monitoring_example.py → check_drift()
- 📓 train.ipynb → Celda de drift detection
- ✅ CHECKLIST_VALIDACION.md → "Data Drift Detection"

### 4️⃣ Hidden Feature Leakage

**Qué es:**
- 📖 ML_BEST_PRACTICES.md → Sección 4
- 📝 MEJORAS_ML_V2.md → "Hidden Feature Leakage Detection"
- 📋 RESUMEN_EJECUTIVO.md → Mejora 4

**Cómo detectarlo:**
- 📓 train.ipynb → Análisis de correlación
- ✅ CHECKLIST_VALIDACION.md → "Feature Leakage Check"
- 🚀 INICIO_RAPIDO.md → Alertas importantes

---

## 🎯 Flujos de Lectura Recomendados

### Para Manager/Stakeholder (15 minutos):
```
1. README.md                 (5 min)  - Visión general
2. RESUMEN_EJECUTIVO.md     (10 min) - Impacto de mejoras
```

### Para ML Engineer (60 minutos):
```
1. INICIO_RAPIDO.md         (5 min)  - Comandos básicos
2. RESUMEN_EJECUTIVO.md     (10 min) - Qué se mejoró
3. ML_BEST_PRACTICES.md     (30 min) - Teoría completa
4. train.ipynb              (15 min) - Ver implementación
```

### Para DevOps (30 minutos):
```
1. INICIO_RAPIDO.md         (5 min)  - Setup básico
2. drift_monitoring_example.py (10 min) - Script de monitoreo
3. CHECKLIST_VALIDACION.md  (15 min) - Sección producción
```

### Para QA/Testing (20 minutos):
```
1. CHECKLIST_VALIDACION.md  (15 min) - Todos los checks
2. MEJORAS_ML_V2.md         (5 min)  - Qué validar
```

---

## 🔍 Búsqueda Rápida por Keyword

### Accuracy / Métricas
- 📓 train.ipynb → Celda de evaluación
- 📊 model_metrics.json
- 📖 ML_BEST_PRACTICES.md → "Métricas de Evaluación"

### Baseline
- 📊 baseline_statistics.json
- 📓 train.ipynb → Celda de baseline
- 🐍 drift_monitoring_example.py → load_baseline()

### Cross-Validation
- 📖 ML_BEST_PRACTICES.md → "Nested Cross-Validation"
- 📓 train.ipynb → Markdown sobre CV

### Drift
- 🐍 drift_monitoring_example.py
- 📊 PIPELINE_DIAGRAMS.md → "Ciclo de Vida"
- 📖 ML_BEST_PRACTICES.md → Sección 3

### Features
- 📊 features.json
- 📓 train.ipynb → FEATURES list
- 📖 ML_BEST_PRACTICES.md → "Feature Leakage"

### Hiperparámetros
- 📓 train.ipynb → RandomForestClassifier config
- 📖 ML_BEST_PRACTICES.md → "Ajuste de Hiperparámetros"

### Normalización
- 📊 scaler.joblib
- 📓 train.ipynb → StandardScaler
- 📖 ML_BEST_PRACTICES.md → "Normalización"

### Overfitting
- 📓 train.ipynb → Comparación Val vs Test
- 📖 ML_BEST_PRACTICES.md → "Prevención de Overfitting"
- ✅ CHECKLIST_VALIDACION.md → "Prevención de overfitting"

### Re-entrenamiento
- 🐍 drift_monitoring_example.py → should_retrain()
- 📊 PIPELINE_DIAGRAMS.md → "Matriz de Decisión"
- 📖 ML_BEST_PRACTICES.md → "Estrategia de Re-entrenamiento"

### Scaler
- 📊 scaler.joblib
- 📓 train.ipynb → StandardScaler
- 🚀 INICIO_RAPIDO.md → "Cargar Modelo"

### Train/Val/Test Split
- 📓 train.ipynb → train_test_split
- 📖 ML_BEST_PRACTICES.md → Sección 2
- 📊 PIPELINE_DIAGRAMS.md → "División de Datos"

### Validaciones
- 📓 train.ipynb → Celda de validaciones
- ✅ CHECKLIST_VALIDACION.md → Todas las secciones
- 📝 MEJORAS_ML_V2.md → "Validaciones Implementadas"

---

## 📊 Matriz de Contenido

|  | Teoría | Práctica | Validación | Monitoreo |
|--|--------|----------|------------|-----------|
| **Data Leakage** | ML_BEST_PRACTICES.md | train.ipynb | CHECKLIST_VALIDACION.md | - |
| **Test Contamination** | ML_BEST_PRACTICES.md | train.ipynb | CHECKLIST_VALIDACION.md | - |
| **Drift Detection** | ML_BEST_PRACTICES.md | drift_monitoring_example.py | CHECKLIST_VALIDACION.md | drift_monitoring_example.py |
| **Feature Leakage** | ML_BEST_PRACTICES.md | train.ipynb | CHECKLIST_VALIDACION.md | - |

---

## 🆘 Troubleshooting - Dónde Buscar

| Problema | Documento | Sección |
|----------|-----------|---------|
| Accuracy muy alta (>99%) | ML_BEST_PRACTICES.md | Sección 4 |
| Accuracy cae en producción | drift_monitoring_example.py | check_performance_decay() |
| Baseline no encontrado | INICIO_RAPIDO.md | Troubleshooting |
| Drift detectado | PIPELINE_DIAGRAMS.md | Matriz de Decisión |
| Error al cargar modelo | INICIO_RAPIDO.md | Integrar en aplicación |
| Feature names mismatch | INICIO_RAPIDO.md | Troubleshooting |
| Overfitting detectado | ML_BEST_PRACTICES.md | Prevención de Overfitting |
| Test >> Validation | ML_BEST_PRACTICES.md | Sección 2 |
| Validaciones fallan | CHECKLIST_VALIDACION.md | Red Flags |

---

## 📅 Documentos por Fase del Proyecto

### Fase 1: Setup Inicial
- [ ] README.md
- [ ] INICIO_RAPIDO.md
- [ ] train.ipynb

### Fase 2: Entrenamiento
- [ ] CHECKLIST_VALIDACION.md
- [ ] train.ipynb
- [ ] ML_BEST_PRACTICES.md

### Fase 3: Validación
- [ ] MEJORAS_ML_V2.md
- [ ] CHECKLIST_VALIDACION.md
- [ ] PIPELINE_DIAGRAMS.md

### Fase 4: Deployment
- [ ] INICIO_RAPIDO.md (Integración)
- [ ] drift_monitoring_example.py
- [ ] CHECKLIST_VALIDACION.md (Producción)

### Fase 5: Mantenimiento
- [ ] drift_monitoring_example.py
- [ ] PIPELINE_DIAGRAMS.md (Ciclo de Vida)
- [ ] ML_BEST_PRACTICES.md (Re-entrenamiento)

---

## 🎓 Recursos Externos Referenciados

### En ML_BEST_PRACTICES.md:
- Google ML Best Practices
- Kaggle Data Leakage Tutorial
- Towards Data Science - Concept Drift
- Papers with Code - Distribution Shift

### Herramientas Mencionadas:
- Evidently AI (Drift monitoring)
- Great Expectations (Data validation)
- MLflow (Experiment tracking)
- Weights & Biases (Model monitoring)

---

## ✅ Checklist de Documentación Leída

### Nivel Básico (Para empezar):
- [ ] README.md
- [ ] INICIO_RAPIDO.md
- [ ] RESUMEN_EJECUTIVO.md

### Nivel Intermedio (Para desarrollar):
- [ ] train.ipynb (ejecutar y entender)
- [ ] MEJORAS_ML_V2.md
- [ ] CHECKLIST_VALIDACION.md

### Nivel Avanzado (Para dominar):
- [ ] ML_BEST_PRACTICES.md
- [ ] PIPELINE_DIAGRAMS.md
- [ ] drift_monitoring_example.py (código completo)

---

## 🔄 Mantenimiento de Documentación

### Esta documentación se actualiza cuando:
- ✅ Se agrega nueva funcionalidad
- ✅ Se encuentra un bug común
- ✅ Se mejora el pipeline
- ✅ Usuarios reportan confusión

### Versiones:
- **v1.0** (Original) - README básico
- **v2.0** (Actual) - Mejoras ML completas + documentación exhaustiva

---

## 📞 Contacto y Contribuciones

**Equipo:** URLytics ML Team  
**Versión de docs:** 2.0  
**Última actualización:** 2025-11-15

**¿Encontraste un error en la documentación?**  
Por favor abre un issue en GitHub con el tag `documentation`.

**¿Quieres contribuir?**  
Pull requests son bienvenidos! Sigue el mismo estilo de documentación.

---

## 🎯 Próximas Adiciones Planeadas

### En desarrollo:
- [ ] Tutorial en video del notebook
- [ ] FAQ extendido
- [ ] Ejemplos de integración con diferentes frameworks
- [ ] Guía de optimización de hiperparámetros

### Solicitado por usuarios:
- [ ] Traducción al inglés
- [ ] Jupyter notebook con ejemplos interactivos
- [ ] Dashboard de métricas (Streamlit)

---

**¡Gracias por usar URLytics! 🛡️**

Para empezar, ve a: **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** 🚀
