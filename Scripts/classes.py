import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, name):
        # Tiles
        super().__init__()
        self.pos = pos
        self.name = name
        
        # Try to load image, or create fallback
        try:
            self.image = pygame.image.load(f'Assets\\Tileset\\{name}.png')
        except:
            # Create fallback image for missing tiles
            self.image = pygame.Surface((32, 32))
            if name == 'yyydoor':
                # Green door with highlight
                self.image.fill((50, 150, 50))
                pygame.draw.rect(self.image, (100, 255, 100), (4, 4, 24, 24))
                pygame.draw.rect(self.image, (255, 255, 0), (12, 12, 8, 8))  # Yellow center
            else:
                # Pink placeholder for other missing tiles
                self.image.fill((255, 0, 255))
        
        self.rec = self.image.get_rect(topleft = pos)
        
        # Define hazard types
        self.is_fire = name in ['lava', 'lavadown']
        self.is_water = name in ['water', 'waterdown']
        self.is_solid = not (self.is_fire or self.is_water) and name != 'yyydoor'

    def update(self, xshift):
        self.rec.x += xshift

    def draw(self, surf): 
        surf.blit(self.image, self.rec)