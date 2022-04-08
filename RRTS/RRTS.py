import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon, Point
import numpy as np

class Node:

	def __init__(self, x, y, parent):
		self.x = x
		self.y = y 
		self.parent = parent


class Obstacle:

	def __init__ (self, sides, x, y):
		self.sides = sides
		self.x = x
		self.y = y

class Map:

	def __init__ (self, start, goal, obsNum, fig, ax):
		self.start = start
		self.goal = goal
		self. obsNum = obsNum
		self.fig = fig
		self.ax = ax
		self.plt = plt

		self.nodes = []
		self.obstacles = []

		self.nodes.append(Node(self.start, self.goal, 0))

		self.goalFlag = False

		self.neighbour = 15
		self.step = 10

		self.validConnects = []

	def addNode(self, n, x, y):
		self.nodes.insert(n, Node(x,y,None))

	def removeNode(self, n):
		self.nodes.pop(n)

	def totalNodes(self):
		return len(self.nodes)

	def drawObs(self, obs_list):
		for i in range(len(obs_list)):
			x, y = obs_list[i].exterior.xy
			self.obstacles.append(obs_list[i])
			plt.plot(x, y, c="black")
			plt.show()

	def drawMap(self):
		startNode = plt.Circle(self.start, 2, color='darkgreen')
		goalNode = plt.Circle(self.goal, 4, color='red')
		self.ax.add_patch(startNode) 
		self.ax.add_patch(goalNode)

	def collision(self, x,y):
		point = Point(x,y)
		for i in range(len(self.obstacles)):
			if point.within(self.obstacles[i]):
				return True
		return False

	def makeNode(self):
		notValid = True
		while notValid:
			x = np.random.randint(0,100)
			y = np.random.randint(0,100)
			notValid = self.collision(x,y)

			if notValid == False:

				self.validConnects = []
				for i in range(len(self.nodes)):
					check = edgeCheck()
					if check:
						self.validConnects.append(self.nodes[i])
						notValid = False
					else:
						notValid = True

				node = plt.Circle((x,y),0.5,color='deeppink')
				self.ax.add_patch(node)

	def edgeCheck(self,pNew,p):
		xNew, yNew = pNew
		x, y = p

		#make divisions of the line and check if any of its sub-points lies in an obstacle
"""
####Checklist
1) check neighbour radius for other nodes
2) check if they are valid connections
3) add all to valid connects list
4) if valid connects list is empty, create a new node until you get at least one valid connect

	