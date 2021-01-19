import pygame as pg
import random

from a_star.board import Board
from a_star.constants import WIDTH, HEIGHT, CUBE_SIZE, ROWS, COLS
from a_star.algorithm import algorithm

def main():

    path_is_generated = False
    start = None
    end = None
    started = False

    clock = pg.time.Clock() #define fps
    
    board = Board()
    board.draw(SCREEN)

    while not path_is_generated:
        clock.tick(30)
        

        for event in pg.event.get():

            if event.type == pg.QUIT:
                path_is_generated = True

            if started:
                continue

            if pg.mouse.get_pressed()[0]: #left mouse button
                position = pg.mouse.get_pos()
                row, col = mouse_position_to_board_position(position)
                node = board.array[row][col]

                if not start and not node.is_end():
                    board.make_start(row, col)
                    start = board.array[row][col]

                elif not end and not node.is_start():
                    board.make_end(row, col)
                    end = board.array[row][col]

                elif start is not None and end is not None and not node.is_end() and not node.is_start():
                    board.make_barrier(row, col)

            elif pg.mouse.get_pressed()[2]:  
                position = pg.mouse.get_pos()
                row, col = mouse_position_to_board_position(position)
                node = board.array[row][col]
                if node.is_start():
                    start = None
                if node.is_end():
                    end = None
                node.reset()


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    for row in board.array:
                        for node in row:
                            board.get_neighbours(node)
                    draw = lambda: board.draw(SCREEN)
                    algorithm(draw, board, start, end)

                if event.key == pg.K_r:
                    board.reset(SCREEN)
                    start = None
                    end = None


        board.draw(SCREEN)


    pg.quit()


def main_1():
    path_is_generated = False
    board = Board()
    board.array[0][0].make_start()
    start = board.array[0][0]
    board.array[ROWS-1][COLS-1].make_end()
    end = board.array[ROWS-1][COLS-1]

    for row in range(ROWS):
        for col in range(COLS):
            if row%2 == 0 and board.array[row][col] != start and board.array[row][col] != end:
                choice = random.choice([True, False])
                if choice:
                    board.array[row][col].make_barrier()

    started = False

    clock = pg.time.Clock() #define fps
    

    board.draw(SCREEN)

    while not path_is_generated:
        clock.tick(30)
        

        for event in pg.event.get():

            if event.type == pg.QUIT:
                path_is_generated = True

            if started:
                continue

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    for row in board.array:
                        for node in row:
                            board.get_neighbours(node)
                    draw = lambda: board.draw(SCREEN)
                    algorithm(draw, board, start, end)

                if event.key == pg.K_r:
                    board.reset(SCREEN)
                    start = None
                    end = None


        board.draw(SCREEN)


    pg.quit()

mode = input('Draw barriers or pseudo random barriers? (d/r)')

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('A* Path finding')

def mouse_position_to_board_position(mouse_position):
    array_row = mouse_position[0] // CUBE_SIZE
    array_col = mouse_position[1] // CUBE_SIZE
    return array_row, array_col

if mode == 'd':
    main()
else:
    main_1()
