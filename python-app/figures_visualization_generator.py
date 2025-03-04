import os
import requests

def process_pdf_generate_figures_visualization(pdf_path, base_url, output_folder):
    """
    Envía el PDF al endpoint de Grobid para obtener una visualización que muestra
    el número de figuras por artículo. La respuesta (imagen) se guarda en output_folder
    como 'visualization_figures.png'.
    """
    url = f"{base_url}/api/visualization/figures"
    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {"input": pdf_file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            visualization_path = os.path.join(output_folder, "visualization_figures.png")
            with open(visualization_path, "wb") as f:
                f.write(response.content)
            print(f"Visualización de figures guardada en: {visualization_path}")
        else:
            print("Error en el procesamiento del PDF para figures. Código:", response.status_code)
            print(response.text)
    except Exception as e:
        print("Excepción al enviar el PDF para figures:", e)

def main():
    """
    Procesa todos los archivos PDF en el directorio definido por PDF_FOLDER.
    Para cada PDF se crea una carpeta (con el mismo nombre del archivo sin extensión)
    y, dentro de ella, una subcarpeta llamada "visualization_figures" donde se guardará la
    visualización generada. Si ya existe el archivo 'visualization_figures.png', se omite
    el procesamiento para ese PDF.
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
        # Crear la carpeta de salida: carpeta base y subcarpeta 'visualization_figures'
        output_folder = os.path.join(pdf_folder, base_name, "visualization_figures")
        
        visualization_file = os.path.join(output_folder, "visualization_figures.png")
        if os.path.exists(visualization_file):
            print(f"Visualización ya generada para {pdf_file}. Se omite el procesamiento.")
            continue
        
        os.makedirs(output_folder, exist_ok=True)
        print(f"\nProcesando el archivo PDF: {pdf_path}")
        process_pdf_generate_figures_visualization(pdf_path, base_url, output_folder)

if __name__ == "__main__":
    print("Ejecutando archivo figures_visualization_generator.py")
    main()
