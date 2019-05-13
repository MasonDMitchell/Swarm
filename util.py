from pickle import load
from os import walk, path
from networkx import read_gml 

#Example of how to load data for a specific file:

#data, graph = load_data(filepaths_mac()[0])

def filepaths_mac():
    directory = '/Volumes/DATA/data'
    filepaths = []
    for subdir, dirs, files in walk(directory):
        for file in files:
            if(file != ".DS_Store"):
                filepaths.append(path.join(subdir, file))
    return filepaths

def load_data_mac(filepath): 
    data = load(open(filepath,'rb'))
    graph = []
    for i in range(20):
        graph.append(read_gml("/Volumes/DATA/network_data/"+filepath[12:-2]+"_net"+str(i)+".gml"))
    return data, graph


def filepaths_pc():
    #TODO Directory needs changed
    directory = './data/'
    filepaths = []
    for subdir, dirs, files in walk(directory):
        for file in files:
            if(file != ".DS_Store"):
                filepaths.append(path.join(subdir, file))
    return filepaths

def load_data_pc(filepath): 
    data = load(open(filepath,'rb'))
    #TODO Directory needs changed
    graph = []
    for i in range(20):
        graph.append(read_gml("./network_data/"+filepath[12:-2]+"_net"+str(i)+".gml"))
    return data, graph

def filepaths_local():
    directory = './data'
    filepaths = []
    for subdir, dirs, files in walk(directory):
        for file in files:
            if(file != ".DS_Store"):
                filepaths.append(path.join(subdir, file))
    return filepaths

def load_data_local(filepath): 
    data = load(open(filepath,'rb'))
    graph = []
    for i in range(20):
        graph.append(read_gml("./network_data/"+filepath[12:-2]+"_net"+str(i)+".gml"))
    return data, graph
