"""
This example showcases a live plotting animation.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from time import *

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    animate.counter += 1

    time = localtime().tm_hour + (localtime().tm_min/60) + (localtime().tm_sec/3600)
    print('Time is:', time, 'hrs')
    print(localtime().tm_hour, 'hrs,', localtime().tm_min, 'mins and', localtime().tm_sec, 'secs')
    xs.append(time)

    # This is what will be altered to hold power station values
    ys.append(np.random.rand())

    ax1.clear()
    ax1.plot(xs, ys)

animate.counter = 0

xs = []
ys = []

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
