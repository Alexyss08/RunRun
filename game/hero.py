import pygame
from pygame.sprite import Sprite

pygame.init()

# Clase Heroe
class Hero(Sprite):
    height = pygame.display.Info().current_h
    length = pygame.display.Info().current_w
    hero_size = height // 20

    def __init__(self):
        super().__init__()
        self.sprite_sheet_idle = pygame.image.load("sprites/mono/PNG/Unarmed_Idle/Unarmed_Idle_full.png")
        self.sprite_sheet_run = pygame.image.load("sprites/mono/PNG/Unarmed_Run/Unarmed_Run_full.png")
        self.sprite_sheet_attack = pygame.image.load("sprites/mono/PNG/Sword_Walk_Attack/Sword_Walk_Attack_full.png")
        
        self.sprites = self.cut_sprites(self.sprite_sheet_idle)
        self.sprite_idx = 0
        self.img = self.sprites[self.sprite_idx]
        self.rect = self.img.get_rect()
        self.is_idle = True
        self.direction = "down"  # Dirección inicial
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 30  # Duración del ataque en segundos

    def cut_sprites(self, sprite_sheet, y_offset=0, num_sprites=8):
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
            scaled_sprite = pygame.transform.scale(sprite, (Hero.hero_size, Hero.hero_size))
            sprites.append(scaled_sprite)

        return sprites

    def cut_sprites_non_auto_cut(self, sprite_sheet, y_offset=0, num_sprites=8, margin_left=0, margin_right=0, margin_top=0, margin_bottom=0, scale_factor=1.0):
        sprite_width = 64
        sprite_height = 64

        sprites = []
        for j in range(num_sprites):
            # Obtener el sprite completo
            rect = pygame.Rect(j * sprite_width, y_offset, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect).copy()
            
            # Crear un nuevo rect con los márgenes aplicados
            new_width = sprite_width - margin_left - margin_right
            new_height = sprite_height - margin_top - margin_bottom
            new_rect = pygame.Rect(margin_left, margin_top, new_width, new_height)
            
            # Recortar el sprite según los márgenes especificados
            sprite = sprite.subsurface(new_rect)
            
            # Escalar el sprite con diferentes factores para ancho y alto
            new_width = int(Hero.hero_size * scale_factor)  # Más ancho
            new_height = Hero.hero_size  # Altura original de la hitbox
            scaled_sprite = pygame.transform.scale(sprite, (new_width, new_height))
            sprites.append(scaled_sprite)

        return sprites

    def set_run_animation(self, direction):
        """Configura la animación de correr según la dirección."""
        if direction == "left":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 64)
        elif direction == "right":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 128)
        elif direction == "up":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 192)
        elif direction == "down":
            self.sprites = self.cut_sprites(self.sprite_sheet_run, y_offset = 0)
    
    def set_attack_animation(self, direction):
        """Configura la animación de atacar según la dirección."""
        if direction == "left":
            self.sprites = self.cut_sprites_non_auto_cut(
                self.sprite_sheet_attack, 
                y_offset=64, 
                num_sprites=6,
                margin_left=5,
                margin_right=25,
                margin_top=20,
                margin_bottom=20,
                scale_factor=2.7  # Más ancho horizontalmente
            )
        elif direction == "right":
            self.sprites = self.cut_sprites_non_auto_cut(
                self.sprite_sheet_attack, 
                y_offset=128, 
                num_sprites=6,
                margin_left=5,
                margin_right=5,
                margin_top=20,
                margin_bottom=20,
                scale_factor=4  # Más ancho horizontalmente
            )
        elif direction == "up":
            self.sprites = self.cut_sprites_non_auto_cut(
                self.sprite_sheet_attack, 
                y_offset=192, 
                num_sprites=6,
                margin_left=10,
                margin_right=10,
                margin_top=13,
                margin_bottom=20,
                scale_factor=3  # Más ancho horizontalmente
            )
        elif direction == "down":
            self.sprites = self.cut_sprites_non_auto_cut(
                self.sprite_sheet_attack, 
                y_offset=0, 
                num_sprites=6,
                margin_left=15,
                margin_right=15,
                margin_top=21,
                margin_bottom=13,
                scale_factor=2.5  # Más ancho horizontalmente
            )

    def set_idle_animation(self):
        """Configura la animación de reposo según la dirección."""
        if self.direction == "left":
            self.sprites = self.cut_sprites(self.sprite_sheet_idle, y_offset = 64, num_sprites = 12)
        elif self.direction == "right":
            self.sprites = self.cut_sprites(self.sprite_sheet_idle, y_offset = 128, num_sprites = 12)
        elif self.direction == "up":
            self.sprites = self.cut_sprites(self.sprite_sheet_idle, y_offset = 192, num_sprites = 4)
        elif self.direction == "down":
            self.sprites = self.cut_sprites(self.sprite_sheet_idle, y_offset = 0, num_sprites = 12)

    def move(self, keys, *groups):
        move = 15
        self.is_idle = True  # Asume que el héroe está en reposo hasta que se detecte movimiento

        # Simular movimiento horizontal
        proposed_rect = self.rect.copy()
        if keys[pygame.K_LEFT]:
            self.is_idle = False
            self.set_run_animation("left")  # Cambiar a animación de correr hacia la izquierda
            proposed_rect.x -= move
            if not any(pygame.sprite.spritecollideany(self, group, collided=lambda s, r: proposed_rect.colliderect(r.rect)) for group in groups):
                self.rect.x -= move
            if self.rect.x < 0:
                self.rect.x = Hero.length
            self.direction = "left"

        if keys[pygame.K_RIGHT]:
            self.is_idle = False
            self.set_run_animation("right")  # Cambiar a animación de correr hacia la derecha
            proposed_rect.x += move
            if not any(pygame.sprite.spritecollideany(self, group, collided=lambda s, r: proposed_rect.colliderect(r.rect)) for group in groups):
                self.rect.x += move
            if self.rect.x > Hero.length:
                self.rect.x = 0
            self.direction = "right"

        # Simular movimiento vertical
        proposed_rect = self.rect.copy()
        if keys[pygame.K_UP]:
            self.is_idle = False
            self.set_run_animation("up")  # Cambiar a animación de correr hacia arriba
            proposed_rect.y -= move
            if not any(pygame.sprite.spritecollideany(self, group, collided=lambda s, r: proposed_rect.colliderect(r.rect)) for group in groups):
                self.rect.y -= move
            if self.rect.y < 0:
                self.rect.y = Hero.height
            self.direction = "up"

        if keys[pygame.K_DOWN]:
            self.is_idle = False
            self.set_run_animation("down")  # Cambiar a animación de correr hacia abajo
            proposed_rect.y += move
            if not any(pygame.sprite.spritecollideany(self, group, collided=lambda s, r: proposed_rect.colliderect(r.rect)) for group in groups):
                self.rect.y += move
            if self.rect.y > Hero.height:
                self.rect.y = 0
            self.direction = "down"
    
    def attack(self, keys, rocks_group, enemy_group):
        """Configura la animación de ataque y detecta colisiones con enemigos."""
        if keys[pygame.K_f]:
            self.is_idle = False
            self.is_attacking = True
            self.set_attack_animation(self.direction)
            
            # Crear un rect para el área de ataque
            attack_rect = self.rect.copy()
            if self.direction == "left":
                attack_rect.width *= 2
                attack_rect.x -= attack_rect.width
            elif self.direction == "right":
                attack_rect.width *= 2
            elif self.direction == "up":
                attack_rect.height *= 2
                attack_rect.y -= attack_rect.height
            elif self.direction == "down":
                attack_rect.height *= 2

            # Comprobar colisiones con enemigos
            for enemy in enemy_group:
                if attack_rect.colliderect(enemy.rect):
                    enemy_group.remove(enemy)  # Eliminar el enemigo

            return True
        return False


    def update(self):
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
        elif self.is_idle:
            self.set_idle_animation()

        update_rate = 5
        self.sprite_idx += 1
        if self.sprite_idx >= update_rate * len(self.sprites):
            self.sprite_idx = 0
            if self.is_attacking:  # Si estaba atacando, volver a idle
                self.is_attacking = False
                self.attack_timer = 0
        
        self.img = self.sprites[self.sprite_idx // update_rate]

    def draw(self):
        # Calcular la posición para centrar el sprite en la hitbox
        sprite_rect = self.img.get_rect()
        
        # Si está atacando hacia la izquierda, alinear con el borde derecho
        if self.direction == "left" and any(sprite.get_width() > Hero.hero_size for sprite in self.sprites):
            pos_x = self.rect.right - sprite_rect.width  # Alinear con el borde derecho
            pos_y = self.rect.centery - sprite_rect.height // 2
        else:
            # Para el resto de casos, centrar el sprite
            pos_x = self.rect.centerx - sprite_rect.width // 2
            pos_y = self.rect.centery - sprite_rect.height // 2
        
        # Dibujar el sprite
        screen = pygame.display.get_surface()
        screen.blit(self.img, (pos_x, pos_y))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Dibuja la hitbox en negro