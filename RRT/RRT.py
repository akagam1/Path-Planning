import matplotlib.pyplot as plt
import numpy as np
import time
import math

class RRTMap:

	def __init__(self,start,goal,obsNum,fig,ax):
		self.start = start
		self.goal = goal

		self.goalFlag = False
		self.x = []
		self.y = []
		self.parent = []
		self.x.append(self.start[0])
		self.y.append(self.start[1])
		self.parent.append(0)
		self.validConnects = []

		self.nodeRad = 0
		self.ax = ax
		self.fig = fig

		self.obstacles = []
		self.obsNum = obsNum
		self.obsX = []
		self.obsY = []
		self.obsRad = []

		self.infinity = False

	def addNode(self,n,x,y):
		self.x.insert(n,x)
		self.y.insert(n,y)
	
	def parentlen(self):
		return len(self.parent)

	def removeNode(self,n):
		self.x.pop(n)
		self.y.pop(n)

	def addEdge(self,parent,child):
		self.parent.insert(child+1,parent)
		x1,y1 = self.x[parent], self.y[parent]
		x2,y2 = self.x[child], self.y[child]
		line = plt.Line2D((x1,x2),(y1,y2), color='cyan')
		self.ax.add_line(line)

	def removeEdge(self,n):
		self.parent.pop(n)

	def number_of_nodes(self):
		return len(self.x)

	def distance(self,n1,n2):
		x1,y1 = self.x[n1],self.y[n1]
		x2,y2 = self.x[n2],self.y[n2]
		distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
		return distance

	def nearest(self,validConnects,n):
		dmin = self.distance(0,n)
		nodeNum = 0
		for i in range(0,len(validConnects)):
			dtemp = self.distance(validConnects[i],n)
			if dtemp < dmin:
				dmin = dtemp
				nodeNum = validConnects[i]
		return nodeNum

	def step(self, near, randNode, dmax = 0.05):
		d = self.distance(near,randNode)
		xnear,ynear = self.x[near],self.y[near]
		xrand,yrand = self.x[randNode],self.y[randNode]
		if xrand == self.goal[0] and yrand == self.goal[1]:
			if d>dmax:
				u = dmax/d
				px,py = xrand-xnear, yrand-ynear
				theta = math.atan2(py,px)
				x,y = xnear+dmax*math.cos(theta),ynear + dmax*math.sin(theta)
				self.removeNode(randNode) 
				self.addNode(randNode,x,y)
			else:
				self.goalFlag = True

		elif d>dmax:
			u = dmax/d
			px,py = xrand-xnear, yrand-ynear
			theta = math.atan2(py,px)
			x,y = xnear+dmax*math.cos(theta),ynear + dmax*math.sin(theta)
			self.removeNode(randNode)
			if (x-self.goal[0])**2 + (y-self.goal[1])**2 <= 0.05**2:
				self.addNode(randNode,self.goal[0],self.goal[1])
				self.goalState = randNode
				self.goalFlag = True
			else:
				self.addNode(randNode,x,y)
		else:
			if (xrand-self.goal[0])**2 + (yrand-self.goal[1])**2 <= 0.05**2:
				self.removeNode(randNode)
				self.addNode(randNode,self.goal[0],self.goal[1])
				self.goalState = randNode
				self.goalFlag = True

			#no else statement as xrand,yrand are already present in the x,y lists

	def makeCircle(self):
		bounds = True
		while bounds:
			tempX = np.random.rand()
			tempY = np.random.rand()
			radius = np.random.rand()
			if tempX<=0.1 or tempX>=0.9 or tempY<=0.1 or tempY>=0.9 or radius>=0.05 or radius<=0.01:
				bounds = True
			else:
				bounds = False
		return tempX,tempY,radius

	def makeObs(self):
		obs=[]
		for i in range(0, self.obsNum):
			collide = True
			while collide:
				centreX, centreY, rad = self.makeCircle()
				#create the circle
				a,b = self.start
				c,d = self.goal
				circle = plt.Circle((centreX,centreY),rad, color='black')
				if ((a-centreX)**2 + (b-centreY)**2 <= rad) or ((c-centreX)**2 + (d-centreY)**2 <= rad):
					collide = True
				else:	
					collide = False
			
			self.obsX.append(centreX)
			self.obsY.append(centreY)
			self.obsRad.append(rad)
			obs.append(circle)

		self.obstacles = obs.copy()	
		return obs

	def drawMap(self):
		obs = self.makeObs()
		startNode = plt.Circle(self.start, 0.01, color='darkgreen')
		goalNode = plt.Circle(self.goal, 0.05, color='red')
		self.ax.add_patch(startNode) 
		self.ax.add_patch(goalNode)
		for i in range(len(obs)):
			self.ax.add_patch(obs[i])


	def drawPath(self,child):
		parent = self.parent[child]
		xp,yp = self.x[parent],self.y[parent]
		xc,yc = self.x[child],self.y[child]
		line = plt.Line2D((xc,xp),(yc,yp),color='gold')
		self.ax.add_line(line)
		return parent
		
	def makeNode(self):
		choice = np.random.rand()
		if choice<=0.3:
			self.expand()
		else:
			self.validConnects = []
			nodes = self.number_of_nodes()
			self.addNode(nodes,self.goal[0],self.goal[1])
			for i in range(len(self.x)):
				self.connect(i,nodes)
			if len(self.validConnects) == 0:
				self.removeNode(nodes)
				self.expand()
			else:
				near = self.bias()
				if self.infinity == True:
					self.removeNode(nodes)
					self.expand()
				else:
					nodeRadius = 0.005
					x,y = self.x[nodes],self.y[nodes]
					node = plt.Circle((x,y),nodeRadius,color='deeppink')
					self.ax.add_patch(node)
					self.addEdge(near,nodes)
		return self.goalFlag

	def nodeCheck(self,x,y):
		for i in range(len(self.obsX)):
			if (x-self.obsX[i])**2 + (y-self.obsY[i])**2 <= self.obsRad[i]**2:
				return True
		if (x-self.start[0])**2 + (y-self.start[1])**2 <= 0.01**2:
			return True
		return False
	
	def crossObstacle(self,x1,x2,y1,y2):
		dy = y2-y1
		dx = x2-x1
		if dx == 0:
			self.infinity = True
			return True
		self.infinity = False
		m = dy/dx
		d = (dx*y2-dy*x2)/dx
		xmin,ymin = min(x1,x2),min(y1,y2)
		xmax,ymax = max(x1,x2),max(y1,y2)
		for i in range(len(self.obstacles)):
			a = 1+m**2
			b = 2*m*(d-self.obsY[i])-2*self.obsX[i]
			c = self.obsX[i]**2+(d - self.obsY[i])**2 - self.obsRad[i]**2
			disc = b**2 - 4*a*c
			if disc >= 0:

				xint = (-b + disc**0.5)/(2*a)
				yint = m*xint + d
				if (xint>xmin and xint<xmax and yint>ymin and yint<ymax):
					return True
			
		return False

	def connect(self,n1,n2):
		x1,y1 = self.x[n1], self.y[n1]
		x2,y2 = self.x[n2], self.y[n2]
		if not self.crossObstacle(x1,x2,y1,y2):
			self.validConnects.append(n1)

	def bias(self):
		nodes = self.number_of_nodes()-1
		nodeRadius = 0.005
		validConnects = self.validConnects
		near = self.nearest(validConnects, nodes)
		self.step(near,nodes)
		return near

	def expand(self):
		notValid = True
		while notValid:

			x=np.random.rand()
			y=np.random.rand()
			nodeRadius = 0.005
			notValid = self.nodeCheck(x,y)
			if notValid == False:
				self.x.append(x)
				self.y.append(y)
				self.validConnects = []
				for i in range(0,len(self.x)-1):
					self.connect(i,len(self.x)-1)
					
				if len(self.validConnects)>=1:
					notValid = False
				else:
					self.removeNode(len(self.x)-1)
					notValid = True

		nodes = self.number_of_nodes()-1
		validConnects = self.validConnects
		nearestNode = self.nearest(validConnects,nodes)
		self.step(nearestNode, nodes, 0.05)
		x,y = self.x[nodes],self.y[nodes]
		node = plt.Circle((x,y),nodeRadius,color='deeppink')
		self.ax.add_patch(node)
		self.addEdge(nearestNode,nodes)