#!/usr/bin/env python3
"""
🧪 Script de prueba para la API de URLytics
================================================
Prueba el modelo de detección de phishing con varios ejemplos.
"""

import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

API_URL = "http://localhost:5000"

def test_predict(url, description=""):
    """Prueba la API con una URL específica"""
    print(f"\n{'='*70}")
    print(f"🔍 {description if description else 'Prueba'}")
    print(f"{'='*70}")
    print(f"📎 URL: {url}")
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": url},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Determinar color según predicción
            if data['prediction'] == 1:
                color = Fore.RED
                label = "🚨 PHISHING"
            else:
                color = Fore.GREEN
                label = "✅ LEGÍTIMO"
            
            print(f"\n{color}{Style.BRIGHT}{label}{Style.RESET_ALL}")
            print(f"   • Confianza: {data['confidence']*100:.2f}%")
            print(f"   • Probabilidad de phishing: {data['phishing_probability']*100:.2f}%")
            print(f"   • Nivel de riesgo: {data['risk_level'].upper()}")
            
            print(f"\n📊 Features detectadas:")
            for feature, value in data['features'].items():
                emoji = "⚠️ " if value != 0 else "  "
                print(f"   {emoji}{feature:25s}: {value}")
            
        else:
            print(f"{Fore.RED}❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error de conexión: {e}")


def test_health():
    """Prueba el endpoint de health"""
    print(f"\n{'='*70}")
    print(f"🏥 Health Check")
    print(f"{'='*70}")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"{Fore.GREEN}✅ API funcionando correctamente")
            print(f"\n📊 Métricas del modelo:")
            print(f"   • Accuracy:  {data['metrics']['test_accuracy']*100:.2f}%")
            print(f"   • Precision: {data['metrics']['test_precision']*100:.2f}%")
            print(f"   • Recall:    {data['metrics']['test_recall']*100:.2f}%")
            print(f"   • F1-Score:  {data['metrics']['test_f1']:.4f}")
        else:
            print(f"{Fore.RED}❌ Error {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}❌ No se puede conectar a la API: {e}")
        print(f"\n💡 Asegúrate de que la API esté corriendo con: python api.py")
        return False
    return True


def main():
    """Ejecuta todas las pruebas"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print(f"{'='*70}")
    print(f"🛡️  URLYTICS - PRUEBAS DE API DE DETECCIÓN DE PHISHING")
    print(f"{'='*70}")
    print(f"{Style.RESET_ALL}")
    
    # 1. Health check
    if not test_health():
        return
    
    # 2. Pruebas con URLs legítimas
    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*70}")
    print(f"✅ PRUEBAS CON URLs LEGÍTIMAS")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    test_predict("https://www.google.com", "URL legítima - Google")
    test_predict("https://github.com/usuario/proyecto", "URL legítima - GitHub")
    test_predict("https://stackoverflow.com/questions/123", "URL legítima - Stack Overflow")
    
    # 3. Pruebas con URLs de phishing
    print(f"\n{Fore.RED}{Style.BRIGHT}{'='*70}")
    print(f"🚨 PRUEBAS CON URLs SOSPECHOSAS/PHISHING")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    test_predict("http://paypal-secure-login@malicious.com", "Phishing - Símbolo @ sospechoso")
    test_predict("https://bit.ly/3xYz123", "Sospechoso - Acortador de URL")
    test_predict("http://www-paypal-verify.suspicious-domain.com", "Phishing - Dominio sospechoso con guiones")
    test_predict("https://192.168.1.100/login.php", "Sospechoso - IP en lugar de dominio")
    test_predict("http://secure.bank-login-verify-account.xyz", "Phishing - Múltiples subdominios + HTTP")
    
    # Resumen final
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"✅ PRUEBAS COMPLETADAS")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"\n💡 Para más información sobre el modelo:")
    print(f"   curl http://localhost:5000/info\n")


if __name__ == "__main__":
    main()
