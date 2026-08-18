import PyPDF2
def pdf_string(ruta_pdf):
    try:
        with open(ruta_pdf,"rb") as archivo:
            paginas=PyPDF2.PdfReader(archivo)
            paginas_texto={}
            for num in range(len(paginas.pages)):
                pagina=paginas.pages[num]
                texto=pagina.extractText()
                paginas_texto[f"Pagina {num+1}"]=f"*** Texto de la pagina {num+1} ***\n\n{texto}"
    except FileNotFoundError:
        raise FileNotFoundError("El archivo pedido no puede ser encontrado")
    except Exception as error:
        raise FileExistsError (f"Hubo un error al leer el archivo: {error}")
    return paginas_texto
