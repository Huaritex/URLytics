# ✅ Checklist de Validación ML - SocialGuard

## 📋 Checklist Pre-Entrenamiento

### 🔍 Validación de Datos

- [ ] **Dataset cargado correctamente**
  - [ ] Sin errores de lectura
  - [ ] Columnas esperadas presentes
  - [ ] Tipos de datos correctos

- [ ] **Limpieza de datos completada**
  - [ ] Duplicados eliminados
  - [ ] Valores nulos manejados
  - [ ] Nombres de columnas normalizados

- [ ] **Features validadas**
  - [ ] No contienen información del futuro
  - [ ] No son derivadas directamente del target
  - [ ] Estarán disponibles en producción
  - [ ] Tienen sentido en el dominio del problema

### 🎯 Validación de Target

- [ ] **Distribución del target**
  - [ ] Balance aceptable (o estrategia para desbalance)
  - [ ] Sin valores nulos
  - [ ] Tipo de dato correcto (int para clasificación)

### ✂️ División de Datos

- [ ] **Split en 3 conjuntos (70/15/15)**
  - [ ] Training: ~70% de los datos
  - [ ] Validation: ~15% de los datos
  - [ ] Test: ~15% de los datos

- [ ] **Estratificación aplicada**
  - [ ] Distribución similar de target en Train/Val/Test
  - [ ] Diferencia < 2% entre conjuntos

- [ ] **Sin overlap entre conjuntos**
  - [ ] Train ∩ Val = ∅
  - [ ] Train ∩ Test = ∅
  - [ ] Val ∩ Test = ∅

---

## 🔧 Checklist Durante Entrenamiento

### 📐 Normalización/Preprocesamiento

- [ ] **Scaler entrenado SOLO con training**
  - [ ] `scaler.fit_transform(X_train)` ← Aprende
  - [ ] `scaler.transform(X_val)` ← Solo transforma
  - [ ] `scaler.transform(X_test)` ← Solo transforma

- [ ] **Validación post-normalización**
  - [ ] Media de X_train ≈ 0
  - [ ] Std de X_train ≈ 1
  - [ ] Media de X_val ≠ 0 (confirma no-leakage)
  - [ ] Media de X_test ≠ 0 (confirma no-leakage)

### 🧠 Entrenamiento del Modelo

- [ ] **Modelo entrenado solo con training**
  - [ ] `model.fit(X_train, y_train)`
  - [ ] No se usó X_val o X_test durante fit

- [ ] **Evaluación durante desarrollo**
  - [ ] Métricas calculadas en validation set
  - [ ] Test set NO tocado aún

### 🎚️ Ajuste de Hiperparámetros

- [ ] **Tunning con validation set**
  - [ ] Hiperparámetros ajustados basándose en métricas de validation
  - [ ] NO se usó test para decidir hiperparámetros

- [ ] **Prevención de overfitting**
  - [ ] Comparar Train vs Validation accuracy
  - [ ] Si Train >> Validation → overfitting detectado

---

## 🛡️ Checklist de Validaciones Anti-Leakage

### 1️⃣ Data Leakage Check

- [ ] **Overlap verification**
  - [ ] Sin filas duplicadas entre Train/Val/Test
  - [ ] Hash verification ejecutado

- [ ] **Correlación de features**
  - [ ] Ninguna feature con correlación > 0.95 vs target
  - [ ] Features sospechosas investigadas

- [ ] **Varianza de features**
  - [ ] Todas las features tienen varianza > 0.01
  - [ ] Features de baja varianza identificadas

### 2️⃣ Test Contamination Check

- [ ] **División correcta aplicada**
  - [ ] 70% Training
  - [ ] 15% Validation
  - [ ] 15% Test

- [ ] **Uso correcto de conjuntos**
  - [ ] Training → Entrenar modelo
  - [ ] Validation → Tunear hiperparámetros
  - [ ] Test → Evaluación final (UNA VEZ)

### 3️⃣ Data Drift Detection

- [ ] **Test de Kolmogorov-Smirnov ejecutado**
  - [ ] KS test para cada feature
  - [ ] p-values registrados
  - [ ] Features con drift identificadas (p < 0.05)

- [ ] **Análisis de drift**
  - [ ] Si drift detectado → investigar causa
  - [ ] Validar si es esperado o preocupante

### 4️⃣ Hidden Feature Leakage Detection

- [ ] **Análisis de correlación completado**
  - [ ] Correlaciones feature→target calculadas
  - [ ] Features "mágicas" investigadas

- [ ] **Feature importance review**
  - [ ] Importancias calculadas
  - [ ] Ninguna feature con >90% importancia
  - [ ] Importancias tienen sentido lógico

---

## 📊 Checklist Post-Entrenamiento

### 🧪 Evaluación Final

- [ ] **Evaluación en test set (UNA VEZ)**
  - [ ] Accuracy calculada
  - [ ] Precision calculada
  - [ ] Recall calculada
  - [ ] F1-score calculada
  - [ ] ROC-AUC calculada

- [ ] **Comparación Val vs Test**
  - [ ] Métricas similares → modelo generaliza bien
  - [ ] Val >> Test → posible overfitting
  - [ ] Test >> Val → posible suerte/leakage

### 📈 Visualizaciones

- [ ] **Matriz de confusión generada**
  - [ ] True Positives identificados
  - [ ] False Positives analizados
  - [ ] False Negatives analizados
  - [ ] True Negatives verificados

- [ ] **Curva ROC generada**
  - [ ] AUC calculada
  - [ ] Threshold óptimo identificado

- [ ] **Feature importance visualizada**
  - [ ] Top features identificadas
  - [ ] Tiene sentido en el contexto del problema

---

## 💾 Checklist de Exportación

### 🔐 Modelo y Artefactos

- [ ] **Modelo guardado**
  - [ ] `phishing_model_rf.joblib` exportado
  - [ ] Modelo carga correctamente
  - [ ] Número de features correcto

- [ ] **Scaler guardado**
  - [ ] `scaler.joblib` exportado
  - [ ] Scaler carga correctamente
  - [ ] Parámetros (mean, scale) verificados

- [ ] **Features guardadas**
  - [ ] `features.json` exportado
  - [ ] Lista de features coincide con modelo

- [ ] **Métricas guardadas**
  - [ ] `model_metrics.json` exportado
  - [ ] Métricas de training, validation y test incluidas
  - [ ] Feature importance incluida

### 📊 Baseline para Monitoreo

- [ ] **Baseline statistics guardadas**
  - [ ] `baseline_statistics.json` exportado
  - [ ] Estadísticas por feature incluidas
  - [ ] Performance baseline incluida

- [ ] **Código de monitoreo generado**
  - [ ] `drift_monitoring_example.py` exportado
  - [ ] Funciones de drift detection incluidas
  - [ ] Ejemplo de uso documentado

---

## 🚀 Checklist de Producción

### 🔌 Integración

- [ ] **Modelo integrado en API**
  - [ ] Endpoint de predicción funcionando
  - [ ] Scaler aplicado correctamente
  - [ ] Features extraídas correctamente

- [ ] **Validación de entrada**
  - [ ] Features requeridas validadas
  - [ ] Tipos de datos correctos
  - [ ] Valores dentro de rangos esperados

### 📡 Monitoreo

- [ ] **Sistema de drift detection configurado**
  - [ ] `check_drift()` ejecutándose periódicamente
  - [ ] Frecuencia definida (diario/semanal)
  - [ ] Baseline cargada correctamente

- [ ] **Alertas configuradas**
  - [ ] Alerta cuando drift detectado
  - [ ] Alerta cuando performance cae
  - [ ] Notificaciones al equipo (Slack/Email)

- [ ] **Logging implementado**
  - [ ] Predicciones guardadas
  - [ ] Timestamps registrados
  - [ ] Features de entrada guardadas (para análisis)

### 🔄 Plan de Re-entrenamiento

- [ ] **Criterios definidos**
  - [ ] Umbral de drift para re-entrenar
  - [ ] Umbral de performance decay
  - [ ] Frecuencia mínima de re-entrenamiento

- [ ] **Proceso documentado**
  - [ ] Pasos para recolectar datos frescos
  - [ ] Pipeline de re-entrenamiento automatizado
  - [ ] Proceso de A/B testing para nueva versión

---

## 📚 Checklist de Documentación

### 📝 Documentación Técnica

- [ ] **README actualizado**
  - [ ] Descripción de mejoras ML
  - [ ] Instrucciones de uso
  - [ ] Referencias a documentos

- [ ] **Documentación de mejores prácticas**
  - [ ] `ML_BEST_PRACTICES.md` creado
  - [ ] Ejemplos de código incluidos
  - [ ] Referencias externas incluidas

- [ ] **Documentación de pipeline**
  - [ ] `PIPELINE_DIAGRAMS.md` creado
  - [ ] Diagramas visuales incluidos
  - [ ] Flujo completo documentado

### 📊 Documentación de Resultados

- [ ] **Resumen de mejoras**
  - [ ] `MEJORAS_ML_V2.md` creado
  - [ ] Comparación antes/después
  - [ ] Validaciones documentadas

- [ ] **Resumen ejecutivo**
  - [ ] `RESUMEN_EJECUTIVO.md` creado
  - [ ] Impacto de mejoras documentado
  - [ ] Próximos pasos definidos

---

## 🎯 Criterios de Éxito

### ✅ El proyecto cumple con éxito si:

#### Validaciones Técnicas
- [x] Sin data leakage detectado
- [x] Sin test contamination
- [x] Drift analysis completado
- [x] Sin feature leakage

#### Rendimiento
- [ ] Accuracy > 90% en test
- [ ] F1-score > 0.85 en test
- [ ] ROC-AUC > 0.90 en test
- [ ] Diferencia Val-Test < 5%

#### Infraestructura
- [x] Modelo exportado correctamente
- [x] Baseline guardada
- [x] Sistema de monitoreo implementado
- [x] Documentación completa

#### Producción
- [ ] API funcionando
- [ ] Monitoreo activo
- [ ] Alertas configuradas
- [ ] Plan de re-entrenamiento definido

---

## 🚨 Red Flags a Evitar

### ❌ Señales de Problemas

- [ ] **Accuracy "perfecta" (>99%)**
  - 🚨 Posible feature leakage
  - 🔍 Investigar correlaciones

- [ ] **Test score >> Validation score**
  - 🚨 Posible test contamination o suerte
  - 🔍 Verificar uso de conjuntos

- [ ] **Una feature domina (>90% importance)**
  - 🚨 Posible hidden leakage
  - 🔍 Validar feature manualmente

- [ ] **Val score >> Train score**
  - 🚨 Posible error en split o leakage
  - 🔍 Verificar división de datos

- [ ] **Drift severo en múltiples features**
  - 🚨 Datos cambiaron significativamente
  - 🔍 Re-entrenar inmediatamente

---

## 📅 Calendario de Mantenimiento

### Diario
- [ ] Verificar logs de predicciones
- [ ] Revisar errores en producción

### Semanal
- [ ] Ejecutar drift detection
- [ ] Revisar métricas de performance
- [ ] Analizar predicciones incorrectas

### Mensual
- [ ] Revisión completa de drift
- [ ] Análisis de performance trends
- [ ] Evaluar necesidad de re-entrenamiento

### Trimestral
- [ ] Re-entrenamiento programado (mínimo)
- [ ] Revisión de features (agregar/remover)
- [ ] Actualización de documentación

---

**Versión**: 2.0  
**Fecha**: 2025-11-15  
**Autor**: SocialGuard ML Team

---

## 💡 Uso de este Checklist

1. ✅ **Durante desarrollo**: Marcar cada ítem al completarlo
2. 📝 **Antes de PR**: Verificar que todos los ítems críticos estén marcados
3. 🚀 **Antes de deploy**: Verificar sección de producción completa
4. 🔄 **Mantenimiento**: Seguir calendario de revisiones

**¿Todos los ítems marcados?** → ✅ Modelo listo para producción!
