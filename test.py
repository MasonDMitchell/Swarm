import matplotlib as mpl
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
import scipy as sci
from include import *
from Swarm import Swarm
plt.style.use('dark_background')
mpl.rc('axes',prop_cycle=cycler(color=['#2dedff','#ffae00','m','#02d11a','#e6f202','#2f58fc']),grid=True)
mpl.rc('grid',color='#6d6d6d')
mpl.rc('legend',frameon=False)

x = Swarm(400)
x.simulate(3,.1,[3,.9,1.5,.7])
