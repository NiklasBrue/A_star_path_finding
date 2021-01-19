import pygame as pg
from queue import PriorityQueue


def heuristic_function(P1, P2):
    P1_x, P1_y = P1
    P2_x, P2_y = P2
    return abs(P1_x-P2_x) + abs(P1_y-P2_y)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm(draw, board, start, end):
	grid = board.array
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = heuristic_function(start.get_array_position(), end.get_array_position())

	open_set_hash = {start}
	
	while not open_set.empty(): 
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in board.get_neighbours(current):
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic_function(neighbor.get_array_position(), end.get_array_position())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False