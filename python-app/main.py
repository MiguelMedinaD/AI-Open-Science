import requests
import time
import os

def main():
    url = os.environ.get("GROBID_URL", "http://grobid:8070")
    retries = 10  # número de intentos
    delay = 10    # segundos entre cada intento

    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("¡La página de bienvenida de GROBID se ha accedido correctamente!")
                return
            else:
                print(f"Intento {i+1}: Error al acceder, código de estado: {response.status_code}")
        except Exception as e:
            print(f"Intento {i+1}: Excepción al intentar acceder a GROBID: {e}")
        time.sleep(delay)
    print("No se pudo acceder a GROBID después de varios intentos.")

if __name__ == "__main__":
    main()
