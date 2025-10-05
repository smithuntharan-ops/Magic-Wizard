import pygame

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_paused = False
        
        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)
        
        # Button dimensions
        self.button_width = 300
        self.button_height = 60
        self.button_spacing = 20
        
        # Calculate positions
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Buttons
        self.buttons = {
            'resume': pygame.Rect(center_x - self.button_width // 2, 
                                 center_y - 40, 
                                 self.button_width, 
                                 self.button_height),
            'restart': pygame.Rect(center_x - self.button_width // 2, 
                                  center_y + 40, 
                                  self.button_width, 
                                  self.button_height),
            'quit': pygame.Rect(center_x - self.button_width // 2, 
                               center_y + 120, 
                               self.button_width, 
                               self.button_height)
        }
        
        self.selected_button = None
        
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
                return 'toggle'
        
        if not self.is_paused:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.buttons['resume'].collidepoint(mouse_pos):
                self.is_paused = False
                return 'resume'
            elif self.buttons['restart'].collidepoint(mouse_pos):
                return 'restart'
            elif self.buttons['quit'].collidepoint(mouse_pos):
                return 'quit'
                
        return None
    
    def update(self):
        if not self.is_paused:
            return
            
        mouse_pos = pygame.mouse.get_pos()
        self.selected_button = None
        
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                self.selected_button = button_name
                break
    
    def draw(self, surf):
        if not self.is_paused:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surf.blit(overlay, (0, 0))
        
        # Title
        title_text = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        surf.blit(title_text, title_rect)
        
        # Buttons
        button_labels = {
            'resume': 'Resume',
            'restart': 'Restart',
            'quit': 'Quit Game'
        }
        
        for button_name, button_rect in self.buttons.items():
            # Button color based on hover
            if self.selected_button == button_name:
                button_color = (80, 120, 200)
                text_color = (255, 255, 255)
                border_width = 4
            else:
                button_color = (50, 50, 80)
                text_color = (200, 200, 200)
                border_width = 2
            
            # Draw button
            pygame.draw.rect(surf, button_color, button_rect, border_radius=10)
            pygame.draw.rect(surf, (255, 255, 255), button_rect, border_width, border_radius=10)
            
            # Draw text
            button_text = self.button_font.render(button_labels[button_name], True, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            surf.blit(button_text, text_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 30)
        instruction_text = instruction_font.render("Press ESC to resume", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        surf.blit(instruction_text, instruction_rect)