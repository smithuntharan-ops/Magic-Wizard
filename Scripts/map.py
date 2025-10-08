#tile size 32x32 pixels
import pygame
from os import listdir
import csv

pygame.init()
pygame.font.init()

# Screen --------------------------------------- #
SCREEN_RES = (1060, 640)
screen = pygame.display.set_mode(SCREEN_RES)
Background_img = pygame.image.load('Assets\\Background\\background.png').convert_alpha()
Background_img.fill((10, 10, 10), special_flags = pygame.BLEND_RGB_ADD)
Background_img_rect = Background_img.get_rect()
sidepanel = pygame.Rect(760, 0, 300, 640)
shiftx, shifty = 0, 0
clock = pygame.time.Clock()

# Side Panel ------------------------------------ #
Tiles_List = {}
# Mapping from integer ID (as string) to tile name
world_data = {
   '0' : 'dirt',
   '1' : 'lava',
   '2' : 'lavadown',
   '3' : 'platform',
   '6' : 'toptile',
   '7' : 'water', 
   '8' : 'waterdown',
   '9' : 'yplayer',
   '10' : 'yyenemy',
   '11' : 'yyydoor'
}

world_data_reverse = {v: k for k, v in world_data.items()}


current_tile_selected = 'dirt'
mousex, mousey = pygame.mouse.get_pos() 
tile_pos = [] 
tiles_in_map = [] 
font = pygame.font.SysFont('Assets\\UI\\lemonmilk.ttf', 30)
current_level = 1

# Buttons -------------------------------------- #
trigger = True
next_button = pygame.image.load('Assets\\UI\\next.png')
next_button_rect = next_button.get_rect()
next_button_rect.x, next_button_rect.y = 1010, 70
prev_button = pygame.image.load('Assets\\UI\\previous.png')
prev_button_rect = prev_button.get_rect()
prev_button_rect.x, prev_button_rect.y = 810, 70

# Buttons List ---------------------------------- # 
Buttons_List = {
   'next' : [next_button, next_button_rect],
   'prev' : [prev_button, prev_button_rect]
}

# Functions ------------------------------------- #

def draw_grids():
   for i in range(60):
      pygame.draw.line(Background_img, (255, 255, 255), (i*32, 0), (i*32, 960))

   for i in range(40):
      pygame.draw.line(Background_img, (255, 255, 255), (0, i*32), (1920, i*32))

def load_images():
   path = 'Assets\\Tileset'
   for imgid, name_with_ext in enumerate(listdir(path)):
      img = pygame.image.load(path + '\\' + name_with_ext).convert_alpha()
      img = pygame.transform.scale(img, (32, 32))
      name = name_with_ext[:-4]
      Tiles_List[name] = [img, img.get_rect(), str(imgid)]

def fill_sidepanel():

   ctr = 0
   lst = [820, 150]
   for name in Tiles_List: 
      rec = Tiles_List[name][1]
      img = Tiles_List[name][0]
      screen.blit(img, (lst[0], lst[1]))
      rec.x, rec.y = lst[0], lst[1]
      lst[0] += 150
      if ctr == 1:
         ctr = 0
         lst[0] = 820 
         lst[1] += 50
      else:
         ctr += 1

def update_bg():
   global shiftx, shifty, mousex, mousey, tile_pos
   K = pygame.key.get_pressed()
   
   if K[pygame.K_RIGHT] and Background_img_rect.x > -(Background_img.get_width() - 750): 
      Background_img_rect.x -= 8
      shiftx -= 8
   if K[pygame.K_LEFT] and Background_img_rect.x < 0: 
      Background_img_rect.x += 8
      shiftx += 8
   if K[pygame.K_DOWN] and Background_img_rect.y > -(Background_img.get_height() - SCREEN_RES[1]): 
      Background_img_rect.y -= 8 
      shifty -= 8
   if K[pygame.K_UP] and Background_img_rect.y < 0: 
      Background_img_rect.y += 8
      shifty += 8

   
   mousex, mousey = pygame.mouse.get_pos() 
   
   
   tile_pos = [(mousex - shiftx) // 32, (mousey - shifty) // 32]
   
def collision_mouse(data):
   global current_tile_selected
   
   M = pygame.mouse.get_pressed()
   for name in data:
      rec = Tiles_List[name][1]
    
      if rec.collidepoint(mousex, mousey):
         if M[0]: 
            current_tile_selected = name
      
     
      if name == current_tile_selected:
            pygame.draw.rect(screen, (0, 0, 0), rec, 2)

def collision_button(data):
   global current_level, trigger, tiles_in_map

   M = pygame.mouse.get_pressed()
   for name in data:
      rec = Buttons_List[name][1]
      if rec.collidepoint(mousex, mousey):
         if M[0] and name == 'next' and trigger:
            current_level += 1
            trigger = False
            load_world(current_level)
         elif M[0] and name == 'prev' and current_level > 1 and trigger:
            current_level -= 1
            trigger = False
            load_world(current_level) 
         
         if not M[0]: 
            trigger = True 
                 
def draw_buttons():
   for button in Buttons_List:
      img = Buttons_List[button][0]
      rec = Buttons_List[button][1]
      screen.blit(img, rec)

def place_update_tiles():
   global current_tile_selected, tiles_in_map, temp_world

   path = 'Assets\\Tileset\\'
   M = pygame.mouse.get_pressed()

   
   if mousex < sidepanel.x:
      
      grid_x, grid_y = tile_pos[0], tile_pos[1]
      if 0 <= grid_y < len(temp_world) and 0 <= grid_x < len(temp_world[0]):
         if M[0]:
            
            if temp_world[grid_y][grid_x] != world_data_reverse[current_tile_selected]:
               # Visual
               img = Tiles_List[current_tile_selected][0]
               rec = img.get_rect()
               rec.x, rec.y = grid_x * 32, grid_y * 32
               tiles_in_map.append((img, rec, (grid_x, grid_y)))

               # Data
               temp_world[grid_y][grid_x] = Tiles_List[current_tile_selected][2]
         
         elif M[2]:
            
            for i, (img, rec, (tx, ty)) in enumerate(tiles_in_map):
               if tx == grid_x and ty == grid_y:
                  tiles_in_map.pop(i)
                  temp_world[grid_y][grid_x] = ' ' 
                 

   # Blit all tiles currently in the map, applying camera shift
   for img, rec, (tx, ty) in tiles_in_map:
      screen.blit(img, (tx * 32 + shiftx, ty * 32 + shifty))

def load_world(level):
   global temp_world, tiles_in_map, shiftx, shifty

   tiles_in_map.clear()
   shiftx, shifty = 0, 0 

   try:
      with open(f'Assets\\Mapdata\\Level{level}.csv', 'r') as file:
         data = list(csv.reader(file))
         temp_world = data
   
   except FileNotFoundError:
      
      temp_world = [[' ' for _ in range(60)] for _ in range(40)]
      
      with open(f'Assets\\Mapdata\\Level{level}.csv', 'w', newline = '') as file:
         pen = csv.writer(file)
         for row in temp_world:
            pen.writerow(row)
   
   path = 'Assets\\Tileset\\'
   for y, row in enumerate(temp_world):
      for x, data_id_str in enumerate(row):
         if data_id_str in world_data: 
            tile_name = world_data[data_id_str]
            if tile_name in Tiles_List: 
               img = Tiles_List[tile_name][0] 
               rec = img.get_rect()
               rec.x, rec.y = x * 32, y * 32 
               tiles_in_map.append([img, rec, (x, y)])
            else:
                print(f"Warning: Tile '{tile_name}' (ID: {data_id_str}) not found in Tiles_List.")
         elif data_id_str != ' ':
             print(f"Warning: Unknown tile ID '{data_id_str}' at ({x},{y}) in Level {level}. Ignoring.")

def save_data():
      with open(f'Assets\\Mapdata\\Level{current_level}.csv', 'w', newline = '') as file:
         pen = csv.writer(file)
         for row in temp_world:
            pen.writerow(row)


temp_world = [[' ' for _ in range(60)] for _ in range(40)] 
draw_grids()
load_images() 
load_world(current_level) 

# !Mainloop ----------------------------------------------- #
run = True
while run:

   clock.tick(60)

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         run = False
      if event.type == pygame.MOUSEBUTTONUP: 
         trigger = True

   update_bg()
   
   
   screen.blit(Background_img, Background_img_rect)
   place_update_tiles()
   save_data() 
   
   
   pygame.draw.rect(screen, (77, 77, 77), sidepanel)
   fill_sidepanel()


   level_text = font.render(f'Currently Editing Level {current_level}', 1, (0, 0, 0))
   screen.blit(level_text, (790, 10))
   
   draw_buttons() 

   
   collision_mouse(Tiles_List)
   collision_button(Buttons_List) 

   pygame.display.update()      

pygame.quit()
