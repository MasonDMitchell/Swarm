import matplotlib as mpl
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
import scipy as sci
from include import *
from Swarm import Swarm
import os
i = 0
while os.path.isdir("/Volumes/DATA/data/run"+str(i)):
    i += 1

path = '/Volumes/DATA/data/run'+str(i)
os.mkdir(path)
#p = proxy
#s = separation
#a = alignment
#c = cohesion

for p in np.arange(4,6,1):
    for s in np.arange(0,1,.1):
        for a in np.arange(0,1,.1):
            for c in np.arange(0,1,.1):
                x = Swarm(400)
                x.simulate(path,10,.1,[p,s,a,c],False)
