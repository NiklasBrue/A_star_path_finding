import pygame as pg
import numpy as np

from .node import Node
from .constants import BLACK, WHITE

class Board():

    def __init__(self, ROWS, COLS, CUBE_SIZE):
        self.ROWS = ROWS
        self.COLS = COLS
        self.CUBE_SIZE = CUBE_SIZE
        self.HEIGHT = self.CUBE_SIZE*self.COLS
        self.WIDTH = self.CUBE_SIZE*self.ROWS
        self.array = np.empty((self.ROWS, self.COLS), dtype=Node)
        self.make_board()

    def __repr__(self):
        return 'Board: {}'.format(self.array)
    
    def make_board(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                node = Node(row, col, self.CUBE_SIZE)
                self.array[row][col] = node

    def draw_grid_lines(self, screen):
        for row in range(self.ROWS+1):
            pg.draw.line(screen, BLACK, (row*self.CUBE_SIZE, 0), (row*self.CUBE_SIZE, self.HEIGHT))
            for col in range(self.COLS+1):
                pg.draw.line(screen, BLACK, (0, col*self.CUBE_SIZE), (self.WIDTH, col*self.CUBE_SIZE))

    def draw(self, screen):
        screen.fill(WHITE)
        for row in self.array:
            for node in row:
                node.draw(screen)
        self.draw_grid_lines(screen)
        pg.display.update()

    def reset(self, screen):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                node = Node(row, col, self.CUBE_SIZE)
                node.reset()
                self.array[row][col] = node

    def make_start(self, row, col):
        self.array[row][col].make_start()

    def make_end(self, row, col):
        self.array[row][col].make_end()

    def make_barrier(self, row, col):
        self.array[row][col].make_barrier()

    def get_neighbours(self, node):
        neighbours = []
        if node.row > 0 and not self.array[node.row-1][node.col].is_barrier(): #SQR above
            neighbours.append(self.array[node.row-1][node.col])
        if node.row < self.ROWS-1 and not self.array[node.row+1][node.col].is_barrier(): #SQR down
            neighbours.append(self.array[node.row+1][node.col])
        if node.col > 0 and not self.array[node.row][node.col-1].is_barrier(): #SQR left
            neighbours.append(self.array[node.row][node.col-1])
        if node.col < self.COLS-1 and not self.array[node.row][node.col+1].is_barrier(): #SQR right
            neighbours.append(self.array[node.row][node.col+1])
        return neighbours