import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon, Point
import numpy as np
import math

class Node:

	def __init__(self, x, y, isStart=False):
		self.x = x
		self.y = y 
		self.parent = []
		self.isStart = isStart

	def coordinates(self):
		return (self.x, self.y)

	def addParent(self, parent):
		self.parent.append(parent)

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

		self.xStart, self.yStart = self.start
		self.nodes.append(Node(self.xStart, self.yStart, True))
		self.nodes[0].addParent(0)

		self.goalFlag = False
		self.step = 50

		self.validConnects = []
		self.nearest = []
		self.edges = {}
		self.kNearest = 3

	def totalNodes(self):
		return len(self.nodes)

	def reachEnd(self):
		self.nearest = []
		self.validConnects = []
		point = self.goal
		for i in range(len(self.nodes)):
			if not self.edgeCheck(point, self.nodes[i].coordinates()):
				self.validConnects.append(i)
		for i in range(len(self.validConnects)):
			if len(self.nearest) < self.kNearest:
				self.nearest.append(self.validConnects[i])
			else:
				maximum = 0
				for j in range(len(self.nearest)):
					p1 = self.nodes[self.nearest[j]].coordinates()
					dist = self.distance(point,p1)
					if dist > maximum:
						maximum = j
				p1 = self.nodes[self.nearest[maximum]].coordinates()
				p2 = self.nodes[self.validConnects[i]].coordinates()
				if self.distance(point, p1) > self.distance(point, p2):
					self.nearest[maximum] = self.validConnects[i]
		self.nodes.append(Node(point[0],point[1]))
		node = plt.Circle(point, 1, color='blue')
		self.ax.add_patch(node)
		for i in range(len(self.nearest)):
			index = self.nearest[i]
			self.drawEdge(point, self.nodes[index].coordinates(),len(self.nodes)-1,index)
			self.nodes[-1].addParent(index)


	def drawObs(self, obs_list):
		for i in range(len(obs_list)):
			x, y = obs_list[i].exterior.xy
			self.obstacles.append(obs_list[i])
			plt.plot(x, y, c="black")
			plt.show()

	def drawMap(self):
		startNode = plt.Circle(self.start, 2, color='darkgreen')
		goalNode = plt.Circle(self.goal, 5, color='red')
		self.ax.add_patch(startNode) 
		self.ax.add_patch(goalNode)

	def drawPath(self, child):
		parent = self.nodes[child].parent
		xp,yp = self.nodes[parent].coordinates()
		xc,yc = self.nodes[child].coordinates()
		line = plt.Line2D((xc,xp),(yc,yp),color='aqua')
		self.ax.add_line(line)
		return parent

	def collision(self, x,y):
		point = Point(x,y)
		for i in range(len(self.obstacles)):
			if point.within(self.obstacles[i]):
				return True
		return False


	def makeNode(self):
		self.validConnects =[]
		self.nearest = []

		notValid = True

		# KNearst Nodes logic
		"""
		1) create validConnects
		2) find the 5 nearest nodes in validConnects

		"""
		while notValid:
			x = np.random.rand()*100
			y = np.random.rand()*100
			if self.collision(x,y) == False:
				notValid = False

			if notValid == False:
				for i in range(len(self.nodes)):
					if self.distance((x,y), self.nodes[i].coordinates()) < 20:
						if self.edgeCheck((x,y),self.nodes[i].coordinates()) == False:
							self.validConnects.append(i)
				if len(self.validConnects) == 0:
					notValid = True

		point = (x,y)
		for i in range(len(self.validConnects)):
			if len(self.nearest) < self.kNearest:
				self.nearest.append(self.validConnects[i])
			else:
				maximum = 0
				for j in range(len(self.nearest)):
					p1 = self.nodes[self.nearest[j]].coordinates()
					dist = self.distance(point,p1)
					if dist > maximum:
						maximum = j
				p1 = self.nodes[self.nearest[maximum]].coordinates()
				p2 = self.nodes[self.validConnects[i]].coordinates()
				if self.distance(point, p1) > self.distance(point, p2):
					self.nearest[maximum] = self.validConnects[i]

		self.nodes.append(Node(point[0],point[1]))
		node = plt.Circle(point, 1, color='blue')
		self.ax.add_patch(node)
		for i in range(len(self.nearest)):
			index = self.nearest[i]
			self.drawEdge(point, self.nodes[index].coordinates(),len(self.nodes)-1,index)
			self.nodes[-1].addParent(index)

	def expand(self):
		pass
		
	def edgeCheck(self,pNew,p):
		xNew, yNew = pNew
		x, y = p

		for i in range(len(self.obstacles)):
			for j in range(1001):
				u = j/1000
				v = 1-u
				xTemp = (u*x + v*xNew)
				yTemp = (u*y + v*yNew)
				point = Point(xTemp,yTemp)
				if point.within(self.obstacles[i]):
					return True
		return False

	def distance(self, p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		dist = (x1-x2)**2 + (y1-y2)**2
		return dist**0.5 

	def drawEdge(self, p1, p2, i1, i2):
		xc,yc = p1
		xp, yp = p2
		line = plt.Line2D((xc,xp),(yc,yp),color='green')
		self.ax.add_line(line)
		self.edges[f"{i1}-{i2}"] = line #stores edge line in dictionary with key as childIndex-parentIndex