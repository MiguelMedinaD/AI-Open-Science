import os
import requests
import time
import sys

def run_tester():
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    success = True

    # Test 1: Versión de la API
    version_url = f"{base_url}/api/version"
    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            version = response.text.strip()
            print("Versión de la API:", version)
            if version != "0.8.1":
                print("Test fallido: se esperaba '0.8.1'.")
                success = False
        else:
            print("Error en /api/version. Código:", response.status_code)
            success = False
    except Exception as e:
        print("Excepción en /api/version:", e)
        success = False

    # Test 2: Estado isalive
    isalive_url = f"{base_url}/api/isalive"
    try:
        response = requests.get(isalive_url)
        if response.status_code == 200:
            is_alive = response.text.strip().lower()
            print("Resultado de /api/isalive:", is_alive)
            if is_alive != "true":
                print("Test fallido: se esperaba 'true'.")
                success = False
        else:
            print("Error en /api/isalive. Código:", response.status_code)
            success = False
    except Exception as e:
        print("Excepción en /api/isalive:", e)
        success = False

    return success

if __name__ == "__main__":
    i = 0
    delay = 10
    while not run_tester():

        print(f"Intento {i+1}: Comprobando endpoints de la API...")
        i = i + 1

        print(f"{'-' * 20} \nError en las pruebas unitarias.\n{'-' * 20}")

        print(f"Esperando {delay} segundos antes del siguiente intento...\n")

        time.sleep(delay)

    print("Pruebas unitarias completadas exitosamente.")
    print("Ejecutando los siguientes archivos, espere...")
    sys.exit(0)
