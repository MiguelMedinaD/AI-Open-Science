import sys
import os
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def process_pdf_save_tei(pdf_path, base_url, output_folder):
    """
    Envía el PDF al endpoint /api/processFulltextDocument de Grobid para obtener el TEI XML
    y lo guarda en output_folder como 'tei.xml'.
    """
    url = f"{base_url}/api/processFulltextDocument"
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
        else:
            print(f"Error en el procesamiento de {os.path.basename(pdf_path)}. Código: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Excepción al enviar {os.path.basename(pdf_path)}: {e}")

def count_figures_in_tei(tei_file_path):
    """
    Lee el archivo TEI XML y cuenta el número de elementos <figure> usando el namespace TEI.
    """
    try:
        tree = ET.parse(tei_file_path)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        figures = root.findall(".//tei:figure", ns)
        return len(figures)
    except Exception as e:
        print(f"Error al contar figuras en {tei_file_path}: {e}")
        return 0

def generate_figures_summary(pdf_folder, output_image_path):
    """
    Recorre cada PDF del directorio pdf_folder, busca el archivo tei.xml en su subcarpeta 'pdf_full_text_document'
    y cuenta el número de figuras. Luego, genera un gráfico de barras con el número de figuras por artículo (usando
    el nombre base del PDF como etiqueta) y lo guarda en output_image_path.
    Se ordenan alfabéticamente los artículos para que la asociación sea correcta.
    """
    results = {}
    # Ordenar los archivos PDF para tener un orden consistente
    for filename in sorted(os.listdir(pdf_folder)):
        if filename.lower().endswith(".pdf"):
            base_name = os.path.splitext(filename)[0]
            tei_path = os.path.join(pdf_folder, base_name, "pdf_full_text_document", "tei.xml")
            if os.path.exists(tei_path):
                count = count_figures_in_tei(tei_path)
                results[base_name] = count
            else:
                print(f"No se encontró tei.xml para {filename} en la ruta esperada.")
    
    if results:
        # Ordenar los artículos alfabéticamente
        articles = sorted(results.keys())
        counts = [results[a] for a in articles]
        plt.figure(figsize=(max(6, len(articles)*1.5), 6))
        plt.bar(articles, counts, color='green')
        plt.xlabel("Artículos")
        plt.ylabel("Número de figuras")
        plt.title("Número de figuras por artículo")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_image_path)
        plt.close()
        print(f"Gráfico de resumen guardado en: {output_image_path}")
    else:
        print("No se encontraron datos para generar el gráfico.")

def main():
    base_url = os.environ.get("GROBID_URL", "http://grobid:8070")
    pdf_folder = os.environ.get("PDF_FOLDER", "/app/pdfs")
    
    pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])
    if not pdf_files:
        print(f"No se encontraron archivos PDF en el directorio {pdf_folder}.")
        return
    
    # Procesar cada PDF para generar y guardar el TEI XML en pdf_full_text_document
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        output_folder = os.path.join(pdf_folder, base_name, "pdf_full_text_document")
        tei_file = os.path.join(output_folder, "tei.xml")
        if os.path.exists(tei_file):
            print(f"TEI XML ya generado para {pdf_file}. Se omite el procesamiento.")
        else:
            os.makedirs(output_folder, exist_ok=True)
            print(f"\nProcesando el archivo PDF: {pdf_path}")
            process_pdf_save_tei(pdf_path, base_url, output_folder)
    
    # Una vez procesados todos los PDFs, generar el gráfico resumen en la ruta general de los PDFs.
    output_image_path = os.path.join(pdf_folder, "figures_in_articles.png")
    generate_figures_summary(pdf_folder, output_image_path)

if __name__ == "__main__":
    print("Ejecutando archivo figures_visualization_generator.py")
    main()
    print("Ejecutando los siguientes archivos, espere...")
    sys.exit(0)
