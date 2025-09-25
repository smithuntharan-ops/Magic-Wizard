import pygame
from os import listdir

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Animation
        self.animationlist_imgs = {
            'Dash1' : [],
            'Dash2' : [],
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
        self.gravity = 0
        self.running = False
        self.dash1 = False
        self.dash2 = False

    def load_images(self):
        
        path = 'Assets\\Player\\'
        for name in listdir(path):
            for img_name in listdir(path + name):
                img = pygame.image.load(path + name + '\\' + img_name)
                img = pygame.transform.scale(img, (64, 64))
                img = img.subsurface(20, 0, 24, 50)
                self.animationlist_imgs[name].append(img)

    def get_keys(self):
        K = pygame.key.get_pressed()

        if K[pygame.K_a] and self.current_image_rec.x > 0:
            if self.speed.x >= -3:
                self.speed.x += 0.1 * -5
            self.pos.x += self.speed.x
            self.running = True
            self.flip_char = True
            self.set_animation('Walk')

        elif K[pygame.K_d]:
            if self.speed.x <= 3:
                self.speed.x += 0.1 * 5
                self.flip_char = False
            self.pos.x += self.speed.x
            self.running = True 
            self.set_animation('Walk')
        
        else:
            if abs(self.speed.x) > 0:
                if self.speed.x < 0: self.speed.x += 0.1 * 5
                if self.speed.x > 0: self.speed.x -= 0.1 * 5
            
            else: self.speed.x = 0
            self.running = False
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
        #self.init = False
        
        #pygame.draw.rect(surf, (255, 255, 255), self.current_image_rec, width = 2)
        #self.current_image = pygame.transform.flip(self.current_image, self.flip_char, 0)
        surf.blit(self.current_image, self.current_image_rec)   

    def gpull(self):
        if self.gravity < 15:
            self.gravity += 2

        self.speed.y = self.gravity
        self.pos.y += self.speed.y