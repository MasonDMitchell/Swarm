import numpy as np
import scipy as sci
import networkx as nx
from os import walk, path
from pickle import load

directory = '/Volumes/DATA/data/run3'

#Go through directory and append filepaths to 'filepaths'
filepaths = []
for subdir, dirs, files in walk(directory):
    for file in files:
        if(file != ".DS_Store"):
            filepaths.append(path.join(subdir, file))

#Iterating through each file
for f in filepaths:

    #Get data from file
    data = load(open(f,'rb'))
    total_can_see = data[0]
    
    #Iterate through per timestep
    for t in range(len(total_can_see)):
    
        #Get timestep's can_see & initialize the Graph
        can_see = total_can_see[t]
        Graph = nx.Graph()
        Graph.add_nodes_from(range(0,400))
    
        #Create list of edges from can_see that can be parsed by networkX 
        edge_paths = []
        for j in range(len(can_see)):
            for i in can_see[j]:
                edge_paths.append((j,i))

        #Add the edges to the Graph
        Graph.add_edges_from(edge_paths)
        
        #Save graph file
        nx.write_gml(Graph,"/Volumes/DATA/network_data/" + f[24:-2]+"_net"+str(t)+".gml")

