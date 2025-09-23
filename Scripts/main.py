import pygame
from level import Level

pygame.init()
SCREEN_RES = (960, 640)
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption('Magic Wizard')
clock = pygame.time.Clock()
current_level = 1

level_1 = Level()
level_1.load_level(1)

run = True
while run:

    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    level_1.start_level(screen)
    pygame.display.update()
pygame.quit()