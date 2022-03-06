import matplotlib.pyplot as plt
from RRT import RRTMap
import time


plt.ion()
fig, ax = plt.subplots()
plt.xlim(0,1)
plt.ylim(0,1)
plt.get_current_fig_manager().canvas.set_window_title('RRT Visualizer')
plt.draw()


block = RRTMap((0.1,0.9),(0.9,0.1),(5,5),6,40,fig,ax)
obstacles = block.drawMap()

stop = False
while not stop:
    stop = block.makeNode()
    fig.canvas.draw_idle()
    plt.pause(0.05)

#plt.waitforbuttonpress()

child = block.number_of_nodes() - 1
start = False
"""print(block.parentlen())
print(child)"""
while not start:
    current = block.drawPath(child)
    fig.canvas.draw_idle()
    plt.pause(0.05)
    child = current
    if child == 0:
        start = True
plt.waitforbuttonpress()