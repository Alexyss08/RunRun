import random

def generate_random_map(rows=10, cols=18, characters="#GT"):
    """
    Genera un mapa aleatorio con caracteres dados.
    
    :param rows: Número de filas.
    :param cols: Número de columnas.
    :param characters: Cadena de caracteres posibles.
    :return: Lista de cadenas representando el mapa.
    """
    weights = [0.3, 0.02, 0.9] # Probabilidades de cada caracter
    
    myMap = [''.join(random.choices(characters, weights, k=cols)) for _ in range(rows)]

    return myMap

def save_map_to_file(map_data, file_path):
    """
    Guarda un mapa en un archivo de texto.
    
    :param map_data: Lista de cadenas representando el mapa.
    :param file_path: Ruta del archivo donde se guardará el mapa.
    """
    with open(file_path, 'w') as file:
        for row in map_data:
            file.write(row + '\n')

# Generar el mapa aleatorio
random_map = generate_random_map()

# Guardar el mapa en el archivo mapa_roques.txt
save_map_to_file(random_map, "assets/mapa_roques.txt")
