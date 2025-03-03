import requests
import time
import os

def check_api_version(base_url):
    version_url = f"{base_url}/api/version"
    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            version = response.text.strip()
            print("Versión de la API:", version)
            return True
        else:
            print("Error al acceder a /api/version. Código de estado:", response.status_code)
    except Exception as e:
        print("Excepción al acceder a /api/version:", e)
    return False

def check_api_isalive(base_url):
    isalive_url = f"{base_url}/api/isalive"
    try:
        response = requests.get(isalive_url)
        if response.status_code == 200:
            is_alive = response.text.strip().lower()
            print("Resultado de /api/isalive:", is_alive)
            return is_alive == "true"
        else:
            print("Error al acceder a /api/isalive. Código de estado:", response.status_code)
    except Exception as e:
        print("Excepción al acceder a /api/isalive:", e)
    return False

def main():
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    retries = 10  # número de intentos
    delay = 10    # segundos de espera entre intentos

    for i in range(retries):
        print(f"Intento {i+1}: Comprobando endpoints de la API...")
        version_ok = check_api_version(base_url)
        isalive_ok = check_api_isalive(base_url)
        if version_ok and isalive_ok:
            print("¡Ambos checks se han realizado correctamente!")
            return
        print(f"Esperando {delay} segundos antes del siguiente intento...\n")
        time.sleep(delay)
    
    print("No se pudo confirmar el correcto funcionamiento de la API después de varios intentos.")

if __name__ == "__main__":
    main()
