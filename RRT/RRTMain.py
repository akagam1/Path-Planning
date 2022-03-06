import matplotlib.pyplot as plt
from RRT import RRTMap
import time


plt.ion()
fig, ax = plt.subplots()
plt.xlim(0,1)
plt.ylim(0,1)
plt.get_current_fig_manager().canvas.set_window_title('RRT Visualizer')
plt.draw()


graph = RRTMap((0.1,0.9),(0.9,0.1),40,fig,ax)
obstacles = graph.drawMap()

stop = False
plt.pause(2)
while not stop:
    stop = graph.makeNode()
    fig.canvas.draw_idle()
    plt.pause(0.05)

#plt.waitforbuttonpress()

child = graph.number_of_nodes() - 1
start = False
while not start:
    current = graph.drawPath(child)
    fig.canvas.draw_idle()
    plt.pause(0.05)
    child = current
    if child == 0:
        start = True
plt.waitforbuttonpress()