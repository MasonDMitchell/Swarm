import numpy as np
import scipy as sci
import networkx as nx
from os import walk, path
from pickle import load
import csv
import time

#directory = '/Volumes/DATA/data/run3'
data_csv = "network_info.csv"
directories = ['D:/data/run0', 'D:/data/run1', 'D:/data/run2', 'D:/data/run3']

#Go through directory and append filepaths to 'filepaths'
filepaths = []
for directory in directories:
    for subdir, dirs, files in walk(directory):
        for file in files:
            if(file != ".DS_Store"):
                filepaths.append(path.join(subdir, file))
    print(len(filepaths))

#Iterating through each file
file_num = 0
print("Number of files: " + str(len(filepaths)))

start_time = time.time()
for f in filepaths:
    file_num += 1
    if file_num%5 == 0:
        print(str(file_num) + "Time to analyze last five files: " + str(time.time() - start_time))
        start_time = time.time()

    #Get data from file
    data = load(open(f,'rb'))
    total_can_see = data[0]
    weights = data[1]

    #Iterate through per timestep
    with open(data_csv, mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
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

            num_edges = nx.number_of_edges(Graph)

            components = list(nx.connected_components(Graph))
            num_components = len(components)
            giant = len(max(components, key=len))

            #Save network information
            #print([t] + weights + [num_edges] + [num_components] + [giant])
            data_writer.writerow([t] + weights + [num_edges] + [num_components] + [giant])

            #Save graph file
            #nx.write_gml(Graph,"/Volumes/DATA/network_data/" + f[24:-2]+"_net"+str(t)+".gml")
