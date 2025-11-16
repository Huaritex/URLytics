from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json
import os
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# =====================================================
# 🛡️ URLytics API - Phishing Detection
# =====================================================
# Versión 2.0 - Modelo mejorado con normalización
# =====================================================

# Rutas a los artefactos del modelo entrenado
MODEL_DIR = 'phishing_model_artefacts'
MODEL_PATH = os.path.join(MODEL_DIR, 'phishing_model_rf.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.joblib')
FEATURES_PATH = os.path.join(MODEL_DIR, 'features.json')
METRICS_PATH = os.path.join(MODEL_DIR, 'model_metrics.json')

# Validar que existan los archivos
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Modelo no encontrado: {MODEL_PATH}")
if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"❌ Scaler no encontrado: {SCALER_PATH}")

# Cargar modelo y artefactos
print(f"📦 Cargando modelo desde {MODEL_PATH}...")
model = joblib.load(MODEL_PATH)
print(f"✅ Modelo cargado: {model.n_estimators} estimadores, {model.n_features_in_} features")

print(f"📐 Cargando scaler desde {SCALER_PATH}...")
scaler = joblib.load(SCALER_PATH)
print(f"✅ Scaler cargado: {len(scaler.mean_)} features")

# Cargar lista de features
with open(FEATURES_PATH, 'r') as f:
    FEATURES = json.load(f)
print(f"📋 Features cargadas: {FEATURES}")

# Cargar métricas del modelo (para información)
with open(METRICS_PATH, 'r') as f:
    MODEL_METRICS = json.load(f)
print(f"📊 Métricas del modelo:")
print(f"   • Test Accuracy: {MODEL_METRICS['test_metrics']['accuracy']:.2%}")
print(f"   • Test Precision: {MODEL_METRICS['test_metrics']['precision']:.2%}")
print(f"   • Test Recall: {MODEL_METRICS['test_metrics']['recall']:.2%}")
print(f"   • Test F1-Score: {MODEL_METRICS['test_metrics']['f1_score']:.4f}")
print(f"\n✅ API lista para recibir peticiones\n")

def extract_features_from_text(text):
    """
    Extrae las 6 features de phishing de una URL o texto.
    
    Features:
    - Abnormal_URL: Detecta patrones anormales
    - Prefix_Suffix: Uso de guiones en dominio
    - SSLfinal_State: Certificado SSL/TLS
    - Shortining_Service: Acortadores de URL
    - having_At_Symbol: Símbolo '@' en URL
    - having_Sub_Domain: Número de subdominios
    
    Args:
        text (str): URL o texto a analizar
    
    Returns:
        pd.DataFrame: DataFrame con las features extraídas
    """
    features = {}
    
    # 1. Abnormal_URL: 1 si la URL tiene patrones sospechosos
    # (IP en lugar de dominio, URL muy larga, etc.)
    is_abnormal = 0
    if any(char.isdigit() for char in text[:20]):  # Dígitos al inicio
        is_abnormal = 1
    if len(text) > 100:  # URL muy larga
        is_abnormal = 1
    features['Abnormal_URL'] = is_abnormal
    
    # 2. Prefix_Suffix: 1 si hay guiones en el dominio
    features['Prefix_Suffix'] = int('-' in text.split('//')[0] if '//' in text else '-' in text[:30])
    
    # 3. SSLfinal_State: -1 (sin HTTPS), 0 (HTTPS dudoso), 1 (HTTPS válido)
    # En este caso simplificado: 1 si empieza con https, -1 si no
    if text.startswith('https://'):
        features['SSLfinal_State'] = 1
    elif text.startswith('http://'):
        features['SSLfinal_State'] = -1
    else:
        features['SSLfinal_State'] = 0
    
    # 4. Shortining_Service: 1 si usa acortador de URL
    shorteners = ['bit.ly', 'goo.gl', 'tinyurl', 'ow.ly', 't.co', 'is.gd', 'buff.ly', 'adf.ly']
    features['Shortining_Service'] = int(any(short in text.lower() for short in shorteners))
    
    # 5. having_At_Symbol: 1 si tiene '@' (técnica de phishing)
    features['having_At_Symbol'] = int('@' in text)
    
    # 6. having_Sub_Domain: Cuenta subdominios (0, 1, 2+)
    # Extraer dominio
    domain_part = text
    if '//' in text:
        domain_part = text.split('//')[1].split('/')[0]
    
    # Contar puntos (subdominios)
    dot_count = domain_part.count('.')
    if dot_count <= 1:
        features['having_Sub_Domain'] = 0  # ejemplo.com
    elif dot_count == 2:
        features['having_Sub_Domain'] = 1  # www.ejemplo.com
    else:
        features['having_Sub_Domain'] = 2  # sub.sub.ejemplo.com (sospechoso)
    
    # Crear DataFrame con el orden correcto de features
    feature_vector = [features[f] for f in FEATURES]
    return pd.DataFrame([feature_vector], columns=FEATURES)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint principal para predicción de phishing.
    
    Request JSON:
        {
            "text": "https://ejemplo.com/url-a-analizar"
        }
    
    Response JSON:
        {
            "prediction": 0 o 1 (0=legítimo, 1=phishing),
            "confidence": 0.0-1.0,
            "risk_level": "low", "medium" o "high",
            "features": {...},
            "timestamp": "ISO-8601"
        }
    """
    try:
        # Validar request
        data = request.json
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Campo "text" requerido',
                'example': {'text': 'https://ejemplo.com'}
            }), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'El campo "text" no puede estar vacío'}), 400
        
        # 1. Extraer features
        X = extract_features_from_text(text)
        
        # 2. Normalizar features con el scaler entrenado
        X_scaled = scaler.transform(X)
        
        # 3. Predecir
        prediction_proba = model.predict_proba(X_scaled)[0]
        prediction = int(model.predict(X_scaled)[0])
        
        # 4. Calcular confianza y nivel de riesgo
        confidence = float(prediction_proba[prediction])
        
        # Nivel de riesgo basado en probabilidad de phishing
        phishing_prob = float(prediction_proba[1])
        if phishing_prob < 0.3:
            risk_level = "low"
        elif phishing_prob < 0.7:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        # 5. Preparar respuesta
        response = {
            'prediction': prediction,
            'prediction_label': 'phishing' if prediction == 1 else 'legitimate',
            'confidence': round(confidence, 4),
            'phishing_probability': round(phishing_prob, 4),
            'risk_level': risk_level,
            'features': {
                feat: int(X[feat].values[0]) for feat in FEATURES
            },
            'timestamp': datetime.now().isoformat(),
            'analyzed_text': text[:100] + '...' if len(text) > 100 else text
        }
        
        # Log (opcional - descomentar para debugging)
        # print(f"[{response['timestamp']}] Prediction: {prediction}, Confidence: {confidence:.2%}, URL: {text[:50]}")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error en predicción: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de health check para verificar que la API está funcionando.
    """
    return jsonify({
        'status': 'healthy',
        'model': {
            'n_estimators': model.n_estimators,
            'n_features': model.n_features_in_,
            'features': FEATURES
        },
        'metrics': {
            'test_accuracy': MODEL_METRICS['test_metrics']['accuracy'],
            'test_precision': MODEL_METRICS['test_metrics']['precision'],
            'test_recall': MODEL_METRICS['test_metrics']['recall'],
            'test_f1': MODEL_METRICS['test_metrics']['f1_score']
        },
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/info', methods=['GET'])
def info():
    """
    Endpoint para obtener información sobre el modelo y sus características.
    """
    feature_importance = MODEL_METRICS.get('feature_importance', {})
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    return jsonify({
        'model_info': {
            'algorithm': 'Random Forest',
            'version': '2.0',
            'n_estimators': model.n_estimators,
            'training_samples': MODEL_METRICS['training_info']['training_samples']
        },
        'features': FEATURES,
        'feature_importance': dict(sorted_features),
        'performance': MODEL_METRICS['test_metrics'],
        'last_updated': MODEL_METRICS['training_info'].get('created_date', 'N/A')
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)