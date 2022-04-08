import pygame
import numpy as np
from constants import *
 
pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("A* Visualization")

class Node:

	def __init__(self,row,col,width,height,total_rows):
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.x = row * width
		self.y = col * height
		self.total_rows = total_rows

		self.color = WHITE
		self.neighbours = []
		
	def is_closed(self):
		return self.color == BLUE

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == GREEN

	def is_goal(self):
		return self.color == YELLOW

	def reset(self):
		self.color = WHITE

	def closed(self):
		self.color = BLUE

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = GREEN

	def make_end(self):
		self.color = YELLOW

	def draw_path(self):
		self.color = PINK

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

def h(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return abs(x1-x2)+abs(y1-y2)

def make_grid(rows,width): #width == height
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i,j,gap,gap,ROWS)
			grid[i].append(node)
	return grid

def draw_grid(win,rows,width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win,GREY, (0,i*gap),(width, i*gap))
		for j in range(rows):
			pygame.draw.line(win,GREY, (j*gap,0),(j*gap,width))

def draw(win,grid,rows,width):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win,rows,width)
	pygame.display.update()

def position(p,rows,width):
	gap = width//rows
	x,y = p
	row = y // gap
	col = x // gap
	return row,col

grid = make_grid(ROWS,WIDTH)
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if pygame.mouse.get_pressed()[0]:
			point = pygame.mouse.get_pos()
			row,col = position(point,ROWS,WIDTH)
			node = grid[col][row]
			"""if node.is_barrier():
				node.reset()
			else:"""
			node.make_barrier()
		if pygame.mouse.get_pressed()[1]:
			point = pygame.mouse.get_pos()
			row, col = position(point, ROWS, WIDTH)
			node = grid[col][row]
			node.reset()

	draw(win,grid,ROWS,WIDTH)
pygame.quit()