import pygame as pg
from a_star.board import Board
from a_star.algorithm import algorithm
from PIL import Image
import numpy as np
#print('Pillow Version:', PIL.__version__)

############################################################
#ENTER THE PATH OF THE IMAGE
PATH = './Images/maze2.jpg'
############################################################


def img_to_array(PATH):
    '''
    turn it into a numpy array
    '''
    #import image
    image = Image.open(PATH)
    #convert to numpy array
    image = np.asarray(image)
    return image

def rgb2gray(rgb):
    '''
    compress the RGB channels into a single grayscale channel
    '''
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def resize(array, scaling_factor):
    '''
    can be used to resize an array
    '''
    resampled_img = np.zeros((array.shape[0]//scaling_factor, array.shape[1]//scaling_factor))
    for i in range(resampled_img.shape[0]):
        for j in range(resampled_img.shape[1]):
            resampled_img[i,j] = np.mean(array[i*scaling_factor:(i+1)*scaling_factor,j*scaling_factor:(j+1)*scaling_factor])
    return resampled_img

def array_to_bw(image):
    '''
    turns the grayscale image into a BW image
    '''
    #convert to grayscale
    image_gray = image
    #convert to b/w
    image_bw = np.zeros((image_gray.shape[0], image_gray.shape[1]))
    for i in range(image_gray.shape[0]):
        for j in range(image_gray.shape[1]):
            if image_gray[i, j] >= 200:
                image_bw[i, j] = 255
            else:
                image_bw[i, j] = 0
    return image_bw

def mouse_position_to_board_position(mouse_position):
    '''
    determines the mouse position
    '''
    array_row = mouse_position[0] // CUBE_SIZE
    array_col = mouse_position[1] // CUBE_SIZE
    return array_row, array_col

def main(ROWS, COLS, CUBE_SIZE):

    path_is_generated = False
    board = Board(ROWS, COLS, CUBE_SIZE)
    for i in range(ROWS):
        for j in range(COLS):
            if img_array[i][j] == 0:
                board.array[i][j].make_barrier()

    start = None
    end = None
    started = False

    clock = pg.time.Clock()
    
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

#preprocessing
img_array = img_to_array(PATH)
img_array = rgb2gray(img_array)
img_array = resize(img_array, 4) #the factor can be changed according to your PCs power
img_array = array_to_bw(img_array)

#resizing to screen
ORIGINAL_HEIGHT = Image.open(PATH).size[0]
ORIGINAL_WIDTH = Image.open(PATH).size[1]
if ORIGINAL_HEIGHT > ORIGINAL_WIDTH:
    HEIGHT = 720
    WIDTH = ORIGINAL_WIDTH*720//ORIGINAL_HEIGHT
else:
    WIDTH = 1080
    HEIGHT = ORIGINAL_HEIGHT*1000//ORIGINAL_WIDTH

#defining the grid constants
ROWS = img_array.shape[0]
COLS = img_array.shape[1]
CUBE_SIZE = HEIGHT//COLS
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('A* Path finding')


main(ROWS, COLS, CUBE_SIZE)