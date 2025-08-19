import pygame
from config import (GRID_SIZE, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, 
                    GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y, NODE_COLORS, NODE_WEIGHTS)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = GRID_TOP_LEFT_X + col * CELL_SIZE
        self.y = GRID_TOP_LEFT_Y + row * CELL_SIZE
        self.node_type = "AIR"
        self.color = NODE_COLORS["DEFAULT"]
        self.weight = NODE_WEIGHTS["AIR"]
        self.is_wall = False
        self.neighbors = []
        self.reset_path_vars()

    def reset_path_vars(self):
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.came_from = None
        self.is_open = False
        self.is_closed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def set_type(self, node_type):
        self.node_type = node_type
        self.color = NODE_COLORS[node_type]
        self.weight = NODE_WEIGHTS.get(node_type, 1)
        self.is_wall = (node_type == "WALL")

class Grid:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Grid, cls).__new__(cls)
            cls._instance.init_grid()
        return cls._instance

    def init_grid(self):
        self.grid = [[Node(row, col) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        self.start_node = None
        self.end_node = None
        self.update_all_neighbors()

    def update_all_neighbors(self):
        for row in self.grid:
            for node in row:
                node.neighbors = self._get_neighbors(node)

    def _get_neighbors(self, node):
        neighbors = []
        if node.row > 0: neighbors.append(self.grid[node.row - 1][node.col])
        if node.row < GRID_SIZE - 1: neighbors.append(self.grid[node.row + 1][node.col])
        if node.col > 0: neighbors.append(self.grid[node.row][node.col - 1])
        if node.col < GRID_SIZE - 1: neighbors.append(self.grid[node.row][node.col + 1])
        return neighbors

    def draw(self, screen):
        for row in self.grid:
            for node in row:
                node.draw(screen)
        self._draw_grid_lines(screen)

    def _draw_grid_lines(self, screen):
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, (0,0,0), 
                             (GRID_TOP_LEFT_X + i * CELL_SIZE, GRID_TOP_LEFT_Y), 
                             (GRID_TOP_LEFT_X + i * CELL_SIZE, GRID_TOP_LEFT_Y + GRID_HEIGHT))
            pygame.draw.line(screen, (0,0,0), 
                             (GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y + i * CELL_SIZE), 
                             (GRID_TOP_LEFT_X + GRID_WIDTH, GRID_TOP_LEFT_Y + i * CELL_SIZE))

    def get_node_from_pos(self, pos):
        x, y = pos
        if not (GRID_TOP_LEFT_X <= x < GRID_TOP_LEFT_X + GRID_WIDTH and 
                GRID_TOP_LEFT_Y <= y < GRID_TOP_LEFT_Y + GRID_HEIGHT):
            return None
        
        col = (x - GRID_TOP_LEFT_X) // CELL_SIZE
        row = (y - GRID_TOP_LEFT_Y) // CELL_SIZE
        return self.grid[row][col]

    def set_node_type(self, node, brush_type):
        if node is None:
            return

        if brush_type == "START":
            if self.start_node:
                self.start_node.set_type("AIR")
            self.start_node = node
            node.set_type("START")
        elif brush_type == "END":
            if self.end_node:
                self.end_node.set_type("AIR")
            self.end_node = node
            node.set_type("END")
        else:
            if node == self.start_node:
                self.start_node = None
            elif node == self.end_node:
                self.end_node = None
            node.set_type(brush_type)

    def reset_path(self):
        for row in self.grid:
            for node in row:
                node.reset_path_vars()
                if node.node_type not in ["WALL", "START", "END", "DIRT", "MUD", "TAR"]:
                    node.set_type("AIR")
                else:
                    node.set_type(node.node_type)

    def full_reset(self):
        self.start_node = None
        self.end_node = None
        for row in self.grid:
            for node in row:
                node.set_type("AIR")
                node.reset_path_vars()

grid_instance = Grid()