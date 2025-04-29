import pygame
from pygame.sprite import Sprite
import random
import math

pygame.init()

class Enemy(Sprite):
    height = pygame.display.Info().current_h
    length = pygame.display.Info().current_w
    enemy_size = height // 20

    def __init__(self, x, y):
        super().__init__()
        try:
            # Cargar una única imagen
            self.image = pygame.image.load("assets/mapa/PNG/tree_10.png").convert_alpha()
            # Escalar la imagen al tamaño deseado
            self.image = pygame.transform.scale(self.image, (Enemy.enemy_size, Enemy.enemy_size))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 3  # Velocidad reducida para mejor control
            self.previous_pos = self.rect.copy()  # Guardar posición anterior
        except pygame.error as e:
            print(f"Error al cargar la imagen del enemigo: {e}")
            raise

    def move_towards_hero(self, hero, rocks_group):
        # Guardar posición anterior
        self.previous_pos = self.rect.copy()

        # Calcular dirección hacia el héroe
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        
        # Normalizar el vector de dirección
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx = dx / distance
            dy = dy / distance

        # Mover en X
        self.rect.x += dx * self.speed
        # Comprobar colisión en X
        if pygame.sprite.spritecollideany(self, rocks_group):
            self.rect.x = self.previous_pos.x

        # Mover en Y
        self.rect.y += dy * self.speed
        # Comprobar colisión en Y
        if pygame.sprite.spritecollideany(self, rocks_group):
            self.rect.y = self.previous_pos.y

    def update(self, hero, rocks_group):
        self.move_towards_hero(hero, rocks_group)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Hitbox en rojo