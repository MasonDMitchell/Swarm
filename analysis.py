import pickle
import os

#data/run0,1,2,3/[.p files]
f = []
for (dirpath, dirnames, filenames) in os.walk('./data'):
    print(dirpath)
    print(dirnames)
    print(filenames)
    for file in filenames:
        print(file)
        f.append(dirpath + "\\" + file)

print(f)
num_files = len(os.listdir('./data')) - 1
print(num_files)
#pickle.load('./data/')
for file in f:
    temp_file = open(file, "r")
    contents = temp_file.read()
    print(contents)
