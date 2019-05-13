import numpy as np
import scipy as sci
import networkx as nx
from util import *

filepaths = filepaths_local()
for f in filepaths:
    data, graph = load_data_local(f)    
    for G in graph:
        print(G.number_of_edges())
        print(list(nx.connected_components(G)))
