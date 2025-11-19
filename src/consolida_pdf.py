from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, legal
from reportlab.lib.units import inch
from PIL import Image

from reportlab.lib.units import mm

import os


# Oficio / Government Legal paper size
OFICIO = (216 * mm, 330 * mm)

def pngs_a_pdf_carta(lista_pngs, nombre_pdf_salida, pagesize):
    """
    Consolida una lista de archivos PNG en un único PDF con tamaño de página Carta.
    """
    # 1. Crear el objeto Canvas (lienzo) del PDF
    # letter es (8.5 * inch, 11 * inch) o (612, 792) puntos
    c = canvas.Canvas(nombre_pdf_salida, pagesize=pagesize)
    ancho_pagina, alto_pagina = letter

    # 2. Procesar cada archivo PNG
    for i, ruta_png in enumerate(lista_pngs):
        try:
            # Abrir la imagen con PIL
            img = Image.open(ruta_png)

            # --- Ajustar la imagen al tamaño de la página Carta ---
            
            # Las coordenadas en ReportLab se miden desde la esquina inferior izquierda.
            
            # Redimensionar la imagen para que encaje dentro de la página
            # sin perder la relación de aspecto (aspect ratio).
            ancho_img, alto_img = img.size
            
            # Calcular la escala necesaria
            escala_ancho = ancho_pagina / ancho_img
            escala_alto = alto_pagina / alto_img
            
            # Usar la escala más pequeña para asegurar que la imagen quepa completamente
            escala = min(escala_ancho, escala_alto)
            
            # Nuevo tamaño de la imagen en puntos del PDF
            nuevo_ancho = ancho_img * escala
            nuevo_alto = alto_img * escala
            
            # Calcular las coordenadas X e Y para centrar la imagen en la página
            # (Si la imagen no ocupa toda la página, se verá centrada)
            x_centrado = (ancho_pagina - nuevo_ancho) / 2
            y_centrado = (alto_pagina - nuevo_alto) / 2
            
            # 3. Dibujar la imagen en el Canvas
            # c.drawImage(ruta_archivo, x, y, ancho, alto)
            c.drawImage(ruta_png, x_centrado, y_centrado, nuevo_ancho, nuevo_alto)
            
            # 4. Pasar a la siguiente página (si no es el último archivo)
            c.showPage()
            
            print(f"✅ Agregada página {i+1}: {ruta_png}")
            
        except FileNotFoundError:
            print(f"❌ Error: El archivo no fue encontrado: {ruta_png}")
        except Exception as e:
            print(f"❌ Error al procesar {ruta_png}: {e}")

    # 5. Guardar el PDF final
    c.save()
    print(f"\n✨ ¡PDF creado con éxito! Nombre del archivo: **{nombre_pdf_salida}**")

    for i, ruta_png in enumerate(lista_pngs):
        os.remove(ruta_png)

# --- USO DEL SCRIPT ---

if __name__ == '__main__':
    # Reemplaza estas rutas con los nombres reales de tus archivos PNG
    archivos_png = [
        "mi_imagen_1.png",
        "mi_imagen_2.png",
        "ruta/completa/a/otra_imagen_3.png",
        # Agrega todos tus archivos PNG aquí
    ]

    nombre_pdf = "documento_consolidado.pdf"

    # Ejecutar la función
    # NOTA: Asegúrate de que los archivos PNG listados arriba existan en la ubicación correcta
    # antes de ejecutar la función, o el script fallará.
    # pngs_a_pdf_carta(archivos_png, nombre_pdf)

    # Ejemplo de prueba (comentar el código de ejemplo si se usan archivos reales):
    print("Simulación de la ejecución (por favor, descomenta y actualiza 'archivos_png' para usarlo realmente):")
    # pngs_a_pdf_carta(archivos_png, nombre_pdf)