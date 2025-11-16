# 🛡️ Machine Learning Best Practices - Anti-Leakage & Drift Prevention

## 📚 Documento de Referencia para Proyectos de ML

Este documento describe las **4 mejoras críticas** implementadas en el notebook `train.ipynb` para prevenir problemas comunes en Machine Learning.

---

## 1️⃣ DATA LEAKAGE PREVENTION

### ❌ Problema
El modelo "ve" información del conjunto de test durante el entrenamiento, inflando artificialmente las métricas.

### 🔍 Ejemplos de Data Leakage

**Caso 1: Normalización incorrecta**
```python
# ❌ MAL - Fit del scaler con TODOS los datos
scaler.fit(X)  # Incluye train, val y test
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Caso 2: Features derivadas del target**
```python
# ❌ MAL - Feature que "conoce" el resultado
df['is_fraud_ratio'] = df.groupby('user_id')['is_fraud'].transform('mean')
# Esta feature contiene información del target!
```

### ✅ Solución Implementada

```python
# ✅ BIEN - Scaler se entrena SOLO con training
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Aprende de training
X_val_scaled = scaler.transform(X_val)          # Solo transforma
X_test_scaled = scaler.transform(X_test)        # Solo transforma
```

### 🔍 Validaciones Implementadas

1. **Verificación de overlap**: Asegurar que no hay filas duplicadas entre train/val/test
2. **Análisis de correlaciones**: Detectar features con correlación >0.95 con el target
3. **Validación de varianza**: Identificar features sin información útil

---

## 2️⃣ TEST CONTAMINATION PREVENTION

### ❌ Problema
Usar el conjunto de test para ajustar hiperparámetros contamina la evaluación final.

### 🔍 Ejemplo de Contaminación

```python
# ❌ MAL - Tunear hiperparámetros con test
for n_estimators in [50, 100, 200]:
    model = RandomForest(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)  # ⚠️ Usando test para decidir!
    if score > best_score:
        best_n_estimators = n_estimators
```

### ✅ Solución: División en 3 Conjuntos

```
┌─────────────────────────────────────────┐
│ Dataset Total (100%)                    │
├─────────────────────────────────────────┤
│                                         │
│  Train (70%)  →  Entrenar modelo        │
│                                         │
│  Val (15%)    →  Ajustar hiperparámetros│
│                  Validar durante dev    │
│                                         │
│  Test (15%)   →  Evaluación FINAL       │
│                  (tocar UNA VEZ)        │
│                                         │
└─────────────────────────────────────────┘
```

### 📊 Implementación

```python
# División estratificada en 3 conjuntos
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)
```

### 🎯 Workflow Correcto

1. **Durante desarrollo**:
   - Entrenar con `X_train, y_train`
   - Evaluar con `X_val, y_val`
   - Iterar ajustando hiperparámetros basándote en validation

2. **Al final (UNA VEZ)**:
   - Evaluar con `X_test, y_test`
   - Reportar métricas finales
   - NO iterar más después de ver test

### 🔄 Alternativa: Nested Cross-Validation

Para datasets pequeños (<10k samples):

```python
from sklearn.model_selection import cross_val_score, GridSearchCV

# CV externa: evaluar el modelo
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)

# CV interna: tunear hiperparámetros
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

clf = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid={'n_estimators': [50, 100, 200]},
    cv=inner_cv
)

scores = cross_val_score(clf, X, y, cv=outer_cv)
```

---

## 3️⃣ DATA DRIFT / CONCEPT DRIFT DETECTION

### ❌ Problema
Los datos cambian con el tiempo y el modelo se vuelve obsoleto sin que lo notes.

### 🔍 Tipos de Drift

**Data Drift**: La distribución de las features cambia
```
Training (2024):    avg_url_length = 45 caracteres
Production (2025):  avg_url_length = 120 caracteres  ⚠️ Cambió!
```

**Concept Drift**: La relación feature→target cambia
```
Antes:  "bit.ly" → 80% phishing
Ahora:  "bit.ly" → 30% phishing (acortadores más seguros)
```

### ✅ Solución: Monitoreo Continuo

#### 1. Guardar Baseline en Training

```python
baseline_stats = {
    'feature_statistics': {
        'url_length': {
            'mean': 45.2,
            'std': 12.8,
            'min': 10,
            'max': 200
        }
    },
    'performance_baseline': {
        'test_accuracy': 0.9523,
        'test_f1': 0.9481
    }
}
```

#### 2. Detectar Drift en Producción

```python
from scipy.stats import ks_2samp

def check_drift(new_data, baseline, threshold=0.05):
    """
    Detecta drift usando test de Kolmogorov-Smirnov
    
    Returns:
        drift_detected: bool
        features_with_drift: list
    """
    drift_features = []
    
    for feature in baseline['feature_statistics'].keys():
        # KS test: compara distribuciones
        ks_stat, p_value = ks_2samp(
            baseline_samples[feature],  # Samples de training
            new_data[feature]           # Samples de producción
        )
        
        # Si p < 0.05 → distribuciones son diferentes
        if p_value < threshold:
            drift_features.append(feature)
    
    return len(drift_features) > 0, drift_features
```

#### 3. Detectar Performance Decay

```python
# Monitorear accuracy en producción (requiere ground truth)
current_accuracy = evaluate_production_data(model, labeled_production_data)

if current_accuracy < baseline_stats['test_accuracy'] * 0.90:
    print("⚠️ Accuracy cayó >10% - Necesita re-entrenamiento")
```

### 📅 Estrategia de Re-entrenamiento

| Señal | Acción |
|-------|--------|
| Drift leve (1-2 features) | Monitorear |
| Drift moderado (3-5 features) | Planear re-entrenamiento |
| Drift severo (>5 features) | Re-entrenar inmediatamente |
| Accuracy cae >10% | Re-entrenar urgente |

### 🔄 Ciclo de Vida del Modelo

```
1. Training inicial     → Baseline guardado
2. Deploy a producción  → Monitoreo activo
3. Drift detectado      → Alerta generada
4. Re-training          → Nuevo baseline
5. A/B testing          → Validar mejora
6. Deploy nueva versión → Volver a paso 2
```

---

## 4️⃣ HIDDEN FEATURE LEAKAGE DETECTION

### ❌ Problema
Una feature contiene información del target sin que lo sepas, el modelo "hace trampa".

### 🔍 Ejemplos Reales

**Caso 1: Competencia Kaggle (Neumonía en rayos X)**
```
Feature: "image_filename"
Patrón descubierto: "pneumonia_patient_123.jpg"

Accuracy aparente: 99.9%
Accuracy real: 55%

❌ El modelo aprendió a leer el nombre del archivo, no la imagen!
```

**Caso 2: Predicción de Fraude**
```python
# ❌ Feature leaky
df['transaction_declined'] = ...  # Esta columna viene DESPUÉS del fraude
                                  # El modelo no tendrá este dato en producción!
```

**Caso 3: Features Temporales**
```python
# ❌ Usando información del futuro
df['avg_next_week_purchases'] = ...  # No existe al momento de predecir
```

### ✅ Solución: Análisis de Correlación

#### 1. Detectar Features Sospechosas

```python
from scipy.stats import pearsonr

for feature in FEATURES:
    corr, p_value = pearsonr(X_train[feature], y_train)
    
    if abs(corr) > 0.95:
        print(f"🚨 {feature}: correlación {corr:.4f} - SOSPECHOSO!")
    elif abs(corr) > 0.80:
        print(f"⚠️ {feature}: correlación {corr:.4f} - Revisar")
```

#### 2. Validar con Conocimiento del Dominio

Preguntas clave:
- ✅ ¿Esta feature estará disponible en producción?
- ✅ ¿La feature es anterior al evento que quiero predecir?
- ✅ ¿La feature es calculable sin conocer el target?

#### 3. Feature Importance Sanity Check

```python
# Si una feature tiene >90% de importancia → sospechoso
feature_importance = model.feature_importances_

for i, (feat, imp) in enumerate(zip(FEATURES, feature_importance)):
    if imp > 0.90:
        print(f"🚨 {feat} tiene {imp:.2%} de importancia - Investigar!")
```

### 🎯 Checklist de Validación

- [ ] ¿La feature existirá en el momento de la predicción?
- [ ] ¿La feature es calculable sin conocer el outcome?
- [ ] ¿La correlación con target es <0.80?
- [ ] ¿Tiene sentido lógico que esta feature prediga el target?
- [ ] ¿El rendimiento es "demasiado bueno para ser verdad"?

---

## 🎓 RESUMEN: Flujo de Trabajo Correcto

### 📋 Pipeline Completo

```python
# 1️⃣ Cargar datos
df = load_data()

# 2️⃣ ANTES de dividir: limpieza básica
df = df.drop_duplicates()
df = df.dropna()

# 3️⃣ Separar features y target
X = df[FEATURES]
y = df['target']

# 4️⃣ División estratificada (70/15/15)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

# 5️⃣ Normalización SOLO con training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# 6️⃣ Validaciones anti-leakage
check_data_overlap(X_train, X_val, X_test)
check_feature_leakage(X_train, y_train)
check_data_drift(X_train, X_test)

# 7️⃣ Entrenar modelo
model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

# 8️⃣ Evaluar en VALIDATION (para tunear)
y_val_pred = model.predict(X_val_scaled)
val_score = f1_score(y_val, y_val_pred)
print(f"Validation F1: {val_score}")

# 9️⃣ Ajustar hiperparámetros basándote en validation
# ... iterar pasos 7-8 ...

# 🔟 Evaluación FINAL en test (UNA VEZ)
y_test_pred = model.predict(X_test_scaled)
test_score = f1_score(y_test, y_test_pred)
print(f"Test F1: {test_score}")

# 1️⃣1️⃣ Guardar baseline para monitoreo
save_baseline_stats(X_train, y_train, test_score)

# 1️⃣2️⃣ Deploy y monitoreo continuo
monitor_drift_in_production()
```

---

## 📚 Referencias y Recursos

### 📖 Lecturas Recomendadas

1. **[Google - Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)**
   - Rule #6: Be careful about leaked information from data collection

2. **[Kaggle - Data Leakage](https://www.kaggle.com/learn/data-leakage)**
   - Tutorial interactivo sobre leakage

3. **[Towards Data Science - Concept Drift](https://towardsdatascience.com/machine-learning-in-production-why-you-should-care-about-data-and-concept-drift-d96d0bc907fb)**
   - Detección y manejo de drift

4. **[Papers with Code - Distribution Shift](https://paperswithcode.com/task/domain-adaptation)**
   - Estado del arte en domain adaptation

### 🛠️ Herramientas Útiles

| Tool | Propósito |
|------|-----------|
| [Evidently AI](https://github.com/evidentlyai/evidently) | Monitoreo de drift en producción |
| [Great Expectations](https://greatexpectations.io/) | Validación de calidad de datos |
| [MLflow](https://mlflow.org/) | Tracking de experimentos y versiones |
| [Weights & Biases](https://wandb.ai/) | Monitoreo de modelos en producción |

### ⚙️ Configuración de Monitoreo

```python
# Integración con Evidently AI para drift detection
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference_data=X_train, current_data=X_production)
dashboard.save("drift_report.html")
```

---

## ✅ Checklist Final

Antes de deployar tu modelo, verifica:

### Pre-Training
- [ ] Features no contienen información del futuro
- [ ] No hay features derivadas del target
- [ ] Dataset libre de duplicados
- [ ] División estratificada correcta (70/15/15)

### During Training
- [ ] Scaler/encoder entrenado solo con training
- [ ] Hiperparámetros ajustados con validation
- [ ] Test set NO tocado durante desarrollo

### Post-Training
- [ ] Validaciones anti-leakage ejecutadas
- [ ] Análisis de drift completado
- [ ] Correlaciones de features verificadas
- [ ] Baseline statistics guardadas

### Production
- [ ] Sistema de monitoreo de drift configurado
- [ ] Alertas de performance decay activas
- [ ] Plan de re-entrenamiento definido
- [ ] A/B testing strategy para nuevas versiones

---

## 🎯 Conclusión

Los 4 problemas cubiertos (Data Leakage, Test Contamination, Drift, Hidden Leakage) son **responsables del 80% de los fallos de modelos en producción**.

Implementar estas validaciones **antes** de deployar puede ahorrar:
- ❌ Meses de trabajo de debugging
- ❌ Pérdida de confianza del usuario
- ❌ Costos de re-entrenamiento urgente

✅ **Un modelo bien validado hoy = un modelo confiable mañana**

---

**Autor**: URLytics ML Team  
**Última actualización**: 2025-11-15  
**Versión**: 1.0
