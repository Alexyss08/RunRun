import pygame
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from assets.mapa_objects import generate_random_map, save_map_to_file
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
random_map = generate_random_map(rows=10, cols=18, characters="#G ") # Generar el mapa aleatorio
save_map_to_file(random_map, "assets/mapa_roques.txt") # Guardar el mapa en el archivo mapa_roques.txt
rocks = make_terrain_stones() # Crear los bloques de rocas
gold = make_terrain_gold() # Crear los bloques de oro
for block in gold: # Añadir los bloques al grupo de sprites
    gold_group.add(block)
for block in rocks: # Añadir los bloques al grupo de sprites
    rocks_group.add(block)

def set_spawn_point():
    with open("assets/mapa_spawn.txt") as file:
        i = 0
        mapa = file.readlines()
        for row in mapa:
            row = row.strip()
            for j in range(len(row)):
                if row[j] == "s":  # 's' indica el punto de spawn
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    return coord_x, coord_y  # Devuelve las coordenadas del spawn
            i += 1
    return 0, 0  # Valor por defecto si no se encuentra un punto de spawn


"""# Crear groups de sprites per les colisions
rocks_group = Group()"""

"""# Afagir blocs de roques al group
rocks = make_terrain_stones()
for block in rocks:
    rocks_group.add(block)
# Afagir blocs d'or al group
gold = make_terrain_gold()
for block in gold:
    gold_group.add(block)"""


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


# Clase Heroe
class Hero(Sprite):
    height = pygame.display.Info().current_h
    length = pygame.display.Info().current_w
    hero_size = height // 10

    def __init__(self):
        super().__init__()
        self.sprite_sheet_idle = pygame.image.load("sprites/mono/PNG/Unarmed_Idle/Unarmed_Idle_full.png")
        self.sprite_sheet_run = pygame.image.load("sprites/mono/PNG/Unarmed_Run/Unarmed_Run_full.png")
        
        self.sprites = self.cut_sprites()
        
        self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx]
        
        # Ajustar el rect para que el centro coincida
        self.rect = self.img.get_rect()
        """self.rect.center = (length // 2, height // 2)  # Centrar en pantalla"""

    def cut_sprites(self):
        sprite_width = 64
        sprite_height = 64
        num_sprites = 12
        scale_factor = 3.5  # Escala el personaje

        sprites = []
        for j in range(num_sprites):
            rect = pygame.Rect(j * sprite_width, 0, sprite_width, sprite_height)
            sprite = self.sprite_sheet_idle.subsurface(rect).copy()  # Copia para evitar problemas
            
            # Recortar el espacio transparente automáticamente
            bounding_rect = sprite.get_bounding_rect()
            sprite = sprite.subsurface(bounding_rect)

            # Escalar el sprite
            new_width = bounding_rect.width * scale_factor
            new_height = bounding_rect.height * scale_factor
            scaled_sprite = pygame.transform.scale(sprite, (new_width, new_height))
            
            sprites.append(scaled_sprite)

        return sprites


    def move(self, keys, rocks_group):
        move = 30

        # Simular movimiento horizontal
        proposed_rect = self.rect.copy()
        if keys[pygame.K_LEFT]:
            proposed_rect.x -= move
            if not pygame.sprite.spritecollideany(self, rocks_group, collided=lambda s, r: proposed_rect.colliderect(r.rect)):
                self.rect.x -= move
            if self.rect.x < 0:
                self.rect.x = length

        if keys[pygame.K_RIGHT]:
            proposed_rect.x += move
            if not pygame.sprite.spritecollideany(self, rocks_group, collided=lambda s, r: proposed_rect.colliderect(r.rect)):
                self.rect.x += move
            if self.rect.x > length:
                self.rect.x = 0

        # Simular movimiento vertical
        proposed_rect = self.rect.copy()
        if keys[pygame.K_UP]:
            proposed_rect.y -= move
            if not pygame.sprite.spritecollideany(self, rocks_group, collided=lambda s, r: proposed_rect.colliderect(r.rect)):
                self.rect.y -= move
            if self.rect.y < 0:
                self.rect.y = height

        if keys[pygame.K_DOWN]:
            proposed_rect.y += move
            if not pygame.sprite.spritecollideany(self, rocks_group, collided=lambda s, r: proposed_rect.colliderect(r.rect)):
                self.rect.y += move
            if self.rect.y > height:
                self.rect.y = 0

    def update(self):
        update_rate = 5
        self.sprite_idx += 1
        if self.sprite_idx >= update_rate * len(self.sprites):
            self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx // update_rate]

    def draw(self):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Dibuja la hitbox en negro con borde de 2px



# Configuración de FPS
FPS = 30
clock = pygame.time.Clock()

# HERO
hero = Hero()
spawn_x, spawn_y = set_spawn_point()
hero.rect.center = (spawn_x, spawn_y)  # Establecer la posición inicial del héroe

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

    hero.update()
    hero.draw()

    pygame.display.flip()

pygame.quit()
