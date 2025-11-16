import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageColor
import logging



# --- 1. Configuración de los cartones y la página ---

# Definición de los rangos estándar para las columnas de Bingo (B-I-N-G-O)
RANGOS_BINGO = {
    'B': (1, 15),
    'I': (16, 30),
    'N': (31, 45),
    'G': (46, 60),
    'O': (61, 75)
}
COLUMNAS = list(RANGOS_BINGO.keys())

# Configuración del tamaño de la página (216 mm x 279 mm)
# Convertimos mm a píxeles. Usaremos una resolución de 300 DPI (puntos por pulgada)
DPI = 300
MM_POR_PULGADA = 25.4

def mm_a_pixeles(mm):
    return int((mm / MM_POR_PULGADA) * DPI)

PAGE_WIDTH_MM = 216
PAGE_HEIGHT_MM = 279

PAGE_WIDTH_PX = mm_a_pixeles(PAGE_WIDTH_MM)
PAGE_HEIGHT_PX = mm_a_pixeles(PAGE_HEIGHT_MM)

PAGE_SIZE = 'letter'

def set_paper_size_letter(paper_size : str = 'letter'):
    global PAGE_HEIGHT_MM, PAGE_HEIGHT_PX, PAGE_WIDTH_MM, PAGE_WIDTH_PX

    PAGE_WIDTH_MM = 216
    PAGE_HEIGHT_MM = 279

    PAGE_WIDTH_PX = mm_a_pixeles(PAGE_WIDTH_MM)
    PAGE_HEIGHT_PX = mm_a_pixeles(PAGE_HEIGHT_MM)

def set_paper_size_office(paper_size : str = 'letter'):
    global PAGE_HEIGHT_MM, PAGE_HEIGHT_PX, PAGE_WIDTH_MM, PAGE_WIDTH_PX

    PAGE_WIDTH_MM = 216
    PAGE_HEIGHT_MM = 3300

    PAGE_WIDTH_PX = mm_a_pixeles(PAGE_WIDTH_MM)
    PAGE_HEIGHT_PX = mm_a_pixeles(PAGE_HEIGHT_MM)

set_paper_size_map = {
    'letter': set_paper_size_letter,
    'office': set_paper_size_office,
}

def set_paper_size(paper_size : str = 'letter'):
    if paper_size in set_paper_size_map:
        set_paper_size_map[paper_size]
    else:
        PAGE_SIZE = 'letter'
        logging.info(f"Paper size '{paper_size}' not found. Using by default '{PAGE_SIZE}'")

# Configuración del tamaño de cada cartón (ajustable)
CARD_WIDTH_PX = mm_a_pixeles(95)  # Ancho de un cartón en píxeles (aprox 8cm)
CARD_HEIGHT_PX = mm_a_pixeles(95) # Alto de un cartón en píxeles (aprox 8cm)

# Márgenes internos de la página y entre cartones
PAGE_MARGIN_PX = mm_a_pixeles(10) # 10mm de margen en la página
CARD_SPACING_PX = mm_a_pixeles(5)  # 5mm de espacio entre cartones

# Colores y fuentes
BACKGROUND_COLOR = "white"
BORDER_COLOR = "red"
GRID_COLOR = "black"
TEXT_COLOR = "black"
FREE_SPACE_COLOR = "red"
FREE_SPACE_TEXT_COLOR = "white" # Cambiado a blanco para mejor contraste en fondo rojo

# Intentamos cargar una fuente TrueType; si no está disponible, usamos la predeterminada de Pillow
try:
    #const fontPath = path.join(__dirname, '../assets/fonts/PottiSreeramulu.ttf');
    #FONT_PATH = "arial.ttf" # Ruta a una fuente .ttf disponible en tu sistema
    #FONT_PATH = "/usr/share/code/resources/app/node_modules/katex/dist/fonts/KaTeX_Caligraphic-Regular.ttf"
    #FONT_PATH = "/usr/share/fonts/truetype/teluguvijayam/PottiSreeramulu.ttf"
    FONT_PATH = "../assets/fonts/PottiSreeramulu.ttf"
    FONT_HEADER = ImageFont.truetype(FONT_PATH, size=mm_a_pixeles(8)) # Tamaño para B-I-N-G-O
    FONT_NUMBERS = ImageFont.truetype(FONT_PATH, size=mm_a_pixeles(10)) # Tamaño para números
    FONT_FREE = ImageFont.truetype(FONT_PATH, size=mm_a_pixeles(8)) # Tamaño para 'Libre'
except IOError:
    print("Advertencia: No se encontró 'arial.ttf'. Usando la fuente predeterminada de Pillow.")
    FONT_HEADER = ImageFont.load_default()
    FONT_NUMBERS = ImageFont.load_default()
    FONT_FREE = ImageFont.load_default()

# Ajuste de tamaño de fuente si se usa la predeterminada
if FONT_HEADER == ImageFont.load_default():
    FONT_HEADER = ImageFont.load_default(size=40)
    FONT_NUMBERS = ImageFont.load_default(size=60)
    FONT_FREE = ImageFont.load_default(size=40)


# --- 2. Funciones de generación de datos de cartones ---

def generar_carton_bingo():
    """Genera un cartón de Bingo de 5x5 con 'Libre' en el centro."""
    carton = {}
    
    for columna_letra, (min_val, max_val) in RANGOS_BINGO.items():
        cantidad_numeros = 5
        if columna_letra == 'N':
            cantidad_numeros = 4
            
        numeros = random.sample(range(min_val, max_val + 1), k=cantidad_numeros)
        carton[columna_letra] = numeros
    
    carton['N'].insert(2, 'Libre')
    df_carton = pd.DataFrame(carton)
    return df_carton

# --- 3. Función para dibujar un solo cartón ---

def dibujar_carton(df_carton, card_id):
    """
    Dibuja un solo cartón de Bingo como una imagen.
    """
    img = Image.new('RGB', (CARD_WIDTH_PX, CARD_HEIGHT_PX), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Dibujar el borde rojo exterior
    BORDER_THICKNESS = mm_a_pixeles(4) # Grosor del borde
    draw.rectangle(
        (0, 0, CARD_WIDTH_PX - 1, CARD_HEIGHT_PX - 1), 
        fill=BORDER_COLOR, 
        outline=BORDER_COLOR, 
        width=BORDER_THICKNESS
    )
    # Top rectangle
    top_heigh = mm_a_pixeles(15)
    draw.rectangle(
        (0,0, CARD_WIDTH_PX -1, top_heigh),
        fill=BORDER_COLOR
    )
    # Dibujar el área blanca interior (donde van los números)
    inner_rect = (
        BORDER_THICKNESS, top_heigh, 
        CARD_WIDTH_PX - BORDER_THICKNESS, CARD_HEIGHT_PX - BORDER_THICKNESS
    )
    draw.rectangle(inner_rect, fill=BACKGROUND_COLOR)

    # Coordenadas para la cuadrícula interna de 5x5
    cell_width = (inner_rect[2] - inner_rect[0]) / 5
    cell_height = (inner_rect[3] - inner_rect[1]) / 5

    # Dibujar la cuadrícula y rellenar números
    for r in range(6):
        for c in range(5):
            x1 = inner_rect[0] + c * cell_width
            y1 = inner_rect[1] + r * cell_height - cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height


            # Escribir encabezado B I N G O
            if r == 0:
                header_text = COLUMNAS[c]
                text_bbox = draw.textbbox((0,0), header_text, font=FONT_HEADER)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                draw.text(
                    (x1 + (cell_width - text_width) / 2, y1 + (cell_height - text_height) / 2),
                    header_text, 
                    fill=TEXT_COLOR, 
                    font=FONT_HEADER
                )
            else:
                # Dibujar línea de la cuadrícula
                draw.rectangle((x1, y1, x2, y2), outline=GRID_COLOR, width=1)

            # Escribir números o "Libre"
            if r > 0: # Saltamos la fila de encabezados para los números
                if df_carton.columns[c] == 'N' and r == 3:  # Celda central
                    # Abrir el logo
                    try:
                        logo = Image.open("./assets/img/logo.png").convert("RGBA")

                        # Ajustar tamaño del logo para que encaje en la celda
                        logo = logo.resize((int(cell_width-6), int(cell_height-6)), Image.LANCZOS)

                        # Pegar el logo en la celda
                        img.paste(logo, (int(x1+3), int(y1+3)), logo)  # usa el canal alfa como máscara
                    except IOError:
                        print("No se encontró logo.png, usando celda roja por defecto")
                        draw.rectangle((x1, y1, x2, y2), fill=FREE_SPACE_COLOR, outline=GRID_COLOR, width=1)
                        num_text = "Libre"
                        font = FONT_FREE
                        text_color = FREE_SPACE_TEXT_COLOR
                        text_bbox = draw.textbbox((0,0), num_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        draw.text(
                            (x1 + (cell_width - text_width) / 2, y1 + (cell_height - text_height) / 2),
                            num_text,
                            fill=text_color,
                            font=font
                        )
                else:
                    num_text = str(df_carton.iloc[r-1, c]) # r-1 porque la fila 0 es el encabezado
                    font = FONT_NUMBERS
                    text_color = TEXT_COLOR
                
                # Centrar texto
                text_bbox = draw.textbbox((0,0), num_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                draw.text(
                    (x1 + (cell_width - text_width) / 2, y1 + (cell_height - text_height) / 2),
                    num_text, 
                    fill=text_color, 
                    font=font
                )
    
    return img

# --- 4. Función principal para generar la hoja JPG ---

def generar_hoja_bingo_jpg(cantidad_cartones, cols=0, rows=0):
    """
    Genera y organiza múltiples cartones de bingo en una imagen JPG
    simulando una hoja de tamaño carta.
    """
    
    # Calcular cuántos cartones caben por fila y columna
    num_cols_page = (PAGE_WIDTH_PX - 2 * PAGE_MARGIN_PX + CARD_SPACING_PX) // (CARD_WIDTH_PX + CARD_SPACING_PX)
    num_rows_page = (PAGE_HEIGHT_PX - 2 * PAGE_MARGIN_PX + CARD_SPACING_PX) // (CARD_HEIGHT_PX + CARD_SPACING_PX)
    #num_cols_page = cols
    #num_rows_page = rows
    
    if num_cols_page == 0 or num_rows_page == 0:
        print("Error: Los cartones son demasiado grandes para la página o los márgenes.")
        return

    cartones_por_pagina = num_cols_page * num_rows_page
    
    # Asegurarse de que al menos un cartón se puede generar
    if cartones_por_pagina == 0:
        print("No se pueden colocar cartones en la página con los tamaños y márgenes dados.")
        return

    # Creamos la imagen de la hoja
    sheet_img = Image.new('RGB', (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), BACKGROUND_COLOR)
    
    current_card_count = 0
    card_images = []

    # Generar y dibujar los cartones individuales
    print(f"Generando {cantidad_cartones} cartones y dibujándolos...")
    for i in range(cantidad_cartones):
        df_carton = generar_carton_bingo()
        card_img = dibujar_carton(df_carton, i + 1)
        card_images.append(card_img)

    # Pegar los cartones en la hoja
    for idx, card_img in enumerate(card_images):
        if idx >= cartones_por_pagina:
            print(f"Advertencia: Se generaron {cantidad_cartones} cartones, pero solo caben {cartones_por_pagina} en la hoja.")
            break
            
        row = idx // num_cols_page
        col = idx % num_cols_page

        x_offset = PAGE_MARGIN_PX + col * (CARD_WIDTH_PX + CARD_SPACING_PX)
        y_offset = PAGE_MARGIN_PX + row * (CARD_HEIGHT_PX + CARD_SPACING_PX)
        info = { 'idx': idx, 'row': row, 'col': col}
        logging.info(f"{info}")

        sheet_img.paste(card_img, (x_offset, y_offset))
        current_card_count += 1

    output_filename = f"cartones_bingo_hoja_{current_card_count}.jpg"
    sheet_img.save(output_filename, quality=90, dpi=(DPI, DPI)) # Guarda con DPI para impresión
    print(f"\n✅ Se generó '{output_filename}' con {current_card_count} cartones.")
    print(f"Tamaño de la página: {PAGE_WIDTH_MM}mm x {PAGE_HEIGHT_MM}mm ({PAGE_WIDTH_PX}x{PAGE_HEIGHT_PX}px a {DPI} DPI)")

def calc_columns_and_rows(cartones_per_page: int):
    """
    Calcula cuántas columnas y filas se deben usar en la página
    basándose en el tamaño de la página y la cantidad de cartones deseada.
    Devuelve (num_cols, num_rows).
    """

    # Relación de aspecto de la página
    aspect_ratio = PAGE_WIDTH_PX / PAGE_HEIGHT_PX

    # Empezamos buscando factores de cartones_per_page
    posibles = []
    for filas in range(1, cartones_per_page + 1):
        if cartones_per_page % filas == 0:
            cols = cartones_per_page // filas
            posibles.append((cols, filas))

    # Elegimos la combinación cuya proporción columnas/filas
    # se acerque más a la proporción de la página
    mejor_cols, mejor_filas = min(
        posibles,
        key=lambda x: abs((x[0] / x[1]) - aspect_ratio)
    )

    return mejor_cols, mejor_filas

def calc_carton_sizes(rows, columns):
    width = int( (PAGE_WIDTH_PX - PAGE_MARGIN_PX) / columns) 
    heigh = int((PAGE_HEIGHT_MM - PAGE_MARGIN_PX)/rows)
    carton_width = min(width, heigh)- CARD_SPACING_PX
    carton_heigh = carton_width

    offset_width = int((width - carton_width)/2)
    offset_heigh = int((heigh - carton_heigh)/2)

    return carton_width, carton_heigh, offset_width, offset_heigh
    
def calc_sizes(cartones_per_page, paper_size, total_cartones):
    set_paper_size(paper_size=paper_size)
    columns, rows = calc_columns_and_rows(cartones_per_page)
    carton_width, carton_heigh, offset_width, offset_heigh = calc_carton_sizes(rows, columns)
    CARD_WIDTH_PX = carton_width
    CARD_HEIGHT_PX = carton_heigh
    CARD_SPACING_PX = offset_width * 2

    return columns, rows

# --- Ejecución del programa ---
if __name__ == '__main__':
    
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    CANTIDAD_DESEADA_CARTONES = 6 # Puedes cambiar esta cantidad
    paper_size = 'letter'
    #cols, rows = calc_sizes(CANTIDAD_DESEADA_CARTONES, paper_size)
    generar_hoja_bingo_jpg(CANTIDAD_DESEADA_CARTONES) #, cols, rows)
