# Beyond Sight 👁️‍🗨️

## ¿Qué es Beyond Sight?

**Beyond Sight** es el desarrollo inicial de una plataforma web que traduce **textos literarios** e **imágenes de obras de arte** a **braille** y a **secuencias de puntos táctiles**, con el objetivo de democratizar el acceso a la cultura para personas con discapacidad visual en el Perú.

En el Perú, gran parte del contenido cultural —libros, cuadros, exposiciones— no está disponible en formatos accesibles. Beyond Sight busca cerrar esa brecha convirtiendo automáticamente ese contenido en algo que una persona con discapacidad visual pueda "leer" mediante el tacto.

Para lograrlo, se implementó un sistema de **reconocimiento óptico de caracteres (OCR)** en Python que permite traducir texto tanto desde **documentos (PDF)** como desde **imágenes**, junto con un módulo que **convierte imágenes en patrones de puntos**, representando la forma de una obra de arte como una cuadrícula táctil. Este repositorio contiene el motor de procesamiento (texto → braille, imagen → patrón de puntos) que forma la base del proyecto: la visión a futuro es integrarlo en una plataforma web y, después, conectarlo a un **hardware físico** capaz de convertir el braille y los patrones de puntos generados en relieves táctiles reales.

### Módulos incluidos en este repositorio

| Módulo | Qué hace |
|---|---|
| `image_string.py` | Aplica OCR (Tesseract) sobre una imagen para extraer el texto que contiene. Preprocesa la imagen (binarización con Otsu, corrección de contraste) y valida que la resolución/nitidez sea suficiente para un reconocimiento confiable. |
| `pdf_string.py` | Extrae el texto de cada página de un documento PDF (con PyPDF2), devolviendo el contenido separado por página. |
| `string_braille.py` | Traduce un texto a braille (usando `liblouis`) y genera un **PDF visual** donde cada punto braille activo se dibuja gráficamente, para revisar la traducción antes de enviarla a un dispositivo físico. |
| `imagen_puntos.py` | Convierte una **imagen en un patrón de puntos**: detecta bordes y contornos (OpenCV) y los reduce a una matriz binaria de resolución configurable, representando la forma de la imagen como una cuadrícula de puntos "activos" e "inactivos" — la base para representar obras de arte de forma táctil. |

**Estado actual:** proyecto en etapa experimental. Los módulos funcionan de forma independiente y probada, pero aún no están integrados en la plataforma web ni conectados a un hardware físico. Las imágenes `prueba*.jpeg`, `vallejo.jpeg`, `37.png` y `noise.png` son casos de prueba usados para validar el OCR y la conversión de imágenes a patrones de puntos.

---

## 📥 Qué necesitas descargar antes de usarlo

### 1. Python
Se recomienda Python 3.9 o superior.

### 2. Librerías de Python

```bash
pip install opencv-python numpy pillow pytesseract PyPDF2 reportlab louis
```

### 3. Programas externos (no se instalan con pip)

- **Tesseract OCR**, con el paquete de idioma español — lo usa `image_string.py` para el reconocimiento de texto.
  - Windows: descargar el instalador desde el [repositorio oficial de Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) e instalarlo en `C:\Program Files\Tesseract-OCR\` (ruta que usa el script por defecto).
  - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-spa`

- **liblouis** — lo usa `string_braille.py` para la traducción de texto a braille.
  - Linux: `sudo apt-get install liblouis-bin liblouis-data python3-louis`
  - ⚠️ El paquete `louis` de PyPI (`pip install louis`) **no es el correcto**; se necesita el binding oficial de liblouis (`python3-louis`).

---

## ▶️ Cómo usarlo

### Traducir un texto a braille (y generar el PDF visual)

Desde la línea de comandos:

```bash
python string_braille.py "Hola mundo" -o resultado.pdf
```

O a partir de un archivo `.txt`:

```bash
python string_braille.py --archivo texto.txt -o resultado.pdf
```

El resultado es un PDF donde cada celda braille se dibuja punto por punto, ideal para verificar visualmente la traducción antes de pasarla a un dispositivo táctil.

### Extraer texto desde una imagen (OCR)

```python
from image_string import image_string
texto = image_string("prueba1.jpeg")
print(texto)
```

### Extraer texto desde un PDF

```python
from pdf_string import pdf_string
paginas = pdf_string("documento.pdf")
```

### Convertir una imagen de una obra de arte en un patrón de puntos

```python
from imagen_puntos import imagen_matriz, imprimir_matriz

matriz = imagen_matriz("prueba5.jpeg", tamano=(50, 50))
imprimir_matriz(matriz)
```

Esto imprime en consola una cuadrícula de asteriscos (`*`) representando los puntos "activos" detectados en la imagen — la misma matriz que, integrada al hardware, se traduciría en relieves táctiles reales.

---

## 🔭 Próximos pasos del proyecto

- Integrar estos módulos en una **plataforma web** accesible, donde el usuario pueda subir un texto o una imagen y descargar/enviar directamente su traducción a braille o a patrón de puntos.
- Diseñar y construir el **dispositivo háptico** capaz de recibir estos patrones y convertirlos en puntos táctiles físicos.
- Ampliar el catálogo de obras de arte y textos literarios peruanos disponibles en formato accesible.
