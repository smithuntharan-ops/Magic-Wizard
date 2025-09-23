import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, name):

        # Tiles
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(f'Assets\\Tileset\\{name}.png')
        self.rec = self.image.get_rect(topleft = pos)

    def update(self, xshift):
        self.rec.x += xshift

    def draw(self, surf): 
    
        surf.blit(self.image, self.rec)
        #pygame.draw.rect(surf, (0, 0, 0), self.rec)