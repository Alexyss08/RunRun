import pygame
from pygame.sprite import Sprite

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
        # Es trindira que reescalar la imatge
        self.rock_image = pygame.image.load("assets/mapa/PNG/stones_6.png")  # Replace with the correct image path
        self.bg_image = pygame.image.load("assets/mapa/PNG/bg.png")
        self.rock_image = pygame.transform.scale(self.rock_image, (Block.rock_size, Block.rock_size))
        self.bg_image = pygame.transform.scale(self.bg_image, (Block.rock_size, Block.rock_size))
        self.rect_bg = self.bg_image.get_rect()
        self.rect_bg.x = x
        self.rect_bg.y = y
        self.rect_rock = self.rock_image.get_rect()
        self.rect_bg.x = x
        self.rect_bg.y = y
        self.rect_rock.x = x
        self.rect_rock.y = y

def make_terrain():
    with open("assets/mapa.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()  # Read all lines from the file
        for row in mapa:
            row = row.strip()  # Remove any trailing newline or whitespace
            for j in range(len(row)):
                if row[j] == "#":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

def make_terrain_stones():
    with open("assets/mapa_roques.txt") as file:
        i = 0
        terrain = []
        mapa = file.readlines()  # Read all lines from the file
        for row in mapa:
            row = row.strip()  # Remove any trailing newline or whitespace
            for j in range(len(row)):
                if row[j] == "#":
                    coord_x = Block.rock_size * j
                    coord_y = Block.rock_size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

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
        self.rect = self.img.get_rect()
        self.rect.x = (length - self.rect.width) // 2
        self.rect.y = (height - self.rect.height) // 2
    
    def cut_sprites(self):
        sprite_width = 64
        sprite_height = 64
        num_sprites = 12

        self.sprites = []
        for j in range(num_sprites):
            rect = pygame.Rect(j * sprite_width, 0, sprite_width, sprite_height)
            sprite = self.sprite_sheet_idle.subsurface(rect)
            # Escalar el sprite
            scaled_sprite = pygame.transform.scale(sprite, (sprite_width, sprite_height))
            self.sprites.append(scaled_sprite)
        
        return self.sprites

    def move(self, keys):
        move = 30
        if keys[pygame.K_LEFT]:
            self.rect.x -= move
            if self.rect.x < 0:
                self.rect.x = length
        if keys[pygame.K_RIGHT]:
            self.rect.x += move
            if self.rect.x > length:
                self.rect.x = 0
        if keys[pygame.K_UP]:
            self.rect.y -= move
            if self.rect.y < 0:
                self.rect.y = height
        if keys[pygame.K_DOWN]:
            self.rect.y += move
            if self.rect.y > height:
                self.rect.y = 0
    
    def update(self):
        update_rate = 5
        hero.sprite_idx += 1
        if hero.sprite_idx >= update_rate * len(hero.sprites):
            hero.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx // update_rate] 

    def draw(self):
        screen.blit(self.img, self.rect)

# Configuración de FPS
FPS = 30
clock = pygame.time.Clock()

# HERO
hero = Hero()

# Generate terrain
terrain = make_terrain()
rocks = make_terrain_stones()

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
    
    hero.move(keys)

    # Draw terrain
    for block in terrain:
        screen.blit(block.bg_image, block.rect_bg)

    for block in rocks:
        screen.blit(block.rock_image, block.rect_rock)

    hero.update()
    hero.draw()

    pygame.display.flip()

pygame.quit()