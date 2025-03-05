# Rationale

Este documento explica cómo se han validado las respuestas y salidas generadas por los distintos scripts de este repositorio. El proyecto consta de varios scripts en Python que procesan archivos PDF utilizando la API de Grobid para extraer información relevante, como nubes de palabras, visualizaciones de figuras y listas de enlaces. Además, se realizan pruebas unitarias e integrales para asegurar el correcto funcionamiento de cada componente.

---

## Validación de las respuestas de la API

- **Pruebas Iniciales:**  
  Se utiliza el script `tester_inicial.py` para validar que los endpoints clave de Grobid funcionen correctamente. En concreto, se comprueba que:
  - El endpoint `/api/version` retorne la versión esperada (por ejemplo, "0.8.1").
  - El endpoint `/api/isalive` retorne "true".
  
  **Método de validación:**  
  - Se muestran en consola los resultados de ambos endpoints.
  - Solo se procede a ejecutar el resto de los scripts si las pruebas iniciales son exitosas.
  - Además, se ha verificado manualmente usando herramientas de línea de comandos y navegadores.

---

## Validación del Generador de Nubes de Palabras (Keyword Cloud)

- **Script:** `keyword_cloud_generator.py`  
- **Salidas Validadas:**  
  - Se genera un archivo TEI XML (`tei.xml`) en la subcarpeta `keyword_cloud` para cada PDF.
  - Se genera una imagen (`keyword_cloud.png`) que contiene la nube de palabras extraída del abstract del documento.
  
  **Método de validación:**  
  - Se realizaron ejecuciones con varios PDFs de ejemplo y se inspeccionaron visualmente los resultados.
  - Se implementaron pruebas en `tester_final.py` para verificar la existencia de los archivos generados en la estructura de carpetas esperada.

---

## Validación del Generador de Visualización de Figuras

- **Script:** `figures_visualization_generator.py`  
- **Salidas Validadas:**  
  - Se guarda el TEI XML en una subcarpeta llamada `pdf_full_text_document` para cada PDF.
  - Se cuenta el número de elementos `<figure>` (usando el namespace TEI) de forma precisa.
  - Se genera un gráfico de barras (`figures_in_articles.png`) en la carpeta raíz de los PDFs, donde cada barra muestra el número de figuras de cada artículo.
  
  **Método de validación:**  
  - La función que cuenta las figuras se ha probado con archivos TEI XML y se ha verificado que el conteo sea correcto.
  - El gráfico generado se ha inspeccionado manualmente para confirmar que cada artículo está correctamente etiquetado con el número correspondiente de figuras.
  - Se ordenaron alfabéticamente los nombres de los artículos para asegurar la asociación correcta.

---

## Validación del Generador de Extracción de Enlaces

- **Script:** `links_in_pdf_generator.py`  
- **Salidas Validadas:**  
  - Se utiliza el servicio `/api/processReferences` de Grobid para obtener el TEI XML de las referencias.
  - Se extraen los enlaces de los atributos `target` de los elementos del TEI XML.
  - Se manejan casos especiales:
    - Si la API devuelve un código 204, se genera un archivo `links.txt` con un mensaje indicando el error.
    - Si se obtiene TEI XML pero no se encuentran enlaces, se genera un archivo `links.txt` con el mensaje "No se encontraron links en las referencias del archivo."
  
  **Método de validación:**  
  - Se ha probado la lógica de extracción utilizando expresiones regulares y el manejo de namespaces para asegurarse de que se capturan los enlaces correctos.
  - Se han validado manualmente los mensajes generados en los casos de error.

---

## Validación de la Integración Final

- **Script de Pruebas Finales:** `tester_final.py`  
- **Test Unitarios Realizados:**  
  1. Se comprueba que, para cada PDF en la carpeta `PDF_FOLDER`, exista una carpeta con el nombre base del PDF.
  2. Se verifica que, dentro de cada carpeta de PDF, exista una subcarpeta `keyword_cloud` que contenga los archivos `keyword_cloud.png` y `tei.xml`.
  3. Se comprueba que, dentro de cada carpeta de PDF, exista una subcarpeta `pdf_full_text_document` que contenga el archivo `tei.xml`.
  4. Se verifica que, dentro de cada carpeta de PDF, exista una subcarpeta `links_in_pdf` que contenga el archivo `links.txt`.
  5. Se comprueba que en la carpeta raíz de PDFs exista el archivo `figures_in_articles.png`.
  
  **Método de validación:**  
  - Los test unitarios se ejecutan al final del flujo (con `tester_final.py`) y se muestran mensajes de PASSED o FAILED para cada verificación.
  - En caso de que alguno falle, se recomienda reejecutar el proceso.

- **Integración a través de Docker Compose:**  
  - Todos los scripts se encadenan y ejecutan en un contenedor utilizando `docker-compose up --build`.
  - Se han realizado pruebas de integración para verificar que la estructura de carpetas y la generación de archivos se realicen correctamente en el entorno Docker.

---

## Conclusión

La validación de este repositorio se ha realizado mediante una combinación de pruebas unitarias automatizadas y validación manual de los resultados. Cada componente (desde la comunicación con la API de Grobid hasta la generación de gráficos y extracción de enlaces) se ha verificado para asegurar que produce la salida esperada. Si algún test falla, se recomienda volver a ejecutar el proceso, lo cual se informa en los mensajes de error de los scripts.

Si tienes alguna pregunta o encuentras problemas, por favor abre un issue en el repositorio.
