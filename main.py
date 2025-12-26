import pygame
import sys
from grid import Grid
from algorithms import Dijkstra, AStar
from ui import Button, StatusBar
from constants import *

class PathfinderVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Realtime Pathfinder Visualizer")
        self.clock = pygame.time.Clock()
        self.grid = Grid(ROWS, GRID_WIDTH)
        self.start_node = None
        self.end_node = None
        self.algorithm_name = None
        self.running_algorithm = False
        self.algorithm_stats = {"nodes_explored": 0, "path_length": 0, "time_ms": 0}
        
        self._setup_ui()
        
    def _setup_ui(self):
        button_y = GRID_WIDTH + 15 
        button_width = 140  
        button_height = 38
        spacing = 15  
        
        self.buttons = [
            Button(15, button_y, button_width, button_height, "A* Search", COLOR_BUTTON_PRIMARY),
            Button(15 + button_width + spacing, button_y, button_width, button_height, "Dijkstra", COLOR_BUTTON_SECONDARY),
            Button(15 + 2 * (button_width + spacing), button_y, button_width, button_height, "Clear Grid", COLOR_BUTTON_DANGER),
            Button(15 + 3 * (button_width + spacing), button_y, button_width, button_height, "Reset Path", COLOR_BUTTON_WARNING)
        ]
        
        self.status_bar = StatusBar(15, button_y + button_height + 12, GRID_WIDTH - 30, 75)  # Adjusted height
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
               
                if self.buttons[0].is_clicked(mouse_pos) and not self.running_algorithm:
                    self._run_algorithm('astar')
                elif self.buttons[1].is_clicked(mouse_pos) and not self.running_algorithm:
                    self._run_algorithm('dijkstra')
                elif self.buttons[2].is_clicked(mouse_pos) and not self.running_algorithm:
                    self._clear_grid()
                elif self.buttons[3].is_clicked(mouse_pos) and not self.running_algorithm:
                    self._reset_path()
        
            if pygame.mouse.get_pressed()[0] and not self.running_algorithm:
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_WIDTH:  
                    row, col = self.grid.get_clicked_position(pos)
                    node = self.grid.get_node(row, col)
                    
                    if node:
                        if not self.start_node and node != self.end_node:
                            self.start_node = node
                            node.make_start()
                        elif not self.end_node and node != self.start_node:
                            self.end_node = node
                            node.make_end()
                        elif node != self.start_node and node != self.end_node:
                            node.make_barrier()
            
            elif pygame.mouse.get_pressed()[2] and not self.running_algorithm:
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_WIDTH:
                    row, col = self.grid.get_clicked_position(pos)
                    node = self.grid.get_node(row, col)
                    
                    if node:
                        node.reset()
                        if node == self.start_node:
                            self.start_node = None
                        elif node == self.end_node:
                            self.end_node = None
            
            if event.type == pygame.KEYDOWN and not self.running_algorithm:
                if event.key == pygame.K_SPACE:
                    self._run_algorithm('astar')
                elif event.key == pygame.K_d:
                    self._run_algorithm('dijkstra')
                elif event.key == pygame.K_c:
                    self._clear_grid()
                elif event.key == pygame.K_r:
                    self._reset_path()
        
        return True
    
    def _run_algorithm(self, algorithm_type):
        if not self.start_node or not self.end_node:
            return
        
        self.running_algorithm = True
        self.algorithm_name = algorithm_type
        self._reset_path()
        self.grid.update_neighbors()
        
        if algorithm_type == 'astar':
            result = AStar.run(self.grid, self.start_node, self.end_node, 
                             lambda: self.draw())
        else:
            result = Dijkstra.run(self.grid, self.start_node, self.end_node, 
                                lambda: self.draw())
        
        self.algorithm_stats = result
        self.running_algorithm = False
    
    def _clear_grid(self):
        self.start_node = None
        self.end_node = None
        self.algorithm_name = None
        self.algorithm_stats = {"nodes_explored": 0, "path_length": 0, "time_ms": 0}
        self.grid = Grid(ROWS, GRID_WIDTH)
    
    def _reset_path(self):
        for row in self.grid.grid:
            for node in row:
                if node.is_closed() or node.is_open() or node.color == COLOR_PATH:
                    node.reset()
                    if node == self.start_node:
                        node.make_start()
                    elif node == self.end_node:
                        node.make_end()
        self.algorithm_stats = {"nodes_explored": 0, "path_length": 0, "time_ms": 0}
    
    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        

        self.grid.draw(self.screen)
        
        for button in self.buttons:
            button.draw(self.screen)

        status_text = self._get_status_text()
        self.status_bar.draw(self.screen, status_text, self.algorithm_stats)
        
        pygame.display.update()
    
    def _get_status_text(self):
        if self.running_algorithm:
            return f"Running {self.algorithm_name.upper()}..."
        elif not self.start_node:
            return "Click to place START node (Orange)"
        elif not self.end_node:
            return "Click to place END node (Cyan)"
        elif self.algorithm_name and self.algorithm_stats["path_length"] > 0:
            return f"{self.algorithm_name.upper()} Complete!"
        else:
            return "Draw barriers, then run algorithm"
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            self.clock.tick(60)
            running = self.handle_events()
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PathfinderVisualizer()
    app.run()
