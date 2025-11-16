#!/usr/bin/env python3
"""
Script de Verificación de Instalación
======================================
Verifica que todas las librerías necesarias estén instaladas correctamente.
"""

import sys

def check_imports():
    """Verifica que todas las librerías se puedan importar"""
    print("🔍 Verificando instalación de librerías...\n")
    print("="*70)
    
    libraries = {
        'Core ML': [
            ('sklearn', 'scikit-learn'),
            ('numpy', 'numpy'),
            ('pandas', 'pandas'),
            ('scipy', 'scipy'),
        ],
        'Persistence': [
            ('joblib', 'joblib'),
        ],
        'Data': [
            ('kagglehub', 'kagglehub'),
        ],
        'Visualization': [
            ('matplotlib', 'matplotlib'),
            ('seaborn', 'seaborn'),
        ],
        'Web': [
            ('flask', 'flask'),
            ('flask_cors', 'flask-cors'),
        ],
        'Notebook': [
            ('jupyter', 'jupyter'),
            ('notebook', 'notebook'),
            ('ipykernel', 'ipykernel'),
        ],
    }
    
    all_ok = True
    
    for category, libs in libraries.items():
        print(f"\n📦 {category}:")
        for module_name, package_name in libs:
            try:
                module = __import__(module_name)
                version = getattr(module, '__version__', 'N/A')
                print(f"   ✅ {package_name:20s} v{version}")
            except ImportError as e:
                print(f"   ❌ {package_name:20s} - NO INSTALADO")
                all_ok = False
    
    print("\n" + "="*70)
    
    if all_ok:
        print("\n🎉 ¡TODAS LAS LIBRERÍAS ESTÁN INSTALADAS CORRECTAMENTE!")
        print("\n💡 Próximo paso: Ejecutar train.ipynb")
        return 0
    else:
        print("\n⚠️  ALGUNAS LIBRERÍAS NO ESTÁN INSTALADAS")
        print("\n💡 Solución:")
        print("   1. Activar el entorno virtual: source venv/bin/activate")
        print("   2. Instalar requirements: pip install -r requirements.txt")
        return 1

def check_python_version():
    """Verifica la versión de Python"""
    print("\n🐍 Información de Python:")
    print(f"   Versión: {sys.version}")
    print(f"   Ejecutable: {sys.executable}")
    
    if sys.version_info < (3, 8):
        print("\n⚠️  Python 3.8+ recomendado")
        return False
    return True

def check_functionality():
    """Prueba funcionalidad básica"""
    print("\n🧪 Probando funcionalidad básica...\n")
    
    try:
        import numpy as np
        arr = np.array([1, 2, 3, 4, 5])
        print(f"   ✅ NumPy: Array creado - {arr}")
    except Exception as e:
        print(f"   ❌ NumPy: Error - {e}")
        return False
    
    try:
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print(f"   ✅ Pandas: DataFrame {df.shape}")
    except Exception as e:
        print(f"   ❌ Pandas: Error - {e}")
        return False
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10)
        print(f"   ✅ Scikit-learn: RandomForest con {model.n_estimators} estimadores")
    except Exception as e:
        print(f"   ❌ Scikit-learn: Error - {e}")
        return False
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        print(f"   ✅ Matplotlib: Figura creada")
        plt.close(fig)
    except Exception as e:
        print(f"   ❌ Matplotlib: Error - {e}")
        return False
    
    print("\n   🎉 ¡Todas las pruebas pasaron!")
    return True

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🛡️  SOCIALGUARD ML v2.0 - Verificación de Instalación   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Verificar imports
    result = check_imports()
    
    # Si todo OK, probar funcionalidad
    if result == 0:
        if not check_functionality():
            result = 1
    
    print("\n" + "="*70)
    
    if result == 0:
        print("""
    ✅ INSTALACIÓN VERIFICADA EXITOSAMENTE
    
    🚀 Pasos siguientes:
    
    1. Ejecutar el notebook mejorado:
       jupyter notebook train.ipynb
    
    2. O ejecutar el script de drift monitoring:
       python drift_monitoring_example.py
    
    3. Leer la documentación:
       - INICIO_RAPIDO.md
       - ML_BEST_PRACTICES.md
        """)
    else:
        print("""
    ❌ PROBLEMAS DETECTADOS EN LA INSTALACIÓN
    
    💡 Soluciones:
    
    1. Asegúrate de tener el entorno virtual activado:
       source venv/bin/activate
    
    2. Reinstala los paquetes:
       pip install -r requirements.txt
    
    3. Si persiste el error, recrea el entorno virtual:
       rm -rf venv
       python -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt
        """)
    
    print("="*70 + "\n")
    sys.exit(result)
