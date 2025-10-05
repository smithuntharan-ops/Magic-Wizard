import pygame
from os import listdir

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type='slime'):
        super().__init__()
        
        # Position
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        
        # Enemy properties
        self.enemy_type = enemy_type
        self.health = 2 
        self.is_alive = True
        
        # Movement
        self.move_speed = 2
        self.move_direction = 1  
        self.move_range = 100  
        self.start_x = pos[0]
        
        # Animation
        self.animation_frames = []
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 8 
        
        # Visual
        self.load_enemy_images()
        self.image = self.animation_frames[0] if self.animation_frames else self.create_backup()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)
        
        # Damage cooldown (prevent multiple hits in one dash)
        self.damage_cooldown = 0
        self.max_damage_cooldown = 30 
        
        # Hit flash effect
        self.hit_flash = 0
        self.original_image = self.image.copy()
        
    def load_enemy_images(self):

        try:
            path = f'Assets\\Enemies\\{self.enemy_type}\\'
            
            # Get all image files in the directory
            files = sorted([f for f in listdir(path) if f.endswith('.png')])
            
            for img_name in files:
                img = pygame.image.load(path + img_name)
                img = pygame.transform.scale(img, (32, 32))
                self.animation_frames.append(img)
            
            if not self.animation_frames:
                self.animation_frames.append(self.create_backup())
                
        except:
            # If directory doesn't exist, use fallback
            self.animation_frames.append(self.create_backup())
    
    def create_backup(self):
        
        size = 32
        img = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.enemy_type == 'slime':
            # Purple slime blob (box-shaped)
            pygame.draw.rect(img, (120, 50, 120), (4, 12, 24, 20))
            pygame.draw.rect(img, (80, 30, 80), (8, 16, 16, 12))
            # Eyes
            pygame.draw.circle(img, (255, 255, 255), (12, 20), 3)
            pygame.draw.circle(img, (255, 255, 255), (20, 20), 3)
            pygame.draw.circle(img, (0, 0, 0), (12, 20), 1)
            pygame.draw.circle(img, (0, 0, 0), (20, 20), 1)
        elif self.enemy_type == 'spike':
            # Red spike obstacle
            points = [(size//2, 0), (size, size), (0, size)]
            pygame.draw.polygon(img, (200, 50, 50), points)
        else:
            # Default enemy
            pygame.draw.rect(img, (150, 50, 50), (0, 0, size, size))
        
        return img
    
    def animate(self):
        
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.animation_index]
            self.original_image = self.image.copy()
    
    def take_damage(self, damage=1):
        
        if self.damage_cooldown == 0:
            self.health -= damage
            self.damage_cooldown = self.max_damage_cooldown
            self.hit_flash = 10 
            
            if self.health <= 0:
                self.is_alive = False
                return True 
        return False
    
    def check_player_collision(self, player_rect, player_is_dashing):
        
        if not self.is_alive:
            return None
            
        if self.rect.colliderect(player_rect):
            if player_is_dashing:
                # Collision
                destroyed = self.take_damage(1)
                return 'enemy_hit' if not destroyed else 'enemy_destroyed'
            else:
                # Player touching enemy without dash - damage player
                if self.damage_cooldown == 0:
                    self.damage_cooldown = self.max_damage_cooldown
                    return 'player_damaged'
        
        return None
    
    def update(self, xshift, yshift=0, tiles=[]):
        
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
        
        # Animate
        self.animate()
        
        # Enemy movement 
        old_x = self.pos.x
        self.pos.x += self.move_speed * self.move_direction
        self.rect.x = self.pos.x
        
        # Check collision with tiles
        hit_wall = False
        for tile in tiles:
            if self.rect.colliderect(tile.rec):
                # turn back
                self.pos.x = old_x
                self.rect.x = old_x
                self.move_direction *= -1
                hit_wall = True
                break
        
        # Check if enemy reached movement 
        if not hit_wall and abs(self.pos.x - self.start_x) >= self.move_range:
            self.move_direction *= -1 
        
        # Update rect 
        self.rect.y = self.pos.y
        
        # camera scroll
        self.rect.x += xshift
        self.rect.y += yshift
        
        # Update position
        self.pos.x += xshift
        self.pos.y += yshift
        self.start_x += xshift
    
    def draw(self, surf):

        if not self.is_alive:
            return
        
        img_to_draw = self.image
        if self.move_direction < 0:
            img_to_draw = pygame.transform.flip(self.image, True, False)
        
        if self.hit_flash > 0:
            flash_img = img_to_draw.copy()
            flash_img.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(flash_img, self.rect)
        else:
            surf.blit(img_to_draw, self.rect)
        
        if self.health < 2:
            health_bar_width = 32
            health_bar_height = 4
            health_x = self.rect.x
            health_y = self.rect.y - 8
            
            pygame.draw.rect(surf, (200, 50, 50), 
                           (health_x, health_y, health_bar_width, health_bar_height))
            
            current_width = int((self.health / 2) * health_bar_width)
            pygame.draw.rect(surf, (50, 200, 50), 
                           (health_x, health_y, current_width, health_bar_height))


class EnemyManager:
    
    def __init__(self):
        self.enemies = []
    
    def add_enemy(self, pos, enemy_type='slime'):
        
        enemy = Enemy(pos, enemy_type)
        self.enemies.append(enemy)
        return enemy
    
    def clear_enemies(self):
       
        self.enemies.clear()
    
    def update(self, xshift, yshift=0, tiles=[]):
       
        for enemy in self.enemies:
            enemy.update(xshift, yshift, tiles)
        
        # Remove dead enemies
        self.enemies = [e for e in self.enemies if e.is_alive]
    
    def check_collisions(self, player_rect, player_is_dashing):
       
        results = []
        for enemy in self.enemies:
            result = enemy.check_player_collision(player_rect, player_is_dashing)
            if result:
                results.append(result)
        return results
    
    def draw(self, surf):

        for enemy in self.enemies:
            enemy.draw(surf)