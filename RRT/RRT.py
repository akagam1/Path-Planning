import matplotlib.pyplot as plt
import numpy as np
import time

class RRTMap:
	#global ax

	def __init__(self,start,goal,mapDim,obsDim,obsNum,fig,ax):
		self.start = start
		self.goal = goal
		self.mapDim = mapDim
		self.mapHt,self.mapWd = self.mapDim

		self.nodeRad = 0
		self.ax = ax
		self.fig = fig

		self.obstacles = []
		self.obsDim = obsDim
		self.obsNum = obsNum

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
				centreX, centreY, obsRad = self.makeCircle()
				#create the circle
				a,b = self.start
				c,d = self.goal
				circle = plt.Circle((centreX,centreY),obsRad, color='black')
				if ((a-centreX)**2 + (b-centreY)**2 <= obsRad) or ((c-centreX)**2 + (d-centreY)**2 <= obsRad):
					collide = True
				else:	
					collide = False
					
			obs.append(circle)

		self.obstacles = obs.copy()	
		return obs

	def drawMap(self):
		obs = self.makeObs()
		startNode = plt.Circle(self.start, 0.01, color='blue')
		goalNode = plt.Circle(self.goal, 0.01, color='red')
		self.ax.add_patch(startNode) 
		self.ax.add_patch(goalNode)
		for i in range(len(obs)):
			self.ax.add_patch(obs[i])


	def drawPath(self):
		pass

	def drawObs(self):
		pass
		
	def addNode(self):
		trial = plt.Circle((np.random.rand(),np.random.rand()),0.01,color='yellow')
		self.ax.add_patch(trial)

			
"""class RRTGraph:

	def __init__(self,start,goal,mapDim,obsDim,obsNum):
		(x,y) = start
		self.start = start
		self.goal = goal
		self.goalFlag = False
		self.mapHt,self.mapWd = mapDim

		self.x = []
		self.y = []
		self.parent = []
		self.x.append(x)
		self.y.append(y)
		self.parent.append(0)

		self.obstacles = []
		self.obsDim = obsDim
		self.obsNum = obsNum

		self.goalState = None
		self.path = []


	def makeCircle(self):
		bounds = True
		while bounds:
			tempX = np.random.rand()
			tempY = np.random.rand()
			radius = np.random.rand()
			if tempX<=0.1 or tempX>=0.9 or tempY<=0.1 or tempY>=0.9 or radius>=0.01 or radius<=0.005:
				bounds = True
			else:
				bounds = False
		return tempX,tempY,radius

	def makeObs(self):
		obs=[]
		for i in range(0, self.obsNum):
			collide = True
			while collide:
				centreX, centreY, obsRad = self.makeCircle()
				#create the circle
				a,b = self.start
				c,d = self.goal
				circle = plt.Circle((centreX,centreY),radius=obsRad, color='black')
				if ((a-centreX)**2 + (y-centreY)**2 <= obsRad) or ((c-centreX)**2 + (d-centreY)**2 <= obsRad):
					collide = True
				else:
					collide = False
					ax.add_patch(circle)
				obs.append(circle)


	def addNode(self):
		x, y = [],[]
		sc = ax.scatter(x,y)
		plt.xlim(0,10)
		plt.ylim(0,10)

		plt.draw()
		for i in range(10):
			x.append(random.randint(0,10))
			y.append(random.randint(0,10))
			sc.set_offsets(np.c_[x,y])
			fig.canvas.draw_idle()
			plt.pause(0.5)

	def removeNode(self):
		pass

	def number_of_nodes(self):
		pass

	def distance(self):
		pass

	def nearest(self):
		pass"""