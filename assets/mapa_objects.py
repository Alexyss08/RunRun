import random

def generate_random_map(rows=10, cols=18, characters="#G "):
    """
    Genera un mapa aleatorio con caracteres dados.
    
    :param rows: Número de filas.
    :param cols: Número de columnas.
    :param characters: Cadena de caracteres posibles.
    :return: Lista de cadenas representando el mapa.
    """
    weights = [0.4, 0.2, 0.6]
    
    # Filtrar caracteres y pesos con peso mayor a 0
    filtered_characters = [char for char, weight in zip(characters, weights) if weight > 0]
    filtered_weights = [weight for weight in weights if weight > 0]
    
    myMap = [''.join(random.choices(filtered_characters, weights=filtered_weights, k=cols)) for _ in range(rows)]

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

# Imprimir el mapa en la consola
for row in random_map:
    print(row)