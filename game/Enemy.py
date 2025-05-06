import pygame
from pygame.sprite import Sprite
import math

pygame.init()
height = pygame.display.Info().current_h
length = pygame.display.Info().current_w
enemy_size = height // 20

class Enemy(Sprite):
    

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet_idle = pygame.image.load("sprites/enemy/PNG/Slime1/Idle/Slime1_Idle_full.png")
        self.sprite_sheet_run = pygame.image.load("sprites/enemy/PNG/Slime1/Run/Slime1_Run_full.png")
        self.sprite_sheet_death = pygame.image.load("sprites/enemy/PNG/Slime1/Death/Slime1_Death_full.png")
        self.sprite_sheet_attack = pygame.image.load("sprites/enemy/PNG/Slime1/Attack/Slime1_Attack_full.png")
        
        self.sprites = self.cut_sprites(self.sprite_sheet_idle)
        self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx]
        self.rect = self.img.get_rect()
        self.rect.x = x  # Asegurarse de que se establece la posición
        self.rect.y = y
        self.is_idle = True
        self.direction = "down"  # Dirección inicial
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 30  # Duración del ataque en segundos
        self.speed = 3

    def cut_sprites(self, sprite_sheet, y_offset=0, num_sprites=6):
        sprite_width = 64
        sprite_height = 64

        sprites = []
        for j in range(num_sprites):
            rect = pygame.Rect(j * sprite_width, y_offset, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect).copy()

            # Recortar el espacio transparente automáticamente
            bounding_rect = sprite.get_bounding_rect()
            sprite = sprite.subsurface(bounding_rect)

            # Escalar el sprite al tamaño del héroe
            scaled_sprite = pygame.transform.scale(sprite, (enemy_size, enemy_size))
            sprites.append(scaled_sprite)

        return sprites
    
    def cut_sprites_attack(self, sprite_sheet, y_offset=0, num_sprites=10):
        sprite_width = 64
        sprite_height = 64

        sprites = []
        for j in range(num_sprites):
            rect = pygame.Rect(j * sprite_width, y_offset, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect).copy()

            # Recortar el espacio transparente automáticamente
            bounding_rect = sprite.get_bounding_rect()
            sprite = sprite.subsurface(bounding_rect)

            # Escalar el sprite al tamaño del héroe
            scaled_sprite = pygame.transform.scale(sprite, (enemy_size, enemy_size))
            sprites.append(scaled_sprite)

        return sprites
    
    def set_run_animation(self, direction):
        """Configura la animación de correr según la dirección."""
        if direction == "left":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 128)
        elif direction == "right":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 192)
        elif direction == "up":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 64)
        elif direction == "down":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 0)    

    def start_attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 0
            # Cargar sprites de ataque según la dirección
            if self.direction == "left":
                self.sprites = self.cut_sprites(self.sprite_sheet_attack, y_offset=128)
            elif self.direction == "right":
                self.sprites = self.cut_sprites(self.sprite_sheet_attack, y_offset=192)
            elif self.direction == "up":
                self.sprites = self.cut_sprites(self.sprite_sheet_attack, y_offset=64)
            elif self.direction == "down":
                self.sprites = self.cut_sprites(self.sprite_sheet_attack, y_offset=0)
            self.sprite_idx = 0

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

            # Determinar la dirección basada en el movimiento dominante
            if abs(dx) > abs(dy):
                self.direction = "left" if dx < 0 else "right"
            else:
                self.direction = "up" if dy < 0 else "down"
            
            # Actualizar la animación según la dirección
            if not self.is_attacking:
                self.set_run_animation(self.direction)

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
        update_rate = 5
        
        # Calcular distancia al héroe
        distance = math.sqrt((hero.rect.centerx - self.rect.centerx)**2 + 
                            (hero.rect.centery - self.rect.centery)**2)
        
        # Si está lo suficientemente cerca, atacar
        if distance < enemy_size * 2 and not self.is_attacking:
            self.start_attack()
        
        self.sprite_idx += 1
        if self.sprite_idx >= update_rate * len(self.sprites):
            self.sprite_idx = 0
            if self.is_attacking:
                self.is_attacking = False
                self.attack_timer = 0
                self.set_run_animation(self.direction)
        
        self.img = self.sprites[self.sprite_idx // update_rate]
        
        # Solo moverse si no está atacando
        if not self.is_attacking:
            self.move_towards_hero(hero, rocks_group)

    def draw(self):
        # Calcular la posición para centrar el sprite en la hitbox
        sprite_rect = self.img.get_rect()
        
        # Si está atacando hacia la izquierda, alinear con el borde derecho
        if self.direction == "left" and any(sprite.get_width() > enemy_size for sprite in self.sprites):
            pos_x = self.rect.right - sprite_rect.width  # Alinear con el borde derecho
            pos_y = self.rect.centery - sprite_rect.height // 2
        else:
            # Para el resto de casos, centrar el sprite
            pos_x = self.rect.centerx - sprite_rect.width // 2
            pos_y = self.rect.centery - sprite_rect.height // 2
        
        # Dibujar el sprite
        screen = pygame.display.get_surface()
        screen.blit(self.img, (pos_x, pos_y))
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Hitbox en rojo