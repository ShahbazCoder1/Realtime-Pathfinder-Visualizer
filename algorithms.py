import pygame
import time
from queue import PriorityQueue
from constants import ALGORITHM_DELAY  # Fixed: Import the constant

class Algorithm:
    @staticmethod
    def reconstruct_path(came_from, current, draw):
   
        path_length = 0
        while current in came_from:
            current = came_from[current]
            if not current.is_start():
                current.make_path()
            path_length += 1
            draw()
        return path_length

class AStar(Algorithm):
    @staticmethod
    def heuristic(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)
    
    @staticmethod
    def run(grid, start, end, draw):
        start_time = time.time()
        count = 0
        nodes_explored = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
    
        g_score = {node: float("inf") for row in grid.grid for node in row}
        g_score[start] = 0
        
        f_score = {node: float("inf") for row in grid.grid for node in row}
        f_score[start] = AStar.heuristic(start.get_position(), end.get_position())
        
        open_set_hash = {start}
        
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()[2]
            open_set_hash.remove(current)
            nodes_explored += 1
            
            if current == end:
                path_length = AStar.reconstruct_path(came_from, end, draw)
                end.make_end()
                start.make_start()
                elapsed_time = (time.time() - start_time) * 1000
                
                return {
                    "nodes_explored": nodes_explored,
                    "path_length": path_length,
                    "time_ms": round(elapsed_time, 2)
                }
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + AStar.heuristic(
                        neighbor.get_position(), end.get_position()
                    )
                    
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            draw()
            pygame.time.delay(ALGORITHM_DELAY)
            
            if current != start:
                current.make_closed()
        
        elapsed_time = (time.time() - start_time) * 1000
        return {
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "time_ms": round(elapsed_time, 2)
        }

class Dijkstra(Algorithm):
    @staticmethod
    def run(grid, start, end, draw):
        start_time = time.time()
        count = 0
        nodes_explored = 0
    
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        
        distance = {node: float("inf") for row in grid.grid for node in row}
        distance[start] = 0
        
        open_set_hash = {start}
        
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()[2]
            open_set_hash.remove(current)
            nodes_explored += 1
            
            if current == end:
                path_length = Dijkstra.reconstruct_path(came_from, end, draw)
                end.make_end()
                start.make_start()
                elapsed_time = (time.time() - start_time) * 1000
                
                return {
                    "nodes_explored": nodes_explored,
                    "path_length": path_length,
                    "time_ms": round(elapsed_time, 2)
                }
            
            for neighbor in current.neighbors:
                temp_distance = distance[current] + 1
                
                if temp_distance < distance[neighbor]:
                    came_from[neighbor] = current
                    distance[neighbor] = temp_distance
                    
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((distance[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            draw()
            pygame.time.delay(ALGORITHM_DELAY)
            
            if current != start:
                current.make_closed()
        
        elapsed_time = (time.time() - start_time) * 1000
        return {
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "time_ms": round(elapsed_time, 2)
        }
