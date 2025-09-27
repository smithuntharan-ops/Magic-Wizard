import pygame
from player import *
from csv import reader
from classes import *

class Level:

    def __init__(self):
    
        self.world_data = {
        '0' : 'dirt',
        '1' : 'lava',
        '2' : 'lavadown',
        '3' : 'platform',
        '4' : 'spike1',
        '5' : 'spike2',
        '6' : 'toptile',
        '7' : 'water', 
        '8' : 'waterdown',
        '9' : 'yplayer'
        }

        # Bg Update
        self.shiftx = 0
        self.shifty = 0

        # List of elements
        self.tiles_in_map = []
        self.player_obj = None


        # Background
        self.background_img = pygame.image.load('Assets\\Background\\background.png')
        self.background_rec = self.background_img.get_rect()
        self.background_rec.topleft = (0, 0)
        self.started = False
 
    def _draw_(self, data, surf):
        for tile in data:
            tile.draw(surf)
            

    def load_level(self, level):
            with open(f'Assets\\Mapdata\\Level{level}.csv', 'r') as file:
                data = list(reader(file))

                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile != ' ':
                            if tile == '9':
                                new_block = Player([x * 32, y * 32])
                                self.player_obj = new_block
                                self.player_obj.current_image_rec.topleft = (x * 32, y * 32)
                            else:
                                new_block = Tile((x * 32, y * 32), self.world_data[tile])
                                self.tiles_in_map.append(new_block)

    def update_backGround(self):
    
        # Scroll Sides
        # 
        if self.player_obj.current_image_rec.x > 860 and self.background_rec.x > -960 and self.player_obj.speed.x > 0:
            self.player_obj.speed = 0
            self.background_rec.x += 8 
            self.shiftx = 8

        elif self.player_obj.current_image_rec.x < 100 and self.background_rec.x > 0 and self.player_obj.speed.x > 0:
            self.player_obj.speed = 0
            self.background_rec.x -= 8
            self.shiftx = -8
 
        else: self.shiftx = 0

        #  Scroll Top
        if self.player_obj.current_image_rec.y < 100 and self.started and self.background_rec.y < 0:
            self.background_rec.y += 8
            self.shifty = +8 

        elif self.player_obj.current_image_rec.y > 450 and self.background_rec.y > -320:
            self.background_rec.y -= 8
            self.shifty = -8
        
        else: self.shifty = 0

        
    def update_Tiles(self):
        for tile in self.tiles_in_map:
            tile.rec.x += self.shiftx
            tile.rec.y += self.shifty
    
    def draw_player(self, surf):
        self.player_obj.draw_images(surf)

    def collision_top_bottom(self):

        for tile in self.tiles_in_map:
            if tile.rec.colliderect(self.player_obj.current_image_rec):

                # Downward
                if self.player_obj.speed.y > 0:
                    self.player_obj.current_image_rec.bottom = tile.rec.top
                    self.player_obj.pos.y = self.player_obj.current_image_rec.y
                    self.player_obj.land = True
                
                # Upward    
                if self.player_obj.speed.y < 0:
                    self.player_obj.pos.y = tile.rec.y + 32
                    self.player_obj.pos.y = self.player_obj.current_image_rec.y 
        
        print(self.player_obj.speed.y, self.player_obj.gravity, self.player_obj.land)

    def collision_side(self):
        for tile in self.tiles_in_map:
            if tile.rec.colliderect(self.player_obj.current_image_rec):

                # Left side collison
                if self.player_obj.speed.x < 0:
                    self.player_obj.speed.x = 0
                    self.player_obj.current_image_rec.left = tile.rec.right
                    self.player_obj.pos.x = self.player_obj.current_image_rec.x

                # Right side sollison
                elif self.player_obj.speed.x > 0:
                    self.player_obj.speed.x = 0
                    self.player_obj.current_image_rec.right = tile.rec.left
                    self.player_obj.pos.x = self.player_obj.current_image_rec.x


    def level_startup(self):
        if not self.started:
            self.started = True
            while self.background_rec.y > -320:
                self.background_rec.y -= 8
                self.shifty = -8
                self.player_obj.pos[1] -= 8
                self.update_Tiles()

    def start_level(self, surf):
        # Background and Tiles
        surf.blit(self.background_img, self.background_rec)
        self._draw_(self.tiles_in_map, surf)
        self.level_startup()
        self.update_backGround()
        self.update_Tiles()

        # Player
        self.player_obj.gpull()
        
        self.collision_top_bottom()
        self.collision_side()
        self.draw_player(surf)
        self.player_obj.get_keys()
      

        