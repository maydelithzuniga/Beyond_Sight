import cv2
from PIL import Image
import pytesseract
import numpy as np
def image_string(m):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = cv2.imread(m, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("La imagen ingresada no existe o no se puede leer")
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if img_bin.mean() < 127:
        img_bin = cv2.bitwise_not(img_bin)
    pil_imag = Image.fromarray(img_bin)
    dpi = pil_imag.info.get("dpi")
    if dpi is None:
        contorno, jerarquia = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        heights = [cv2.boundingRect(c)[3] for c in contorno if cv2.boundingRect(c)[3] > 5]
        if np.mean(heights) < 20:
            raise FileExistsError("El archivo subido está muy borroso para ser procesado. "
                               "Por favor, carga nuevamente el archivo con una mayor resolución.")
    elif dpi:
        if 200 < dpi[0] and 200 < dpi[1] and (dpi[0] < 300 or dpi[1] < 300):
            resized = cv2.resize(img_bin, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            pil_imag = Image.fromarray(resized)
        elif 200 > dpi[0] or 200 > dpi[1]:
            raise FileExistsError("El archivo subido está muy borroso para ser procesado. "
                               "Por favor, carga nuevamente el archivo con una mayor resolución.")
    texto = pytesseract.image_to_string(pil_imag, lang="spa")
    return(texto)
print(image_string("vallejo.jpeg"))