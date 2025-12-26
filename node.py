import pygame
from constants import *

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col

        self.x = col * width
        self.y = row * width
        self.color = COLOR_DEFAULT
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_position(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == COLOR_CLOSED
    
    def is_open(self):
        return self.color == COLOR_OPEN
    
    def is_barrier(self):
        return self.color == COLOR_BARRIER
    
    def is_start(self):
        return self.color == COLOR_START
    
    def is_end(self):
        return self.color == COLOR_END
    
    def reset(self):
        self.color = COLOR_DEFAULT
    
    def make_start(self):
        self.color = COLOR_START
    
    def make_closed(self):
        self.color = COLOR_CLOSED
    
    def make_open(self):
        self.color = COLOR_OPEN
    
    def make_barrier(self):
        self.color = COLOR_BARRIER
    
    def make_end(self):
        self.color = COLOR_END
    
    def make_path(self):
        self.color = COLOR_PATH
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))
        
        if self.is_start():
            center_x = self.x + self.width // 2
            center_y = self.y + self.width // 2
            radius = min(self.width // 3, 8)
            pygame.draw.circle(screen, WHITE, (center_x, center_y), radius)
            font = pygame.font.Font(None, max(int(self.width * 0.7), 12))
            text = font.render("S", True, BLACK)
            text_rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, text_rect)
            
        elif self.is_end():
            center_x = self.x + self.width // 2
            center_y = self.y + self.width // 2
            radius = min(self.width // 3, 8) 
            pygame.draw.circle(screen, BLACK, (center_x, center_y), radius)
            font = pygame.font.Font(None, max(int(self.width * 0.7), 12))
            text = font.render("E", True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, text_rect)
        if self.color != COLOR_DEFAULT and self.color != COLOR_GRID_LINE:
            border_color = tuple(max(0, c - 40) for c in self.color)
            pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.width), 1)
    
    def update_neighbors(self, grid):
        self.neighbors = []
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False
