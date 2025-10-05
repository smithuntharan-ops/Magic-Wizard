import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, name):

        # Tiles
        super().__init__()
        self.pos = pos
        self.name = name  # Store the tile type name
        self.image = pygame.image.load(f'Assets\\Tileset\\{name}.png')
        self.rec = self.image.get_rect(topleft = pos)
        
        # Define hazard types - fire and water are NOT solid
        self.is_fire = name in ['lava', 'lavadown']
        self.is_water = name in ['water', 'waterdown']
        self.is_solid = not (self.is_fire or self.is_water)  # Only non-hazard tiles are solid

    def update(self, xshift):
        self.rec.x += xshift

    def draw(self, surf): 
    
        surf.blit(self.image, self.rec)
        #pygame.draw.rect(surf, (0, 0, 0), self.rec)