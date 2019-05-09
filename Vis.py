import matplotlib as mpl
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
import scipy as sci
import pandas as pd
import pickle
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import animation

plt.style.use('dark_background')
mpl.rc('axes',prop_cycle=cycler(color=['#2dedff','#ffae00','m','#02d11a','#e6f202','#2f58fc']),grid=True)
mpl.rc('grid',color='#6d6d6d')
mpl.rc('legend',frameon=False)

total_data = pickle.load(open('data/data.p','rb'))
total_pos = total_data[0]

fig = plt.figure()
ax = p3.Axes3D(fig)
d0, = ax.plot([],[],[],'bo',ms=6)

def init():
    d0.set_data([],[])
    d0.set_3d_properties([])
    return d0,

def animate(i):
    x = []
    y = []
    z = []
    for j in range(len(total_pos[i])):
        x.append(total_pos[i][j][0])
        y.append(total_pos[i][j][1])
        z.append(total_pos[i][j][2])
    d0.set_data(x,y)
    d0.set_3d_properties(z)
    return d0,

ax.set_xlim3d([-20,20])
ax.set_xlabel('X')

ax.set_ylim3d([-20, 20])
ax.set_ylabel('Y')

ax.set_zlim3d([-20, 20])
ax.set_zlabel('Z')

ax.set_title('3D Boids Plot')

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(total_pos), interval=100, blit=True)
plt.show()
#anim.save('videos/fly.mp4', fps=100, extra_args=['-vcodec', 'libx264'])

