import pygame
from os import listdir

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Animation
        self.animationlist_imgs = {
            'Dash1' : [],
            'Idle' : [],
            'Jump' : [],
            'Walk' : []
        }
        self.load_images()
        self.animation_index = 0
        self.animation_type = 'Idle'
        self.current_image = self.animationlist_imgs[self.animation_type][self.animation_index]
        self.current_image_rec = self.current_image.get_rect()
        self.animation_timer = 2
        self.animation_counter = 0

        # Movement
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.init = True
        self.speed = pygame.math.Vector2(0, 0)
        self.flip_char = False
        self.gravity = 1
        self.jump_pressed = False
        self.running = False
        self.lives = 5
        self.max_speed = 5  # Can be modified by water/hazards
        
        # Jump Attributes
        self.jump_buffer = 5 
        self.jump_buffer_counter = 0
        self.dash1 = False
        self.dash2 = False
        self.land = False

        # Dash
        self.dash_speed = 12
        self.is_dashing = False
        self.dash_time = 0
        self.dash_duration = 15  
        self.dash_cooldown = 40 
        self.dash_cooldown_counter = 0
        self.dash_pressed = False

    def load_images(self):
        
        path = 'Assets\\Player\\'
        for name in listdir(path):
            for img_name in listdir(path + name):
                img = pygame.image.load(path + name + '\\' + img_name)
                img = pygame.transform.scale(img, (64, 64))
                img = img.subsurface(22, 10, 22, 40)
                self.animationlist_imgs[name].append(img)

    def handle_datseffect1(self):
        K = pygame.key.get_pressed()
        
        # Decrease cooldown
        if self.dash_cooldown_counter > 0:
            self.dash_cooldown_counter -= 1
        
        # Check for dash input (Q key)
        if K[pygame.K_q] and not self.dash_pressed and self.dash_cooldown_counter == 0:
            self.is_dashing = True
            self.dash_time = self.dash_duration
            self.dash_cooldown_counter = self.dash_cooldown
            self.animation_type = 'Dash1'
            self.animation_index = 0
            self.dash_pressed = True
        
        if not K[pygame.K_q]:
            self.dash_pressed = False
        
        # Execute dash
        if self.is_dashing:
            self.dash_time -= 1
            # Dash in facing direction
            self.speed.x = -self.dash_speed if self.flip_char else self.dash_speed
            
            if self.dash_time <= 0:
                self.is_dashing = False
    
    def get_keys(self):
        K = pygame.key.get_pressed()

        # Handle dash first
        self.handle_datseffect1()
        
        # Don't process other input during dash
        if self.is_dashing:
            return

        if K[pygame.K_w]:
            if (self.land or self.jump_buffer_counter > 0) and not self.jump_pressed:
                self.gravity = -18
                self.land = False
                self.jump_buffer_counter = 0
                self.set_animation('Jump')
            self.jump_pressed = True
        else:
            self.jump_pressed = False

        if K[pygame.K_a]:
            if self.speed.x >= -self.max_speed:  # Use max_speed instead of hardcoded 5
                self.speed.x += -0.2
            self.running = True
            self.flip_char = True
            self.set_animation('Walk')

        elif K[pygame.K_d]:
            if self.speed.x <= self.max_speed:  # Use max_speed instead of hardcoded 5
                self.speed.x += 0.2
            self.flip_char = False
            self.running = True 
            self.set_animation('Walk')
        
        else:
            if abs(self.speed.x) > 0.8:
                if self.speed.x < 0: 
                    self.speed.x += 0.8
                elif self.speed.x > 0:
                    self.speed.x -= 0.8
            else: 
                self.speed.x = 0
                
            self.running = False
            if self.land:
                self.set_animation('Idle')
    
    def animate_images(self):
        self.animation_counter += 1
        if self.animation_counter == self.animation_timer:
            self.animation_counter = 0
            try:
                self.animation_index += 1
                self.current_image = self.animationlist_imgs[self.animation_type][self.animation_index] 

            except IndexError:
                self.animation_index = 0
    
    def set_animation(self, new):
        if self.animation_type != new:
            if self.running and new == 'Walk':
                self.animation_type = 'Walk'
                self.animation_index = 0

            else:
                self.animation_type = 'Idle'
                self.animation_index = 0
                
    def draw_images(self, surf):
        self.animate_images()
        self.current_image_rec = self.current_image.get_rect()
        self.current_image_rec.topleft = (self.pos.x, self.pos.y)
             
        # Get a fresh copy and flip it if needed
        img_to_draw = self.current_image
        if self.flip_char:
            img_to_draw = pygame.transform.flip(self.current_image, True, False)
        
        surf.blit(img_to_draw, self.current_image_rec)
    
    def gpull(self): 
        if self.land:
            self.jump_buffer_counter = self.jump_buffer
        elif self.jump_buffer_counter > 0:
            self.jump_buffer_counter -= 1
            
        if not self.land and self.gravity < 15:
            self.gravity += 2
        
        self.speed.y = self.gravity
        self.pos.y += self.speed.y