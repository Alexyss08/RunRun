import pygame
from pygame.sprite import Sprite

pygame.init()

# Configuración de la pantalla
length = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = (length, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pantalla del joc")

# Establir el fons de pantalla
bg_img = pygame.image.load("assets/mapa/PNG/bg.png")
bg_color = (160, 160, 160)

class Block(Sprite):
    def __init__(self):
        super().__init__()
        # Es trindira que reescalar la imatge
        self.image = pygame.image.load("assets/") # Carrega la imatge
        self.image = pygame.transform.scale_by(self.image, (Block.size, Block.size))
    
def make_terrain():
    with open("mapa.txt") as file:
        i = 0
        terrain = []
        for row in mapa:
            for j in range(len(ron)):
                if row[j] == "#":
                    coord_x = Block.size * j
                    coord_y = Block.size * i
                    terrain.append(Block(coord_x, coord_y))
            i += 1
    return terrain

# Clase Heroe
class Hero(Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet_idle = pygame.image.load("sprites/sprites/PNG/Unarmed_Idle/Unarmed_Idle_full.png")
        self.sprite_sheet_run = pygame.image.load("sprites/sprites/PNG/Unarmed_Run/Unarmed_Run_full.png")
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
            self.sprites.append(sprite)
        
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
    
    screen.fill(bg_color)

    hero.update()
    hero.draw()

    pygame.display.flip()

pygame.quit()