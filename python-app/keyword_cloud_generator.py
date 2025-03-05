import os
import time
import re
import requests
import xml.etree.ElementTree as ET
from wordcloud import WordCloud
import sys

def generate_keyword_cloud(text, output_folder):
    """Genera una nube de palabras a partir del texto del abstract y la guarda como 'keyword_cloud.png'."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    output_path = os.path.join(output_folder, "keyword_cloud.png")
    wordcloud.to_file(output_path)
    print(f"Keyword cloud guardado en: {output_path}")

def extract_abstract_from_xml(tei_xml):
    """Extrae el contenido del abstract a partir del TEI XML."""
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
    """Extrae el campo abstract del texto en formato BibTeX."""
    match = re.search(r'abstract\s*=\s*\{(.*?)\}', bibtex_text, re.DOTALL | re.IGNORECASE)
    if match:
        abstract_text = match.group(1).strip()
        return abstract_text
    else:
        print("No se encontró el campo 'abstract' en el BibTeX.")
    return None

def process_pdf_generate_keyword_cloud(pdf_path, base_url, output_folder):
    """
    Envía el PDF al endpoint /api/processHeaderDocument de Grobid para obtener el TEI XML,
    guarda el XML en output_folder y genera una keyword cloud a partir del abstract.
    """
    url = f"{base_url}/api/processHeaderDocument"
    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {"input": pdf_file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            response_text = response.text
            
            # Guarda el TEI XML en un archivo
            tei_output_path = os.path.join(output_folder, "tei.xml")
            with open(tei_output_path, "w", encoding="utf-8") as f:
                f.write(response_text)
            print(f"TEI XML guardado en: {tei_output_path}")
            
            abstract_text = None
            if response_text.lstrip().startswith("<"):
                abstract_text = extract_abstract_from_xml(response_text)
            elif response_text.lstrip().startswith("@"):
                abstract_text = extract_abstract_from_bibtex(response_text)
            else:
                print("Formato de respuesta desconocido.")
            
            if abstract_text:
                print("Texto del abstract extraído.")
                generate_keyword_cloud(abstract_text, output_folder)
            else:
                print("No se pudo extraer el abstract.")
        else:
            print("Error en el procesamiento del PDF. Código:", response.status_code)
            print(response.text)
    except Exception as e:
        print("Excepción al enviar el PDF:", e)

def main():
    """
    Procesa todos los archivos PDF en el directorio definido por PDF_FOLDER.
    Para cada PDF se crea una carpeta (con el mismo nombre del archivo sin extensión)
    y dentro de ella se crea la carpeta 'keyword_cloud', donde se guardan los resultados:
    el TEI XML y la imagen de la keyword cloud.
    Si ya existen ambos archivos en dicha carpeta, se omite el procesamiento para ese PDF.
    """
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    pdf_folder = os.environ.get("PDF_FOLDER", "/app/pdfs")
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No se encontraron archivos PDF en el directorio {pdf_folder}.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        # Se crea la carpeta 'keyword_cloud' dentro de la carpeta del PDF
        output_folder = os.path.join(pdf_folder, base_name, "keyword_cloud")
        
        tei_file = os.path.join(output_folder, "tei.xml")
        keyword_cloud_file = os.path.join(output_folder, "keyword_cloud.png")
        if os.path.exists(tei_file) and os.path.exists(keyword_cloud_file):
            print(f"Resultados ya generados para {pdf_file}. Se omite el procesamiento.")
            continue

        os.makedirs(output_folder, exist_ok=True)
        print(f"\nProcesando el archivo PDF: {pdf_path}")
        process_pdf_generate_keyword_cloud(pdf_path, base_url, output_folder)

if __name__ == "__main__":
    print("Ejecutando archivo keyword_cloud_generator.py")
    main()
    print("Ejecutando los siguientes archivos, espere...")
    sys.exit(0)
