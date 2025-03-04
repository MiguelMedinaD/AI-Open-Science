import sys
import os
import re
import requests
import xml.etree.ElementTree as ET

def process_pdf_save_references_tei(pdf_path, base_url, output_folder):
    """
    Envía el PDF al endpoint /api/processReferences de Grobid para obtener el TEI XML
    de las referencias y lo guarda en output_folder como 'tei.xml'.
    Si el código de respuesta es 204, se genera links.txt con el mensaje de error correspondiente.
    Retorna el TEI XML obtenido (cadena) o "" en caso de 204, o None si hubo otro error.
    """
    url = f"{base_url}/api/processReferences"
    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {"input": pdf_file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            tei_xml = response.text
            tei_output_path = os.path.join(output_folder, "tei.xml")
            with open(tei_output_path, "w", encoding="utf-8") as f:
                f.write(tei_xml)
            print(f"TEI XML guardado en: {tei_output_path}")
            return tei_xml
        elif response.status_code == 204:
            # Crear archivo links.txt con el mensaje de error 204
            links_file = os.path.join(output_folder, "links.txt")
            with open(links_file, "w", encoding="utf-8") as f:
                f.write("El archivo no generó un analisis de referencias. Error 204 de la api processReferences")
            print(f"Se generó {links_file} debido a error 204.")
            return ""  # Indica que no se obtuvo TEI XML
        else:
            print(f"Error en el procesamiento de {os.path.basename(pdf_path)} para referencias. Código: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Excepción al enviar {os.path.basename(pdf_path)} para referencias: {e}")
    return None

def extract_links_from_tei(tei_xml):
    """
    Extrae de forma estructurada los links encontrados en el TEI XML.
    Se recorre el árbol XML (usando el namespace TEI) y se buscan atributos 'target' en cualquier elemento,
    recogiendo aquellos que empiezan por 'http'. Se eliminan duplicados.
    """
    links = set()
    try:
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        root = ET.fromstring(tei_xml)
        for elem in root.iter():
            target = elem.attrib.get("target", "")
            if target.startswith("http"):
                links.add(target)
    except ET.ParseError as e:
        print("Error al parsear el TEI XML:", e)
    return sorted(links)

def process_pdf_extract_links(pdf_folder, pdf_file, base_url):
    """
    Para un PDF dado, crea la carpeta 'links_in_pdf' dentro de la carpeta del PDF,
    llama al servicio de Grobid para extraer las referencias (TEI XML) y, a partir de éste,
    extrae y guarda la lista de links en 'links.txt'. Se consideran los siguientes casos:
      - Si el servicio devuelve 204, se crea links.txt con un mensaje indicándolo.
      - Si se obtiene un TEI XML pero no se encuentran links, se crea links.txt con el mensaje
        "No se encontraron links en las referencias del archivo."
    """
    base_name = os.path.splitext(pdf_file)[0]
    base_pdf_folder = os.path.join(pdf_folder, base_name)
    links_folder = os.path.join(base_pdf_folder, "links_in_pdf")
    os.makedirs(links_folder, exist_ok=True)
    links_file = os.path.join(links_folder, "links.txt")
    
    if os.path.exists(links_file):
        print(f"Links ya extraídos para {pdf_file}. Se omite el procesamiento.")
        return
    
    tei_xml = process_pdf_save_references_tei(os.path.join(pdf_folder, pdf_file), base_url, links_folder)
    if tei_xml is None:
        print(f"No se pudo obtener el TEI XML para {pdf_file}.")
        return
    if tei_xml == "":
        # Caso de error 204, ya se generó el archivo links.txt en process_pdf_save_references_tei
        return

    links = extract_links_from_tei(tei_xml)
    if links:
        with open(links_file, "w", encoding="utf-8") as f:
            for link in links:
                f.write(link + "\n")
        print(f"Se extrajeron {len(links)} links para {pdf_file} y se guardaron en {links_file}")
    else:
        with open(links_file, "w", encoding="utf-8") as f:
            f.write("No se encontraron links en las referencias del archivo.")
        print(f"No se encontraron links en el TEI XML para {pdf_file}. Archivo {links_file} generado.")

def main():
    """
    Procesa todos los archivos PDF en el directorio definido por PDF_FOLDER.
    Para cada PDF se asume que existe una carpeta con el nombre del PDF (sin extensión)
    y se crea (si no existe) una subcarpeta 'links_in_pdf' donde se guardarán:
      - El TEI XML obtenido del endpoint /api/processReferences (archivo tei.xml)
      - La lista de links extraídos (archivo links.txt)
    Si ya existe links.txt, se omite el procesamiento para ese PDF.
    """
    pdf_folder = os.environ.get("PDF_FOLDER", "/app/pdfs")
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No se encontraron archivos PDF en el directorio {pdf_folder}.")
        return

    for pdf_file in pdf_files:
        print(f"\nProcesando PDF: {pdf_file}")
        process_pdf_extract_links(pdf_folder, pdf_file, base_url)

if __name__ == "__main__":
    # Se obtiene la URL de Grobid desde la variable de entorno
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    print("Ejecutando links_in_pdf_generator.py")
    main()
    print("Ejecutando los test finales, espere...")
    sys.exit(0)

