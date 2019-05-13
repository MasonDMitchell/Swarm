import pickle
from os import walk
import numpy as np

def giant_component(can_see, file_num):
    iteration_num = 0
    for iteration in can_see:
        print(str(1000*file_num + iteration_num))
        components = []
        analyzed = np.zeros(400) - 1
        sum_analyzed = 0
        component = []
        while(sum_analyzed < 400):
            component = []
            seen = []
            id = 0
            for id in range(analyzed.shape[0]):
                if(analyzed[id] == -1):
                    break
            component.append(id)
            seen.extend(iteration[id][1:])
            analyzed[id] = 1
            sum_analyzed += 1
            while(len(seen) > 0 and sum_analyzed < 400):
                #print(sum(analyzed))
                if(analyzed[seen[0]] == -1):
                    component.append(seen[0])
                    analyzed[seen[0]] = 1
                    sum_analyzed += 1
                    seen.extend(iteration[seen[0]])
                seen.pop(0)
            components.append(component)
            if(len(component) > 200):
                break
            #if(len(component) != 400 and len(component) != 1):
                #print(len(component))
                #print(data[1])
        iteration_num += 1
#data/run0,1,2,3/[.p files]
f = []
for (dirpath, dirnames, filenames) in walk('D:/data'):
    for file in filenames:
        #print(file)
        if(file != ".DS_Store"):
            f.append(dirpath + "\\" + file)

#print(f)
print(len(f))
#pickle.load('./data/')
file_num = 0
for file in f:
    data = pickle.load(open(file, "rb"))
    can_see = data[0]
    giant_component(can_see, file_num)
    file_num += 1
    break
