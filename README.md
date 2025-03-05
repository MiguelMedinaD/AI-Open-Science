# AI-Open-Science

Este proyecto de Miguel Medina utiliza Docker y Grobid para procesar archivos PDF y extraer información relevante, como nubes de palabras, visualizaciones de figuras y listas de enlaces. Los resultados se generan a través de varios scripts que se ejecutan secuencialmente en contenedores Docker.

---

## Requisitos Previos
Tener instalados los siguientes programas:
- [Git](https://git-scm.com/)
  *Para verificar que Docker está instalado, abre la consola y ejecuta:*
  ```bash
   git -v
   ```
  *Si no lo tienes instalado, sigue las instrucciones en [Git download](https://git-scm.com/downloads).*
- [Docker](https://docs.docker.com/get-docker/)  
  *Para verificar que Docker está instalado, abre la consola y ejecuta:*
  ```bash
   docker --version
   ```
  *Si no lo tienes instalado, sigue las instrucciones en [Get Docker](https://docs.docker.com/get-started/get-docker/).*

---

## Instalación y Configuración

1. **Clona el repositorio**  
   Clona el repositorio en la carpeta que desees:
   ```bash
   git clone https://github.com/MiguelMedinaD/AI-Open-Science.git
   ```
   Si desea continuar no cierre la consola

2. **Prepara los archivos PDF**  
   Guarda los PDFs que deseas procesar en la carpeta `pdfs` que se encuentra en la raíz del repositorio clonado.  
   *Asegúrate de que la carpeta `pdfs` contenga tus archivos y no esté vacía.*

3. **Ubícate en la carpeta del repositorio**  
   Vuelve a la consola y sitúate en la carpeta del repositorio clonado:
   ```bash
   cd AI-Open-Science
   ```
   En caso de que haya cerrado la consola situate en el directorio de la carpeta con su ruta completa:
   ```bash
   cd ruta/AI-Open-Science
   ```

---

## Ejecución

El proyecto se ejecuta a través de Docker Compose y realiza las siguientes operaciones en orden:

- **tester_inicial.py:** Realiza pruebas iniciales de la API de Grobid.  
- **keyword_cloud_generator.py:** Genera nubes de palabras a partir del abstract de los PDFs.  
- **figures_visualization_generator.py:** Procesa los PDFs para generar TEI XML y crea un gráfico de barras que muestra el número de figuras por artículo.  
- **links_in_pdf_generator.py:** Extrae los enlaces de cada PDF usando el servicio de Grobid.  
- **tester_final.py:** Ejecuta test unitarios finales para comprobar que se han generado las carpetas y archivos esperados.

### Pasos para ejecutar el proyecto:

1. **Construir y levantar los contenedores**  
   Abra la consola si la ha cerrado y situese dentro de la carpeta del repositorio clonado:
   ```bash
   cd ruta/AI-Open-Science
   ```
   Ejecuta el siguiente comando para construir y ejecutar todos los servicios:
   ```bash
   docker-compose up --build
   ```
   *Este comando ejecutará, en orden, todos los scripts mencionados.*

2. **Detener la ejecución**  
   Una vez que la ejecución haya finalizado (o si deseas detenerla), presiona `Ctrl + C` en la consola.

3. **Finalizar y eliminar contenedores**  
   Para eliminar los contenedores y recursos generados, ejecuta:
   ```bash
   docker-compose down
   ```

4. **Reejecución del proceso**  
   - **Si borraste los contenedores:** Vuelve a ejecutar `docker-compose up --build` para iniciar el proceso desde cero.  
   - **Si solo paraste la ejecución (Ctrl + C):** Puedes reanudar los contenedores sin eliminar todo usando:
     ```bash
     docker-compose start
     ```
     Y para ver los logs en tiempo real:
     ```bash
     docker-compose logs -f
     ```

---

## Notas Adicionales

- El proyecto utiliza volúmenes para separar el código y los datos.  
  - La carpeta local `./pdfs` (a nivel de la raíz del repositorio) se monta en el contenedor en `/app/pdfs`.  
  - **Importante:** Si encuentras una carpeta `pdfs` dentro de `python-app`, es innecesaria y se ignora en favor de la carpeta `pdfs` externa.

- Revisa el archivo **.gitignore** para asegurarte de que no se suban archivos innecesarios (como los PDFs y resultados generados).

- Si tienes problemas o sugerencias, abre un issue en el repositorio.

---

¡Disfruta usando AI-Open-Science y descubre todo lo que puedes extraer de tus PDFs con Grobid!
