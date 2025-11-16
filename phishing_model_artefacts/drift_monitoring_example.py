
# =====================================================
# CÓDIGO PARA MONITOREO DE DRIFT EN PRODUCCIÓN
# =====================================================
# Usar este código en tu API/aplicación para detectar cuando
# necesitas re-entrenar el modelo
# =====================================================

import json
import numpy as np
from scipy.stats import ks_2samp

def check_drift(new_data, baseline_path='baseline_statistics.json', threshold=0.05):
    """
    Detecta drift en datos de producción comparando con baseline.

    Args:
        new_data: DataFrame con nuevas predicciones (features)
        baseline_path: Path al archivo baseline_statistics.json
        threshold: p-value threshold para KS test (default: 0.05)

    Returns:
        dict con resultados del análisis de drift
    """
    # Cargar baseline
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)

    drift_results = {
        'drift_detected': False,
        'features_with_drift': [],
        'statistics': {}
    }

    for feature in baseline['feature_statistics'].keys():
        if feature not in new_data.columns:
            continue

        # Obtener estadísticas baseline
        baseline_mean = baseline['feature_statistics'][feature]['mean']
        baseline_std = baseline['feature_statistics'][feature]['std']

        # Estadísticas actuales
        current_mean = new_data[feature].mean()
        current_std = new_data[feature].std()

        # Test de Kolmogorov-Smirnov (requiere datos raw, no solo stats)
        # En producción, acumular samples para hacer el test

        # Alerta simple: cambio >20% en media o desviación
        mean_change = abs(current_mean - baseline_mean) / (baseline_std + 1e-10)
        std_change = abs(current_std - baseline_std) / (baseline_std + 1e-10)

        drift_results['statistics'][feature] = {
            'baseline_mean': baseline_mean,
            'current_mean': current_mean,
            'mean_change': mean_change,
            'std_change': std_change
        }

        # Detectar drift
        if mean_change > 0.5 or std_change > 0.5:
            drift_results['drift_detected'] = True
            drift_results['features_with_drift'].append(feature)

    return drift_results

# EJEMPLO DE USO:
# new_predictions = pd.DataFrame(...)  # Tus datos de producción
# drift_info = check_drift(new_predictions)
# 
# if drift_info['drift_detected']:
#     print(f"⚠️ DRIFT DETECTADO en: {drift_info['features_with_drift']}")
#     print("💡 Considerar re-entrenamiento del modelo")
