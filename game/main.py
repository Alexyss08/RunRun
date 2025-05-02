import pygame
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from assets.mapa_objects import generate_valid_map_recursive, save_map_to_file
from Enemy import Enemy
from hero import Hero
from pygame.sprite import Sprite
from pygame.sprite import Group

pygame.init()

# Configuración de la pantalla
length = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = (length, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pantalla del joc")


class Block(Sprite):
    height = pygame.display.Info().current_h
    length = pygame.display.Info().current_w
    rock_size = height // 10
    quantitat_roques = height // rock_size * length // rock_size

    def __init__(self, x, y):
        super().__init__()
        self.rock_image = pygame.image.load("assets/mapa/PNG/stones_6.png")
        self.bg_image = pygame.image.load("assets/mapa/PNG/bg.png")
        self.gold_image = pygame.image.load("assets/mapa/PNG/decor_3.png") # REPLACE WITH THE CORRECT IMAGE PATH
        self.rock_image = pygame.transform.scale(self.rock_image, (Block.rock_size, Block.rock_size))
        self.bg_image = pygame.transform.scale(self.bg_image, (Block.rock_size, Block.rock_size))
        self.rect_bg = self.bg_image.get_rect()
        self.rect_bg.x = x
        self.rect_bg.y = y
        self.rect = self.rock_image.get_rect()
        self.rect.x = x
        self.rect.y = y


def make_terrain():
    with open("assets/mapa.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "T":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

terrain = make_terrain()

rocks_group = Group()

def make_terrain_stones():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "#":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

def make_terrain_empty():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "T":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

gold_group = Group() # Crear un grupo de sprites para el oro

def make_terrain_gold():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "G":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain
random_map = generate_valid_map_recursive(rows=10, cols=18, characters="#GTES") # Generar el mapa aleatorio
save_map_to_file(random_map, "assets/mapa_roques.txt") # Guardar el mapa en el archivo mapa_roques.txt
rocks = make_terrain_stones() # Crear los bloques de rocas
gold = make_terrain_gold() # Crear los bloques de oro
for block in gold: # Añadir los bloques al grupo de sprites
    gold_group.add(block)
for block in rocks: # Añadir los bloques al grupo de sprites
    rocks_group.add(block)

def set_spawn_point():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "S":  # 'S' indica el punto de spawn
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    return coord_x, coord_y  # Devuelve las coordenadas del spawn
            i += 1
    return 0, 0  # Valor por defecto si no se encuentra un punto de spawn

def horitzontal_collision(hero, rocks_group):
    block = pygame.sprite.spritecollideany(hero, rocks_group)
    if block:
        if hero.rect.right > block.rect.left and hero.rect.centerx < block.rect.centerx:
            hero.rect.right = block.rect.left
        elif hero.rect.left < block.rect.right and hero.rect.centerx > block.rect.centerx:
            hero.rect.left = block.rect.right


def vertical_collision(hero, rocks_group):
    block = pygame.sprite.spritecollideany(hero, rocks_group)
    if block:
        if hero.rect.bottom > block.rect.top and hero.rect.centery < block.rect.centery:
            hero.rect.bottom = block.rect.top
        elif hero.rect.top < block.rect.bottom and hero.rect.centery > block.rect.centery:
            hero.rect.top = block.rect.bottom


# Configuración de FPS
FPS = 30
clock = pygame.time.Clock()

# HERO
hero = Hero()
spawn_x, spawn_y = set_spawn_point()
hero.rect.center = (spawn_x, spawn_y)  # Establecer la posición inicial del héroe

# Crear grupo de enemigos
enemy_group = pygame.sprite.Group()

# Función para generar enemigos
def spawn_enemies():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "E":  # 'E' indica la posición de un enemigo
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    enemy = Enemy(coord_x, coord_y)  # Crear un enemigo en las coordenadas
                    enemy_group.add(enemy)  # Añadir el enemigo al grupo
            i += 1

# Generar enemigos en las posiciones marcadas con 'E'
spawn_enemies()

# Main loop
run = True
while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    # Primero comprueba si está atacando
    is_attacking = hero.attack(keys, rocks_group, enemy_group)

    # Solo permite moverse si no está atacando
    if not is_attacking:
        hero.move(keys, rocks_group)

    # Comprobar colisions
    horitzontal_collision(hero, rocks_group)
    vertical_collision(hero, rocks_group)

    # Draw terrain
    for block in terrain:
        screen.blit(block.bg_image, block.rect_bg)

    for block in rocks:
        screen.blit(block.rock_image, block.rect)
    
    for block in gold:
        screen.blit(block.gold_image, block.rect)

    # Actualizar y dibujar enemigos DESPUÉS del terreno
    for enemy in enemy_group:
        enemy.update(hero, rocks_group)
        enemy.draw(screen)

    hero.update()
    hero.draw()

    pygame.display.flip()

pygame.quit()
