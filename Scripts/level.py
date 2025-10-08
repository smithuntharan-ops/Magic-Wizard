import pygame
from player import *
from enemy import *
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
            '9' : 'yplayer',
            '10' : 'yyenemy',
            '11' : 'yyydoor'
        }
        
        self.shiftx = 0
        self.shifty = 0

        self.tiles_in_map = []
        self.solid_tiles = []
        self.hazard_tiles = []
        self.door_tiles = []
        self.player_obj = None
        self.enemy_manager = EnemyManager()

        self.background_img = pygame.image.load('Assets\\Background\\background.png')
        self.background_rec = self.background_img.get_rect()
        self.background_rec.topleft = (0, 0)
        self.started = False
        
        self.respawn_invulnerability = 0
        self.max_invulnerability = 60
        self.in_water = False
 
    def _draw_(self, data, surf):
        for tile in data:
            tile.draw(surf)
            

    def load_level(self, level):
        self.tiles_in_map.clear()
        self.solid_tiles.clear()
        self.hazard_tiles.clear()
        self.door_tiles.clear()
        self.player_obj = None
        self.enemy_manager.clear_enemies()

        with open(f'Assets\\Mapdata\\Level{level}.csv', 'r') as file:
            data = list(reader(file))

            for y, row in enumerate(data):
                for x, tile_id in enumerate(row):
                    if tile_id != ' ':
                        if tile_id == '9':
                            new_block = Player([x * 32, y * 32])
                            self.player_obj = new_block
                            self.player_obj.current_image_rec.topleft = (x * 32, y * 32)
                        elif tile_id == '10':
                            self.enemy_manager.add_enemy([x * 32, y * 32], 'slime')
                        elif tile_id == '11':  # Door tile
                            new_block = Tile((x * 32, y * 32), 'yyydoor')
                            self.door_tiles.append(new_block)
                            self.tiles_in_map.append(new_block)  # Also add to main list for drawing
                        else:
                            if tile_id in self.world_data:
                                tile_name = self.world_data[tile_id]
                                new_block = Tile((x * 32, y * 32), tile_name)
                                self.tiles_in_map.append(new_block)
                                
                                if new_block.is_solid:
                                    self.solid_tiles.append(new_block)
                                else:
                                    self.hazard_tiles.append(new_block)
        
        if self.player_obj is None:
            self.player_obj = Player([100, 100])
            self.player_obj.current_image_rec.topleft = (100, 100)
                                
            
            if self.player_obj is None:
                self.player_obj = Player([100, 100])
                self.player_obj.current_image_rec.topleft = (100, 100)


    def find_nearest_safe_block(self):
        player_x = self.player_obj.pos.x
        player_y = self.player_obj.pos.y
        
        nearest_block = None
        min_distance = float('inf')
        
        
        for tile in self.solid_tiles:
           
            x_distance = abs(tile.rec.centerx - player_x)
            y_condition = tile.rec.top < player_y  
            distance = x_distance + (player_y - tile.rec.top) * 0.1 
            
            if y_condition and distance < min_distance:
                min_distance = distance
                nearest_block = tile
        
        
        if nearest_block is None:
            for tile in self.solid_tiles:
                if tile.rec.top < player_y: 
                    nearest_block = tile
                    break
        
        if nearest_block:
            
            self.player_obj.pos.x = nearest_block.rec.centerx - self.player_obj.current_image_rec.width // 2
            self.player_obj.pos.y = nearest_block.rec.top - self.player_obj.current_image_rec.height
            self.player_obj.current_image_rec.topleft = (int(self.player_obj.pos.x), int(self.player_obj.pos.y))  
            self.player_obj.speed.x = 0
            self.player_obj.speed.y = 0
           
            self.player_obj.land = True
            self.player_obj.gravity = 0
            self.respawn_invulnerability = self.max_invulnerability
        else:
        
            self.player_obj.pos.x = 100
            self.player_obj.pos.y = 100
            self.player_obj.current_image_rec.topleft = (100, 100)
            self.player_obj.speed.x = 0
            self.player_obj.speed.y = 0
            self.player_obj.land = False  
            self.player_obj.gravity = 1
            self.respawn_invulnerability = self.max_invulnerability

    def check_hazards(self):
        if self.respawn_invulnerability > 0:
            self.respawn_invulnerability -= 1
            self.in_water = False
            for tile in self.hazard_tiles:
                if tile.is_water and self.player_obj.current_image_rec.colliderect(tile.rec):
                    self.in_water = True
                    break
            return
        
        self.in_water = False
        
        for tile in self.hazard_tiles:
            if self.player_obj.current_image_rec.colliderect(tile.rec):
                
                if tile.is_fire:
                    self.player_obj.lives -= 1
                   
                    self.find_nearest_safe_block()
                    return 
                
                elif tile.is_water:
                    self.in_water = True

    def update_backGround(self):
        self.shiftx = 0
        self.shifty = 0
        
        player_x = self.player_obj.current_image_rec.x
        player_vx = self.player_obj.speed.x
        
        if player_x > 700 and self.background_rec.x > -960 and player_vx > 0:
            scroll = round(abs(player_vx))
            if scroll == 0 and abs(player_vx) > 0:
                scroll = 1
            scroll = min(scroll, 960 + self.background_rec.x)
            self.background_rec.x -= scroll
            self.shiftx = -scroll
            self.player_obj.pos.x -= scroll
            
        elif player_x < 260 and self.background_rec.x < 0 and player_vx < 0:
            scroll = round(abs(player_vx))
            if scroll == 0 and abs(player_vx) > 0:
                scroll = 1
            scroll = min(scroll, abs(self.background_rec.x))
            self.background_rec.x += scroll
            self.shiftx = scroll
            self.player_obj.pos.x += scroll
        
        player_y = self.player_obj.current_image_rec.y
        vertical_scroll_speed = 8
        
        if player_y < 100 and self.started and self.background_rec.y < 0:
            scroll = min(vertical_scroll_speed, abs(self.background_rec.y))
            self.background_rec.y += scroll
            self.shifty = scroll
            self.player_obj.pos.y += scroll
            self.player_obj.current_image_rec.y = round(self.player_obj.pos.y)
            
        elif player_y > 450 and self.background_rec.y > -320:
            scroll = min(vertical_scroll_speed, 320 + self.background_rec.y)
            self.background_rec.y -= scroll
            self.shifty = -scroll
            self.player_obj.pos.y -= scroll
            self.player_obj.current_image_rec.y = round(self.player_obj.pos.y)

        
    def update_Tiles(self):
        for tile in self.tiles_in_map:
            tile.rec.x += self.shiftx
            tile.rec.y += self.shifty
    
    def draw_player(self, surf):
        self.player_obj.draw_images(surf)
        
        if self.respawn_invulnerability > 0:
            if self.respawn_invulnerability % 10 < 5:
                shield_surf = pygame.Surface((self.player_obj.current_image_rec.width + 4, 
                                             self.player_obj.current_image_rec.height + 4), 
                                            pygame.SRCALPHA)
                pygame.draw.rect(shield_surf, (100, 200, 255, 100), shield_surf.get_rect(), 2)
                surf.blit(shield_surf, (self.player_obj.current_image_rec.x - 2, 
                                       self.player_obj.current_image_rec.y - 2))
        
        health_bar_x = 20
        health_bar_y = 20
        health_bar_width = 200
        health_bar_height = 20
        
        pygame.draw.rect(surf, (100, 20, 20), 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        current_width = int((self.player_obj.lives / 5) * health_bar_width)
        if self.player_obj.lives > 3:
            color = (50, 200, 50)
        elif self.player_obj.lives > 1:
            color = (200, 200, 50)
        else:
            color = (200, 50, 50)
        
        pygame.draw.rect(surf, color, 
                        (health_bar_x, health_bar_y, current_width, health_bar_height))
        
        pygame.draw.rect(surf, (255, 255, 255), 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"Lives: {self.player_obj.lives}/5", True, (255, 255, 255))
        surf.blit(health_text, (health_bar_x + 5, health_bar_y + 2))

    def collision_horizontal(self):
        self.player_obj.pos.x += self.player_obj.speed.x
        self.player_obj.current_image_rec.x = self.player_obj.pos.x
        
        for tile in self.solid_tiles:
            if tile.rec.colliderect(self.player_obj.current_image_rec):
                if self.player_obj.speed.x < 0:
                    self.player_obj.current_image_rec.left = tile.rec.right
                    self.player_obj.pos.x = self.player_obj.current_image_rec.x

                elif self.player_obj.speed.x > 0:
                    self.player_obj.current_image_rec.right = tile.rec.left
                    self.player_obj.pos.x = self.player_obj.current_image_rec.x
                
                self.player_obj.speed.x = 0

    def collision_vertical(self):
        self.player_obj.pos.y += self.player_obj.speed.y
        self.player_obj.current_image_rec.y = self.player_obj.pos.y
        
        on_ground = False
        
        for tile in self.solid_tiles:
            if tile.rec.colliderect(self.player_obj.current_image_rec):
                if self.player_obj.speed.y > 0:
                    self.player_obj.current_image_rec.bottom = tile.rec.top
                    self.player_obj.pos.y = self.player_obj.current_image_rec.y
                    self.player_obj.speed.y = 0
                    self.player_obj.gravity = 0
                    on_ground = True
                
                elif self.player_obj.speed.y < 0:
                    self.player_obj.current_image_rec.top = tile.rec.bottom
                    self.player_obj.pos.y = self.player_obj.current_image_rec.y
                    self.player_obj.speed.y = 0
                    self.player_obj.gravity = 1
        
        self.player_obj.land = on_ground

    def level_startup(self):
        if not self.started:
            self.started = True
            while self.background_rec.y > -320:
                self.background_rec.y -= 8
                self.shifty = -8
                self.player_obj.pos[1] -= 8
                self.update_Tiles()
                self.enemy_manager.update(0, self.shifty, self.solid_tiles)

    def start_level(self, surf):
        surf.blit(self.background_img, self.background_rec)
        self._draw_(self.tiles_in_map, surf)
        self._draw_(self.door_tiles, surf)
        self.level_startup()
        self.update_backGround()
        self.update_Tiles()

        self.enemy_manager.update(self.shiftx, self.shifty, self.solid_tiles)
        
        original_max_speed = 5
        if self.in_water:
            self.player_obj.max_speed = 2.5
        else:
            self.player_obj.max_speed = original_max_speed
        
        self.player_obj.get_keys()
        self.player_obj.gpull()
        
        self.collision_horizontal()
        self.collision_vertical()
        
        self.check_hazards()

        # Check door collision - REMOVE the print statement
        for tile in self.door_tiles:
            if self.player_obj.current_image_rec.colliderect(tile.rec):
                return 'level_complete'
        
        collisions = self.enemy_manager.check_collisions(
            self.player_obj.current_image_rec, 
            self.player_obj.is_dashing
        )
        
        for collision_type in collisions:
            if collision_type == 'player_damaged' and self.respawn_invulnerability == 0:
                self.player_obj.lives -= 1
                self.respawn_invulnerability = self.max_invulnerability
        
        if self.player_obj.lives <= 0:
            return 'game_over'
        
        self.enemy_manager.draw(surf)
        self.draw_player(surf)
        
        return None