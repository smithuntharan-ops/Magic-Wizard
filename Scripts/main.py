import pygame
import os  
from level import Level
from pause_menu import PauseMenu

pygame.init()
SCREEN_RES = (960, 640)
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption('Magic Wizard')
clock = pygame.time.Clock()

pause_menu = PauseMenu(SCREEN_RES[0], SCREEN_RES[1])

def load_level(level_num):
    level = Level()
    level.load_level(level_num)
    return level

def draw_game_over(surf):
    overlay = pygame.Surface((SCREEN_RES[0], SCREEN_RES[1]))
    overlay.set_alpha(200)
    overlay.fill((20, 0, 0))
    surf.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font(None, 100)
    
    center_x = SCREEN_RES[0] // 2
    center_y = SCREEN_RES[1] // 2 - 50
    
    shadow_text = title_font.render("GAME OVER", True, (100, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(center_x + 4, center_y + 4))
    surf.blit(shadow_text, shadow_rect)
    
    game_over_text = title_font.render("GAME OVER", True, (255, 50, 50))
    game_over_rect = game_over_text.get_rect(center=(center_x, center_y))
    surf.blit(game_over_text, game_over_rect)
    
    instruction_font = pygame.font.Font(None, 40)
    instruction_text = instruction_font.render("Press ESC for menu", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 100))
    surf.blit(instruction_text, instruction_rect)

def draw_level_complete(surf, level_num):
    overlay = pygame.Surface((SCREEN_RES[0], SCREEN_RES[1]))
    overlay.set_alpha(200)
    overlay.fill((0, 20, 0))
    surf.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font(None, 100)
    
    center_x = SCREEN_RES[0] // 2
    center_y = SCREEN_RES[1] // 2 - 50
    
    shadow_text = title_font.render("LEVEL COMPLETE!", True, (0, 100, 0))
    shadow_rect = shadow_text.get_rect(center=(center_x + 4, center_y + 4))
    surf.blit(shadow_text, shadow_rect)
    
    level_complete_text = title_font.render("LEVEL COMPLETE!", True, (50, 255, 50))
    level_complete_rect = level_complete_text.get_rect(center=(center_x, center_y))
    surf.blit(level_complete_text, level_complete_rect)

    instruction_font = pygame.font.Font(None, 40)
    instruction_text = instruction_font.render(f"Press ENTER to proceed to Level {level_num + 1}", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 100))
    surf.blit(instruction_text, instruction_rect)

def draw_game_complete(surf):  
    overlay = pygame.Surface((SCREEN_RES[0], SCREEN_RES[1]))
    overlay.set_alpha(200)
    overlay.fill((20, 20, 0)) 
    surf.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font(None, 100)
    
    center_x = SCREEN_RES[0] // 2
    center_y = SCREEN_RES[1] // 2 - 50
    
    shadow_text = title_font.render("GAME COMPLETE!", True, (100, 100, 0))
    shadow_rect = shadow_text.get_rect(center=(center_x + 4, center_y + 4))
    surf.blit(shadow_text, shadow_rect)
    
    game_complete_text = title_font.render("GAME COMPLETE!", True, (255, 215, 0)) 
    game_complete_rect = game_complete_text.get_rect(center=(center_x, center_y))
    surf.blit(game_complete_text, game_complete_rect)
    
    instruction_font = pygame.font.Font(None, 40)
    instruction_text = instruction_font.render("Press R to restart or ESC for menu", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 100))
    surf.blit(instruction_text, instruction_rect)


current_level = 1
level_1 = load_level(current_level)
game_over = False
level_complete = False
game_won = False  

run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        menu_action = pause_menu.handle_event(event)
        
        if menu_action == 'restart':
            level_1 = load_level(current_level)
            pause_menu.is_paused = False
            game_over = False
            level_complete = False
            game_won = False  
        elif menu_action == 'quit':
            run = False
        
        # Handle input for level complete screen
        if level_complete and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                next_level_file = f'Assets\\Mapdata\\Level{current_level + 1}.csv'
                if os.path.exists(next_level_file): 
                    current_level += 1
                    level_1 = load_level(current_level)
                    level_complete = False
                    pause_menu.is_paused = False
                else:
                   
                    game_won = True
                    level_complete = False
                    pause_menu.is_paused = True
        
        
        if game_won and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  
                current_level = 1
                level_1 = load_level(current_level)
                game_won = False
                pause_menu.is_paused = False
                game_over = False
                level_complete = False
            elif event.key == pygame.K_ESCAPE: 
                pause_menu.is_paused = True  

    screen.fill((0, 0, 0))
    
    if not pause_menu.is_paused and not level_complete and not game_won:
        result = level_1.start_level(screen)
        
        if result == 'game_over':
            game_over = True
            pause_menu.is_paused = True
        elif result == 'level_complete':
            level_complete = True
            pause_menu.is_paused = True
    
   
    if game_over:
        draw_game_over(screen)
    elif level_complete:
        draw_level_complete(screen, current_level)
    elif game_won:  
        draw_game_complete(screen)
    
    pause_menu.update()
    pause_menu.draw(screen)
    
    pygame.display.update()

pygame.quit()