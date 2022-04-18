import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon
from RRTS import *

plt.ion()
fig, ax = plt.subplots()
plt.xlim(0,100)
plt.ylim(0,100)
#plt.get_current_fig_manager().canvas.set_window_title('RRT* Visualizer')
fig.canvas.manager.set_window_title('RRT* Visualizer')
plt.draw()

polygon = [Polygon([(10, 10),
   (40, 10),
   (40, 40),
   (10, 40),
]), Polygon([(60,20),
   (80,20),
   (40,80)])]

graph = Map((2,98),(90,5),1,fig,ax)
graph.drawObs(polygon)
graph.drawMap()
"""line = plt.Line2D((2,2),(98,83),color='blue')
ax.add_line(line)"""

goal = False

while not goal:
   goal = graph.makeNode()
   fig.canvas.draw_idle()
   plt.pause(0.05)


child = graph.totalNodes() - 1
start = False
while not start:
    current = graph.drawPath(child)
    fig.canvas.draw_idle()
    plt.pause(0.1)
    child = current
    if child == 0:
        start = True
plt.waitforbuttonpress()
"""for i in range(50):
   graph.makeNode()
   fig.canvas.draw_idle()
   plt.pause(0.05)
plt.waitforbuttonpress()"""