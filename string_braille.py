import argparse
import sys
import textwrap

try:
    import louis
except ImportError:
    sys.exit(
        "No se encontró el módulo 'louis' (liblouis).\n"
        "Instalalo con:\n"
        "    sudo apt-get install liblouis-bin liblouis-data python3-louis\n"
        "(el paquete 'louis' de PyPI NO sirve, es otra cosa homónima)."
    )

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def texto_a_braille(texto: str, tabla: str = "es-g1.ctb") -> str:
    """Traduce texto a una cadena de caracteres braille Unicode (U+2800..)."""
    resultado = louis.translate(["unicode.dis", tabla], texto)
    return resultado[0]


POSICIONES_PUNTOS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2), 7: (0, 3),
    4: (1, 0), 5: (1, 1), 6: (1, 2), 8: (1, 3),
}
BIT_DE_PUNTO = {1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08,
                5: 0x10, 6: 0x20, 7: 0x40, 8: 0x80}


def puntos_de_celda(caracter_braille: str):
    """Devuelve la lista de números de punto (1-8) activos en una celda braille."""
    codigo = ord(caracter_braille) - 0x2800
    return [p for p, bit in BIT_DE_PUNTO.items() if codigo & bit]


def dibujar_michi(c: canvas.Canvas, cx: float, cy: float, r: float):
    """
    Dibuja el punto braille activo como el caracter literal "*" ("michi"),
    centrado en (cx, cy). Se usa una fuente en negrita y un tamaño
    proporcional a r para que se note bien en el PDF.
    """
    c.saveState()
    c.setFillColorRGB(0.1, 0.1, 0.1)
    tam_fuente = r * 2.6
    c.setFont("Helvetica-Bold", tam_fuente)
    # drawCentredString centra horizontalmente; ajustamos verticalmente
    # a ojo para que el "*" quede centrado en (cx, cy) y no por su línea base.
    c.drawCentredString(cx, cy - tam_fuente * 0.32, "*")
    c.restoreState()


def dibujar_punto_vacio(c: canvas.Canvas, cx: float, cy: float, r: float):
    """Punto braille "apagado": un circulito tenue para marcar la posición."""
    c.saveState()
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(0.3)
    c.circle(cx, cy, r * 0.35, fill=0, stroke=1)
    c.restoreState()


def generar_pdf_braille_michi(
    texto: str,
    ruta_pdf: str,
    tabla: str = "es-g1.ctb",
    mostrar_texto_original: bool = True,
):
    braille = texto_a_braille(texto, tabla)

    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    ancho_pagina, alto_pagina = A4

    margen = 15 * mm
    r_punto = 3.0 * mm            # "radio" de cada michi
    ancho_celda = r_punto * 3.4   # separación horizontal entre celdas
    alto_celda = r_punto * 7.2    # separación vertical entre celdas (2x4 puntos)
    sep_punto_x = r_punto * 1.6
    sep_punto_y = r_punto * 1.6

    x = margen
    y = alto_pagina - margen - alto_celda

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margen, alto_pagina - margen + 3 * mm, "Traducción a Braille (puntos = michis)")

    if mostrar_texto_original:
        c.setFont("Helvetica", 9)
        for i, linea in enumerate(textwrap.wrap(f"Texto original: {texto}", 100)):
            c.drawString(margen, alto_pagina - margen - 6 * mm - i * 4 * mm, linea)
        y -= (len(textwrap.wrap(texto, 100)) + 1) * 4 * mm

    for caracter in braille:
        # salto de línea real del texto original (line breaks del propio texto)
        if caracter == "\n":
            x = margen
            y -= alto_celda
            if y < margen:
                c.showPage()
                x, y = margen, alto_pagina - margen - alto_celda
            continue

        # salto de página / de línea si no entra otra celda
        if x + ancho_celda > ancho_pagina - margen:
            x = margen
            y -= alto_celda
        if y < margen:
            c.showPage()
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margen, alto_pagina - margen + 3 * mm, "Traducción a Braille (continuación)")
            x, y = margen, alto_pagina - margen - alto_celda

        puntos_activos = set(puntos_de_celda(caracter))

        for num_punto, (col, fila) in POSICIONES_PUNTOS.items():
            cx = x + col * sep_punto_x + r_punto
            cy = y + alto_celda - (fila * sep_punto_y) - r_punto
            if num_punto in puntos_activos:
                dibujar_michi(c, cx, cy, r_punto)
            else:
                dibujar_punto_vacio(c, cx, cy, r_punto)

        x += ancho_celda

    c.save()
    return braille


def main():
    parser = argparse.ArgumentParser(
        description="Convierte texto a braille (liblouis) y genera un PDF "
                     "donde cada punto braille es dibujado como un michi."
    )
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("texto", nargs="?", help="Texto a convertir (entre comillas)")
    grupo.add_argument("--archivo", "-f", help="Ruta a un archivo .txt con el texto")

    parser.add_argument("-o", "--salida", default="braille_michi.pdf",
                         help="Ruta del PDF de salida (default: braille_michi.pdf)")
    parser.add_argument("--tabla", default="es-g1.ctb",
                         help="Tabla de traducción de liblouis (default: es-g1.ctb). "
                              "Ejemplos: es-g1.ctb, en-us-g1.ctb, es-g2.ctb")

    args = parser.parse_args()

    if args.archivo:
        with open(args.archivo, "r", encoding="utf-8") as f:
            texto = f.read()
    else:
        texto = args.texto

    braille = generar_pdf_braille_michi(texto, args.salida, tabla=args.tabla)
    print(f"Braille generado: {braille}")
    print(f"PDF guardado en: {args.salida}")


if __name__ == "__main__":
    main()