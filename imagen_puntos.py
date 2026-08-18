from PIL import Image
import numpy as np
import cv2
bajo=50
alto=150
def bordes (imagen,umbral_bajo=bajo, umbral_alto=alto):
    img=cv2.imread(imagen)
    img_gris=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gris = cv2.bilateralFilter(img_gris, 9, 75, 75)
    img_gris = cv2.GaussianBlur(img_gris, (5, 5), 0)
    img_gris = cv2.equalizeHist(img_gris)
    """kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    img_sharp = cv2.filter2D(img_gris, -1, kernel)
    bordes = cv2.Canny(img_sharp, umbral_bajo, umbral_alto) """
    
    """bordes = cv2.Canny(img_gris[:,:,1], umbral_bajo, umbral_alto)"""
    """img_gris=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gris = cv2.bilateralFilter(img_gris, 9, 75, 75)
    img_gris = cv2.GaussianBlur(img_gris, (5, 5), 0)
    img_gris = cv2.equalizeHist(img_gris)"""
    #bordes = cv2.Laplacian(img_gris, cv2.CV_64F)
    grad_x = cv2.Sobel(img_gris, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gris, cv2.CV_64F, 0, 1, ksize=3)
    bordes = cv2.magnitude(grad_x, grad_y)
    ##umbral,_=cv2.threshold(img_gris,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ##umbral_bajo=int(umbral*0.5)
    ##umbral_alto=int(umbral*1.5)
    #bordes=cv2.Canny(img_gris,umbral_bajo,umbral_alto)
    return bordes
def imagen_matriz(imagen,umbral_bajo=bajo, umbral_alto=alto, tamano=(50, 50)):
    img_bordes=bordes(imagen,umbral_bajo,umbral_alto)
    img_bordes_resized = cv2.resize(img_bordes, tamano, interpolation=cv2.INTER_NEAREST)
    matriz=np.array(img_bordes_resized)
    matriz_binaria=np.where(matriz>0,1,0)
    return matriz_binaria

def imprimir_matriz(matriz):
    for fila in matriz:
        print(" ".join("*" if int(elemento)==1 else " " for elemento in fila))

imagen="prueba5.jpeg"
matriz=imagen_matriz(imagen, umbral_bajo=bajo, umbral_alto=alto, tamano=(50, 50))
imprimir_matriz(matriz)