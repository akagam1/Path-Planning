import matplotlib.pyplot as plt
from RRT import RRTMap, RRTGraph

block = RRTMap((0.5,0.5),(0.8,0.2),(5,5),6,10)

obstacles = block.drawMap()