import pygame as pg
from .constants import BLACK, GREEN, WHITE, BLACK,\
                 RED, CYAN, MAGENTA, BLUE, CUBE_SIZE

class Node():

    def __init__(self, row, col, CUBE_SIZE):
        self.row = row
        self.col = col
        self.CUBE_SIZE = CUBE_SIZE
        self.x = row * CUBE_SIZE
        self.y = col * CUBE_SIZE
        self.color = WHITE

    def __repr__(self):
        return 'Node: row={}, col={}, color={}'.format(self.row, self.col, self.color)

    def get_array_position(self):
        return self.row, self.col
    
    def get_board_position(self):
        return self.x, self.y

    def is__checked(self):
        return self.color == RED

    def is_not_checked(self):
        return self.color == GREEN

    def is_barrier(self):
        if self.color == BLACK:
            return True

    def is_start(self):
        if self.color == MAGENTA:
            return True

    def is_end(self):
        if self.color == CYAN:
            return True

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = MAGENTA

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = CYAN

    def make_path(self):
        self.color = BLUE

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.CUBE_SIZE, self.CUBE_SIZE))

    def __lt__(self, other):
        return False