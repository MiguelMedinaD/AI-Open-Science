import os
import time
import re
import requests
import xml.etree.ElementTree as ET
from wordcloud import WordCloud

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

def tester():
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    retries = 10  # número de intentos
    delay = 10    # segundos de espera entre intentos

    for i in range(retries):
        print(f"Intento {i+1}: Comprobando endpoints de la API...")
        version_ok = check_api_version(base_url)
        isalive_ok = check_api_isalive(base_url)
        if version_ok and isalive_ok:
            print("¡Ambos checks se han realizado correctamente!")
            return True
        print(f"Esperando {delay} segundos antes del siguiente intento...\n")
        time.sleep(delay)
    
    print("No se pudo confirmar el correcto funcionamiento de la API después de varios intentos.")
    return False

def generate_keyword_cloud(text, output_folder):
    # Genera una nube de palabras a partir del texto del abstract
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    output_path = os.path.join(output_folder, "keyword_cloud.png")
    wordcloud.to_file(output_path)
    print(f"Keyword cloud guardado en: {output_path}")

def extract_abstract_from_xml(tei_xml):
    try:
        root = ET.fromstring(tei_xml)
        abstract_elem = root.find(".//abstract")
        if abstract_elem is not None:
            abstract_text = "".join(abstract_elem.itertext()).strip()
            return abstract_text
        else:
            print("No se encontró el elemento <abstract> en el TEI XML.")
    except ET.ParseError as e:
        print("Error al parsear el TEI XML:", e)
    return None

def extract_abstract_from_bibtex(bibtex_text):
    # Busca el campo abstract en el formato: abstract = {contenido}
    match = re.search(r'abstract\s*=\s*\{(.*?)\}', bibtex_text, re.DOTALL | re.IGNORECASE)
    if match:
        abstract_text = match.group(1).strip()
        return abstract_text
    else:
        print("No se encontró el campo 'abstract' en el BibTeX.")
    return None

def process_pdf_generate_keyword_cloud(pdf_path, base_url, output_folder):
    # Usamos el endpoint processHeaderDocument para extraer el abstract del PDF
    url = f"{base_url}/api/processHeaderDocument"
    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {"input": pdf_file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            response_text = response.text
            # print("Respuesta de Grobid:")
            # print(response_text)
            
            # Guarda el TEI XML en un archivo en el output_folder
            tei_output_path = os.path.join(output_folder, "tei.xml")
            with open(tei_output_path, "w", encoding="utf-8") as f:
                f.write(response_text)
            print(f"Respuesta de Grobid TEI XML guardado en: {tei_output_path}")
            
            abstract_text = None
            # Detectar si la respuesta es XML o BibTeX
            if response_text.lstrip().startswith("<"):
                abstract_text = extract_abstract_from_xml(response_text)
            elif response_text.lstrip().startswith("@"):
                abstract_text = extract_abstract_from_bibtex(response_text)
            else:
                print("Formato de respuesta desconocido.")
            
            if abstract_text:
                print("Texto del abstract extraído")
                # print(abstract_text)
                generate_keyword_cloud(abstract_text, output_folder)
            else:
                print("No se pudo extraer el abstract.")
        else:
            print("Error en el procesamiento del PDF. Código:", response.status_code)
            print(response.text)
    except Exception as e:
        print("Excepción al enviar el PDF:", e)

def main():
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    pdf_folder = os.environ.get("PDF_FOLDER", "/app/pdfs")
    
    # Recorrer todos los archivos PDF en el directorio
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No se encontraron archivos PDF en el directorio {pdf_folder}.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        # Crear una carpeta de salida para este PDF
        output_folder = os.path.join(pdf_folder, base_name)
        os.makedirs(output_folder, exist_ok=True)
        print(f"\nProcesando el archivo PDF: {pdf_path}")
        process_pdf_generate_keyword_cloud(pdf_path, base_url, output_folder)

if __name__ == "__main__":
    if tester():
        main()
