import random
import pandas as pd

# Definición de los rangos estándar para las columnas de Bingo (B-I-N-G-O)
# B: 1-15, I: 16-30, N: 31-45, G: 46-60, O: 61-75
RANGOS_BINGO = {
    'B': (1, 15),
    'I': (16, 30),
    'N': (31, 45),
    'G': (46, 60),
    'O': (61, 75)
}
COLUMNAS = list(RANGOS_BINGO.keys())

def generar_numeros_carton():
    """Genera un cartón de lotería/bingo de 5x5."""
    carton = {}
    
    for columna, (min_val, max_val) in RANGOS_BINGO.items():
        # Selecciona 5 números únicos al azar dentro del rango de la columna
        # La columna 'N' tendrá solo 4 números + el espacio libre
        cantidad_numeros = 5
        if columna == 'N':
            cantidad_numeros = 4
            
        numeros = random.sample(range(min_val, max_val + 1), k=cantidad_numeros)
        carton[columna] = numeros
    
    # Añade el "Free Space" al centro del cartón (Columna 'N', posición 2 - índice 2)
    carton['N'].insert(2, '')
    
    # Transponer los datos para crear el DataFrame
    # Las claves son las columnas (B, I, N, G, O) y los valores son las filas (0-4)
    df_carton = pd.DataFrame(carton)
    return df_carton

def generar_e_imprimir_cartones(cantidad=1):
    """Genera la cantidad de cartones solicitada y los guarda en un archivo."""
    
    print(f"Generando {cantidad} cartón(es) de lotería...")
    
    with open('cartones_loteria.txt', 'w') as f:
        for i in range(1, cantidad + 1):
            carton = generar_numeros_carton()
            
            # --- Formateo de la salida ---
            titulo = f"--- CARTÓN {i:03d} ---"
            
            # Guarda en el archivo de texto
            f.write(titulo + '\n')
            f.write(carton.to_string(index=False) + '\n\n')
            
            # Muestra en la consola (opcional)
            print('\n' + titulo)
            print(carton.to_string(index=False))
            print("----------------------")

# --- Ejecución del Programa ---
# Cambia el número para generar la cantidad de cartones que necesitas
if __name__ == '__main__':
    GENERAR_CANTIDAD = 5
    generar_e_imprimir_cartones(GENERAR_CANTIDAD)

    print(f"\n✅ ¡Generación completada! Los cartones se guardaron en 'cartones_loteria.txt'")