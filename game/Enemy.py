import pygame
from pygame.sprite import Sprite
import random
pygame.init()

class Enemy(Sprite):
    height = pygame.display.Info().current_h
    length = pygame.display.Info().current_w
    enemy_size = height // 20

    def __init__(self, x, y):
        super().__init__()
        # Cambiar a una imagen de enemigo apropiada
        self.sprite_sheet = pygame.image.load("sprites/mono/PNG/Unarmed_Idle/Unarmed_Idle_full.png")
        self.sprites = self.cut_sprites()
        self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice(["left", "right", "up", "down"])
        self.move_timer = 0
        self.move_delay = 30
        self.speed = 5

    def cut_sprites(self, y_offset=0, num_sprites=8):
        sprite_width = 64
        sprite_height = 64
        sprites = []
        for j in range(num_sprites):
            rect = pygame.Rect(j * sprite_width, y_offset, sprite_width, sprite_height)
            sprite = self.sprite_sheet.subsurface(rect).copy()
            
            # Recortar el espacio transparente automáticamente
            bounding_rect = sprite.get_bounding_rect()
            sprite = sprite.subsurface(bounding_rect)
            
            scaled_sprite = pygame.transform.scale(sprite, (Enemy.enemy_size, Enemy.enemy_size))
            sprites.append(scaled_sprite)
        return sprites

    def move(self):
        # Implementar movimiento
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.direction = "right"
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.right > self.length:
                self.direction = "left"
        elif self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.direction = "down"
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rect.bottom > self.height:
                self.direction = "up"

    def update(self):
        # Actualizar movimiento
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.direction = random.choice(["left", "right", "up", "down"])
        
        self.move()

        # Actualizar animación
        update_rate = 5
        self.sprite_idx += 1
        if self.sprite_idx >= update_rate * len(self.sprites):
            self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx // update_rate]

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Cambié el color a rojo para distinguir mejor