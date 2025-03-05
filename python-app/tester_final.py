import os
import sys

def test_folder_per_pdf(pdf_folder):
    """
    Comprueba que para cada archivo PDF en pdf_folder exista una carpeta con su nombre base.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    all_ok = True
    for pdf in pdf_files:
        base_name = os.path.splitext(pdf)[0]
        folder_path = os.path.join(pdf_folder, base_name)
        if not os.path.isdir(folder_path):
            print(f"Test 1 FAILED: La carpeta '{folder_path}' no existe para el PDF '{pdf}'.")
            all_ok = False
        # else:
            # print(f"Test 1 PASSED: La carpeta '{folder_path}' existe para el PDF '{pdf}'.")
    if all_ok:
        print(f"Test 1 PASSED: Se han generado las carpetas correspondientes para todos los pdfs correctamente.")
    return all_ok

def test_keyword_cloud_folder(pdf_folder):
    """
    Comprueba que en cada carpeta de PDF exista una subcarpeta 'keyword_cloud' 
    que contenga los archivos 'keyword_cloud.png' y 'tei.xml'.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    all_ok = True
    for pdf in pdf_files:
        base_name = os.path.splitext(pdf)[0]
        folder_path = os.path.join(pdf_folder, base_name, "keyword_cloud")
        if not os.path.isdir(folder_path):
            print(f"Test 2 FAILED: La carpeta 'keyword_cloud' no existe en '{os.path.join(pdf_folder, base_name)}'.")
            all_ok = False
            continue
        kw_image = os.path.join(folder_path, "keyword_cloud.png")
        tei_file = os.path.join(folder_path, "tei.xml")
        if not os.path.isfile(kw_image):
            print(f"Test 2 FAILED: El archivo 'keyword_cloud.png' no se encontró en '{folder_path}'.")
            all_ok = False
        # else:
            # print(f"Test 2 PASSED: 'keyword_cloud.png' existe en '{folder_path}'.")
        if not os.path.isfile(tei_file):
            print(f"Test 2 FAILED: El archivo 'tei.xml' no se encontró en '{folder_path}'.")
            all_ok = False
        # else:
            # print(f"Test 2 PASSED: 'tei.xml' existe en '{folder_path}'.")
    if all_ok:
        print(f"Test 2 PASSED: Se han generado los keyword cloud para todos los pdfs correctamente.")
    return all_ok

def test_pdf_full_text_document_folder(pdf_folder):
    """
    Comprueba que en cada carpeta de PDF exista una subcarpeta 'pdf_full_text_document'
    que contenga el archivo 'tei.xml'.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    all_ok = True
    for pdf in pdf_files:
        base_name = os.path.splitext(pdf)[0]
        folder_path = os.path.join(pdf_folder, base_name, "pdf_full_text_document")
        if not os.path.isdir(folder_path):
            print(f"Test 3 FAILED: La carpeta 'pdf_full_text_document' no existe en '{os.path.join(pdf_folder, base_name)}'.")
            all_ok = False
            continue
        tei_file = os.path.join(folder_path, "tei.xml")
        if not os.path.isfile(tei_file):
            print(f"Test 3 FAILED: El archivo 'tei.xml' no se encontró en '{folder_path}'.")
            all_ok = False
        # else:
            # print(f"Test 3 PASSED: 'tei.xml' existe en '{folder_path}'.")
    if all_ok:
        print(f"Test 3 PASSED: Se han generado los pdf_full_documents para todos los pdfs correctamente.")
    return all_ok

def test_links_in_pdf_folder(pdf_folder):
    """
    Comprueba que en cada carpeta de PDF exista una subcarpeta 'links_in_pdf'
    que contenga el archivo 'links.txt'.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    all_ok = True
    for pdf in pdf_files:
        base_name = os.path.splitext(pdf)[0]
        folder_path = os.path.join(pdf_folder, base_name, "links_in_pdf")
        if not os.path.isdir(folder_path):
            print(f"Test 4 FAILED: La carpeta 'links_in_pdf' no existe en '{os.path.join(pdf_folder, base_name)}'.")
            all_ok = False
            continue
        links_file = os.path.join(folder_path, "links.txt")
        if not os.path.isfile(links_file):
            print(f"Test 4 FAILED: El archivo 'links.txt' no se encontró en '{folder_path}'.")
            all_ok = False
        # else:
            # print(f"Test 4 PASSED: 'links.txt' existe en '{folder_path}'.")
    
    if all_ok:
        print(f"Test 4 PASSED: Se han generado los links para todos los pdfs correctamente.")
    return all_ok

def test_figures_in_articles(pdf_folder):
    """
    Comprueba que en la carpeta general de PDFs exista el archivo 'figures_in_articles.png'.
    """
    file_path = os.path.join(pdf_folder, "figures_in_articles.png")
    if os.path.isfile(file_path):
        print(f"Test 5 PASSED: 'figures_in_articles.png' existe en '{pdf_folder}'.")
        return True
    else:
        print(f"Test 5 FAILED: 'figures_in_articles.png' no se encontró en '{pdf_folder}'.")
        return False

def main():
    pdf_folder = os.environ.get("PDF_FOLDER", "/app/pdfs")
    print("Ejecutando tester_final.py...\n")
    result1 = test_folder_per_pdf(pdf_folder)
    result2 = test_keyword_cloud_folder(pdf_folder)
    result3 = test_pdf_full_text_document_folder(pdf_folder)
    result4 = test_links_in_pdf_folder(pdf_folder)
    result5 = test_figures_in_articles(pdf_folder)
    
    all_passed = result1 and result2 and result3 and result4 and result5

    print(f"\n{'-' * 20}\n")
    
    if all_passed:
        print("\nTodos los test han pasado exitosamente. \n Se recomienda finalizar ya la ejecución del docker.")
    else:
        print("\nUno o más test han fallado. Se recomienda ejecutar nuevamente el proceso de generación.")

if __name__ == "__main__":
    print("\n \ n")
    print(f"{'-' * 20} \n")
    main()
    print(f"{'-' * 20}\n")
    sys.exit(0)
