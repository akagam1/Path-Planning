import matplotlib.pyplot as plt
from RRT import RRTMap, RRTGraph
import time


plt.ion()
fig, ax = plt.subplots()
plt.xlim(0,1)
plt.ylim(0,1)
plt.get_current_fig_manager().canvas.set_window_title('RRT Visualizer')
plt.draw()


block = RRTMap((0.1,0.8),(0.9,0.1),(5,5),6,40,fig,ax)

trial = block.drawPath()
obstacles = block.drawMap()

for i in range(10):
    block.addNode()
    fig.canvas.draw_idle()
    plt.pause(0.5)

plt.waitforbuttonpress()
