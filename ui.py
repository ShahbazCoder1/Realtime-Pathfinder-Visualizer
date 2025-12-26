import pygame
from constants import *

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, screen):
        color = COLOR_BUTTON_HOVER if self.hover else self.color
        
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=10)
     
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, COLOR_BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

class StatusBar:
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font_large = pygame.font.Font(None, 26) 
        self.font_small = pygame.font.Font(None, 20)
    
    def draw(self, screen, status_text, stats):
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 20), shadow_rect, border_radius=10)
        
        pygame.draw.rect(screen, COLOR_PANEL, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_GRID_LINE, self.rect, 2, border_radius=10)
    
        status_surf = self.font_large.render(status_text, True, COLOR_TEXT)
        screen.blit(status_surf, (self.rect.x + 15, self.rect.y + 12))
    
        legend_y = self.rect.y + 42 
        self._draw_legend_item(screen, self.rect.x + 15, legend_y, COLOR_START, "Start (S)")
        self._draw_legend_item(screen, self.rect.x + 130, legend_y, COLOR_END, "End (E)")
        self._draw_legend_item(screen, self.rect.x + 240, legend_y, COLOR_BARRIER, "Barrier")
        self._draw_legend_item(screen, self.rect.x + 350, legend_y, COLOR_PATH, "Path")
      
        if stats["nodes_explored"] > 0:
            stats_text = f"Nodes: {stats['nodes_explored']} | Path: {stats['path_length']} | {stats['time_ms']}ms"
            stats_surf = self.font_small.render(stats_text, True, COLOR_TEXT)
            screen.blit(stats_surf, (self.rect.x + 460, legend_y + 1))
    
    def _draw_legend_item(self, screen, x, y, color, text):
        pygame.draw.rect(screen, color, (x, y, 18, 18))
        pygame.draw.rect(screen, BLACK, (x, y, 18, 18), 1)
 
        text_surf = self.font_small.render(text, True, COLOR_TEXT)
        screen.blit(text_surf, (x + 24, y - 1))
