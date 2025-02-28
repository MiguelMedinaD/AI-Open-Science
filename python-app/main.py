import requests

def main():
    # Nota: Dentro del contenedor, se puede acceder al servicio 'grobid' por su nombre de servicio
    url = "http://grobid:8070"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("¡La página de bienvenida de GROBID se ha accedido correctamente!")
        else:
            print("Error al acceder a la página de bienvenida. Código de estado:", response.status_code)
    except Exception as e:
        print("Excepción al intentar acceder a GROBID:", e)

if __name__ == "__main__":
    main()
