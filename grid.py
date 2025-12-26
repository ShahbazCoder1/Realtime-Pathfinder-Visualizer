import pygame
from node import Node
from constants import *

class Grid:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = []
        self.gap = width // rows
        self._create_grid()
        self._neighbor_cache = {}
    
    def _create_grid(self):
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                node = Node(i, j, self.gap, self.rows)
                self.grid[i].append(node)
    
    def get_node(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.rows:
            return self.grid[row][col]
        return None
    
    def get_clicked_position(self, pos):
        x, y = pos
        row = y // self.gap
        col = x // self.gap
        return row, col
    
    def update_neighbors(self):
        self._neighbor_cache.clear()
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)
                self._neighbor_cache[(node.row, node.col)] = node.neighbors
    
    def draw(self, screen):
        for row in self.grid:
            for node in row:
                node.draw(screen)
        
        self._draw_grid_lines(screen)
    
    def _draw_grid_lines(self, screen):
        for i in range(self.rows + 1):
            pygame.draw.line(screen, COLOR_GRID_LINE, 
                           (0, i * self.gap), (self.width, i * self.gap), 1)
            pygame.draw.line(screen, COLOR_GRID_LINE, 
                           (i * self.gap, 0), (i * self.gap, self.width), 1)
