import pygame
from level import Level
from pause_menu import PauseMenu

pygame.init()
SCREEN_RES = (960, 640)
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption('Magic Wizard')
clock = pygame.time.Clock()

# Create pause menu
pause_menu = PauseMenu(SCREEN_RES[0], SCREEN_RES[1])

def load_level(level_num):
    level = Level()
    level.load_level(level_num)
    return level

def draw_game_over(surf):
    # Semi-transparent red overlay
    overlay = pygame.Surface((SCREEN_RES[0], SCREEN_RES[1]))
    overlay.set_alpha(200)
    overlay.fill((20, 0, 0))
    surf.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font(None, 100)
    
    center_x = SCREEN_RES[0] // 2
    center_y = SCREEN_RES[1] // 2 - 50
    
    # Shadow (offset by 4 pixels down and right)
    shadow_text = title_font.render("GAME OVER", True, (100, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(center_x + 4, center_y + 4))
    surf.blit(shadow_text, shadow_rect)
    
    # Main text
    game_over_text = title_font.render("GAME OVER", True, (255, 50, 50))
    game_over_rect = game_over_text.get_rect(center=(center_x, center_y))
    surf.blit(game_over_text, game_over_rect)
    
    # Instruction message
    instruction_font = pygame.font.Font(None, 40)
    instruction_text = instruction_font.render("Press ESC for menu", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 100))
    surf.blit(instruction_text, instruction_rect)

current_level = 1
level_1 = load_level(current_level)
game_over = False

run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        menu_action = pause_menu.handle_event(event)
        
        if menu_action == 'restart':
            # Restart the level
            level_1 = load_level(current_level)
            pause_menu.is_paused = False
            game_over = False
        elif menu_action == 'quit':
            run = False
    
    screen.fill((0, 0, 0))
    
    if not pause_menu.is_paused:
        result = level_1.start_level(screen)
        
        # Check if game over
        if result == 'game_over':
            game_over = True
            pause_menu.is_paused = True
    
   
    if game_over:
        draw_game_over(screen)
    
    pause_menu.update()
    pause_menu.draw(screen)
    
    pygame.display.update()

pygame.quit()