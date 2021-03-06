import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon
from prm import *

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


for i in range(300):
   graph.makeNode()
   fig.canvas.draw_idle()
   plt.pause(0.05)
graph.reachEnd()
plt.waitforbuttonpress()