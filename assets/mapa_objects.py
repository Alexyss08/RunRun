import random

def generate_valid_map_recursive(rows=10, cols=18, characters="#GTES"):
    """
    Genera recursivamente un mapa válido con:
    - Un solo héroe ('S').
    - Todos los enemigos ('E') y oro ('G') accesibles desde el héroe sin pasar por piedras ('#').
    """

    def generate_map():
        characters_without_s = characters.replace('S', '')
        weights = [0.3, 0.1, 0.9, 0.1]  # Pesos para #, G, T, E (sin S)
        
        if len(weights) != len(characters_without_s):
            raise ValueError("El número de pesos no coincide con el número de caracteres disponibles.")
        
        myMap = [''.join(random.choices(characters_without_s, weights, k=cols)) for _ in range(rows)]
        hero_row = random.randint(0, rows - 1)
        hero_col = random.randint(0, cols - 1)
        myMap[hero_row] = myMap[hero_row][:hero_col] + 'S' + myMap[hero_row][hero_col + 1:]
        return myMap

    def is_valid(map_data):
        rows = len(map_data)
        cols = len(map_data[0])
        visited = set()

        # Encontrar al héroe
        for r in range(rows):
            for c in range(cols):
                if map_data[r][c] == 'S':
                    start_pos = (r, c)
                    break
            else:
                continue
            break
        else:
            return False

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if (r, c) in visited or map_data[r][c] == '#':
                return
            visited.add((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        dfs(start_pos[0], start_pos[1])

        for r in range(rows):
            for c in range(cols):
                if map_data[r][c] in 'E' and (r, c) not in visited:
                    return False
        return True

    # Generar y validar el mapa
    map_data = generate_map()
    if is_valid(map_data):
        return map_data
    else:
        return generate_valid_map_recursive(rows, cols, characters)  # llamada recursiva


def save_map_to_file(map_data, file_path):
    """
    Guarda un mapa en un archivo de texto.
    
    :param map_data: Lista de cadenas representando el mapa.
    :param file_path: Ruta del archivo donde se guardará el mapa.
    """
    with open(file_path, 'w') as file:
        for row in map_data:
            file.write(row + '\n')

# Generar el mapa válido
valid_map = generate_valid_map_recursive()

# Guardar el mapa válido en el archivo mapa_roques.txt
save_map_to_file(valid_map, "assets/mapa_roques.txt")
print("Mapa válido generado y guardado en 'assets/mapa_roques.txt'.")
