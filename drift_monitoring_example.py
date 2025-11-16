"""
🛡️ URLytics - Drift Monitoring Example
===========================================

Este script proporciona funciones helper para detectar drift en producción.
Usar este código en tu API/aplicación para monitorear la salud del modelo.

Autor: URLytics ML Team
Versión: 2.0
Fecha: 2025-11-15
"""

import json
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def load_baseline(baseline_path='baseline_statistics.json'):
    """
    Carga las estadísticas baseline del modelo.
    
    Args:
        baseline_path: Path al archivo baseline_statistics.json
    
    Returns:
        dict: Estadísticas baseline
    """
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    return baseline


def check_drift_simple(new_data, baseline_path='baseline_statistics.json', threshold=0.5):
    """
    Detecta drift comparando estadísticas simples (media y std).
    Útil cuando no tienes acceso a los datos raw de training.
    
    Args:
        new_data: DataFrame con nuevas predicciones (features)
        baseline_path: Path al archivo baseline_statistics.json
        threshold: Umbral de cambio relativo (default: 0.5 = 50%)
    
    Returns:
        dict: Resultados del análisis de drift
    """
    baseline = load_baseline(baseline_path)
    
    drift_results = {
        'timestamp': datetime.now().isoformat(),
        'drift_detected': False,
        'features_with_drift': [],
        'statistics': {},
        'severity': 'NONE'
    }
    
    drift_count = 0
    
    for feature, stats in baseline['feature_statistics'].items():
        if feature not in new_data.columns:
            continue
        
        # Estadísticas baseline
        baseline_mean = stats['mean']
        baseline_std = stats['std']
        
        # Estadísticas actuales
        current_mean = new_data[feature].mean()
        current_std = new_data[feature].std()
        
        # Calcular cambio relativo
        mean_change = abs(current_mean - baseline_mean) / (abs(baseline_std) + 1e-10)
        std_change = abs(current_std - baseline_std) / (abs(baseline_std) + 1e-10)
        
        drift_results['statistics'][feature] = {
            'baseline_mean': baseline_mean,
            'current_mean': current_mean,
            'mean_change': mean_change,
            'baseline_std': baseline_std,
            'current_std': current_std,
            'std_change': std_change,
            'drift_detected': False
        }
        
        # Detectar drift
        if mean_change > threshold or std_change > threshold:
            drift_results['drift_detected'] = True
            drift_results['features_with_drift'].append(feature)
            drift_results['statistics'][feature]['drift_detected'] = True
            drift_count += 1
    
    # Determinar severidad
    total_features = len(baseline['feature_statistics'])
    drift_ratio = drift_count / total_features if total_features > 0 else 0
    
    if drift_ratio == 0:
        drift_results['severity'] = 'NONE'
    elif drift_ratio < 0.2:
        drift_results['severity'] = 'LOW'
    elif drift_ratio < 0.5:
        drift_results['severity'] = 'MODERATE'
    else:
        drift_results['severity'] = 'HIGH'
    
    return drift_results


def check_drift_ks_test(new_data, baseline_samples, threshold=0.05):
    """
    Detecta drift usando test de Kolmogorov-Smirnov.
    Más robusto pero requiere datos raw de training.
    
    Args:
        new_data: DataFrame con nuevas predicciones (features)
        baseline_samples: DataFrame con samples de training (para KS test)
        threshold: p-value threshold (default: 0.05)
    
    Returns:
        dict: Resultados del análisis de drift con KS test
    """
    drift_results = {
        'timestamp': datetime.now().isoformat(),
        'drift_detected': False,
        'features_with_drift': [],
        'ks_statistics': {},
        'severity': 'NONE'
    }
    
    drift_count = 0
    
    for feature in baseline_samples.columns:
        if feature not in new_data.columns:
            continue
        
        # Test de Kolmogorov-Smirnov
        ks_stat, p_value = ks_2samp(
            baseline_samples[feature].dropna(),
            new_data[feature].dropna()
        )
        
        drift_results['ks_statistics'][feature] = {
            'ks_statistic': float(ks_stat),
            'p_value': float(p_value),
            'drift_detected': p_value < threshold
        }
        
        if p_value < threshold:
            drift_results['drift_detected'] = True
            drift_results['features_with_drift'].append(feature)
            drift_count += 1
    
    # Determinar severidad
    total_features = len(baseline_samples.columns)
    drift_ratio = drift_count / total_features if total_features > 0 else 0
    
    if drift_ratio == 0:
        drift_results['severity'] = 'NONE'
    elif drift_ratio < 0.2:
        drift_results['severity'] = 'LOW'
    elif drift_ratio < 0.5:
        drift_results['severity'] = 'MODERATE'
    else:
        drift_results['severity'] = 'HIGH'
    
    return drift_results


def check_performance_decay(current_metrics, baseline_path='baseline_statistics.json', threshold=0.10):
    """
    Detecta decay en performance del modelo.
    Requiere ground truth de datos de producción.
    
    Args:
        current_metrics: dict con métricas actuales {'accuracy': 0.92, 'f1': 0.91, ...}
        baseline_path: Path al archivo baseline_statistics.json
        threshold: Umbral de decay aceptable (default: 0.10 = 10%)
    
    Returns:
        dict: Resultados del análisis de performance
    """
    baseline = load_baseline(baseline_path)
    baseline_perf = baseline['performance_baseline']
    
    decay_results = {
        'timestamp': datetime.now().isoformat(),
        'decay_detected': False,
        'metrics_with_decay': [],
        'comparison': {}
    }
    
    for metric, current_value in current_metrics.items():
        if metric not in baseline_perf:
            continue
        
        baseline_value = baseline_perf[metric]
        decay = baseline_value - current_value
        decay_pct = (decay / baseline_value) if baseline_value > 0 else 0
        
        decay_results['comparison'][metric] = {
            'baseline': baseline_value,
            'current': current_value,
            'decay': decay,
            'decay_percentage': decay_pct,
            'threshold_exceeded': decay_pct > threshold
        }
        
        if decay_pct > threshold:
            decay_results['decay_detected'] = True
            decay_results['metrics_with_decay'].append(metric)
    
    return decay_results


def should_retrain(drift_results, performance_results=None):
    """
    Determina si el modelo necesita re-entrenamiento basado en drift y performance.
    
    Args:
        drift_results: Resultados de check_drift_simple() o check_drift_ks_test()
        performance_results: Resultados de check_performance_decay() (opcional)
    
    Returns:
        dict: Recomendación de re-entrenamiento
    """
    recommendation = {
        'should_retrain': False,
        'urgency': 'NONE',
        'reason': [],
        'action': 'Continue monitoring'
    }
    
    # Analizar drift
    if drift_results['drift_detected']:
        severity = drift_results['severity']
        
        if severity == 'HIGH':
            recommendation['should_retrain'] = True
            recommendation['urgency'] = 'URGENT'
            recommendation['reason'].append(f"High drift detected in {len(drift_results['features_with_drift'])} features")
            recommendation['action'] = 'Retrain immediately (within 1-2 days)'
        
        elif severity == 'MODERATE':
            recommendation['should_retrain'] = True
            recommendation['urgency'] = 'MEDIUM'
            recommendation['reason'].append(f"Moderate drift detected in {len(drift_results['features_with_drift'])} features")
            recommendation['action'] = 'Schedule retraining (within 1 week)'
        
        elif severity == 'LOW':
            recommendation['urgency'] = 'LOW'
            recommendation['reason'].append(f"Low drift detected in {len(drift_results['features_with_drift'])} features")
            recommendation['action'] = 'Monitor closely, consider retraining if persists'
    
    # Analizar performance decay (si está disponible)
    if performance_results and performance_results['decay_detected']:
        recommendation['should_retrain'] = True
        
        max_decay = max([
            comp['decay_percentage'] 
            for comp in performance_results['comparison'].values()
        ])
        
        if max_decay > 0.15:  # 15% decay
            recommendation['urgency'] = 'URGENT'
            recommendation['reason'].append(f"Severe performance decay detected (>{max_decay*100:.1f}%)")
            recommendation['action'] = 'Retrain immediately'
        else:
            if recommendation['urgency'] == 'NONE':
                recommendation['urgency'] = 'MEDIUM'
            recommendation['reason'].append(f"Performance decay detected (>{max_decay*100:.1f}%)")
    
    return recommendation


def generate_drift_report(drift_results, performance_results=None, output_file='drift_report.json'):
    """
    Genera un reporte completo de drift para logging/alertas.
    
    Args:
        drift_results: Resultados de drift detection
        performance_results: Resultados de performance check (opcional)
        output_file: Path para guardar el reporte
    
    Returns:
        dict: Reporte completo
    """
    report = {
        'timestamp': datetime.now().isoformat(),
        'drift_analysis': drift_results,
        'performance_analysis': performance_results,
        'recommendation': should_retrain(drift_results, performance_results)
    }
    
    # Guardar reporte
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    return report


# =====================================================
# EJEMPLO DE USO
# =====================================================

if __name__ == '__main__':
    print("🔍 URLytics Drift Monitoring - Ejemplo de Uso\n")
    print("="*70)
    
    # Simular datos de producción (reemplazar con datos reales)
    print("\n1. Simulando datos de producción...")
    production_data = pd.DataFrame({
        'Abnormal_URL': np.random.randint(-1, 2, 1000),
        'Prefix_Suffix': np.random.randint(-1, 2, 1000),
        'SSLfinal_State': np.random.randint(-1, 2, 1000),
        'Shortining_Service': np.random.randint(-1, 2, 1000),
        'having_At_Symbol': np.random.randint(-1, 2, 1000),
        'having_Sub_Domain': np.random.randint(-3, 2, 1000)
    })
    print(f"   ✅ {len(production_data)} muestras de producción generadas")
    
    # Detectar drift (método simple)
    print("\n2. Detectando drift...")
    try:
        drift_info = check_drift_simple(
            production_data,
            baseline_path='baseline_statistics.json',
            threshold=0.5
        )
        
        print(f"\n   Drift detectado: {'🚨 SÍ' if drift_info['drift_detected'] else '✅ NO'}")
        print(f"   Severidad: {drift_info['severity']}")
        
        if drift_info['features_with_drift']:
            print(f"   Features con drift: {drift_info['features_with_drift']}")
        
    except FileNotFoundError:
        print("   ⚠️  baseline_statistics.json no encontrado")
        print("   💡 Ejecutar train.ipynb para generar baseline")
        drift_info = None
    
    # Simular métricas de performance (reemplazar con métricas reales)
    print("\n3. Verificando performance...")
    current_metrics = {
        'test_accuracy': 0.92,  # Simular accuracy actual
        'test_f1': 0.91,        # Simular F1 actual
        'test_roc_auc': 0.93    # Simular ROC-AUC actual
    }
    
    try:
        perf_info = check_performance_decay(
            current_metrics,
            threshold=0.10
        )
        
        print(f"\n   Performance decay: {'🚨 SÍ' if perf_info['decay_detected'] else '✅ NO'}")
        
        if perf_info['metrics_with_decay']:
            print(f"   Métricas con decay: {perf_info['metrics_with_decay']}")
        
    except (FileNotFoundError, KeyError):
        print("   ⚠️  Baseline no encontrado o incompleto")
        perf_info = None
    
    # Generar recomendación
    if drift_info:
        print("\n4. Generando recomendación...")
        recommendation = should_retrain(drift_info, perf_info)
        
        print(f"\n   ¿Debe re-entrenar?: {'🚨 SÍ' if recommendation['should_retrain'] else '✅ NO'}")
        print(f"   Urgencia: {recommendation['urgency']}")
        print(f"   Acción: {recommendation['action']}")
        
        if recommendation['reason']:
            print(f"\n   Razones:")
            for reason in recommendation['reason']:
                print(f"      • {reason}")
        
        # Generar reporte
        print("\n5. Generando reporte...")
        report = generate_drift_report(drift_info, perf_info)
        print(f"   ✅ Reporte guardado: drift_report.json")
    
    print("\n" + "="*70)
    print("\n💡 PRÓXIMOS PASOS:")
    print("   1. Integrar este código en tu API/aplicación")
    print("   2. Ejecutar check_drift() periódicamente (diario/semanal)")
    print("   3. Configurar alertas cuando drift_detected = True")
    print("   4. Re-entrenar modelo cuando sea necesario")
    print("\n" + "="*70)
