import numpy as np
import scipy as sci
from pandas import DataFrame
from Particle import Drone
import math
from math import *
columns_per_drone = 2

def equation(equation,points,rangemap):
    rangesize = abs(max(rangemap))+abs(min(rangemap))
    timestep = rangesize/(math.sqrt(points) - 1)
    y_discretized_points = []
    x_discretized_points = []
    z_discretized_points = []
    x = min(rangemap)
    y = min(rangemap)
    e = 2.71828
    print(timestep)
    for j in range(int(math.sqrt(points))):
        for i in range(int(math.sqrt(points))):
            x_discretized_points.append(x)
            y_discretized_points.append(y)
            z_discretized_points.append(eval(equation))
            y = y+timestep
        x = x+timestep
        y = min(rangemap)
    points = np.array((x_discretized_points,y_discretized_points,z_discretized_points))
    size = len(points[0])
    points = np.reshape(points,size*3,order='F').reshape(size,3)
    return points

def nearest_point(drone,drones,positions,points):
    #total_pos = np.array(points) - np.array(my_pos)
    nearest_point = []
    for i in range(drones):
        #print(points)
        total_pos = np.subtract(points, positions[i])
        distance = all_vector_length(total_pos)
        nearest_point.append(distance.argmin())
        total_pos = np.subtract(points[nearest_point],positions[i])
    #TODO
    #Switch to all scale vector
    #make nearest point and vector a list of lists
    vector = all_scale_vector(total_pos)
    return [nearest_point,vector]

def is_solved(drone,drones,solved,positions,nearest_point,points,point_lim=.2):
    distance_from_point = []
    for i in range(drones):
        #print("i: "+str(i))
        #print(nearest_point[i])
        distance_from_point.append(np.subtract(points[nearest_point[i]], positions[i]))
    distance_from_point = all_vector_length(distance_from_point)   
    for i in range(drones):
        if(distance_from_point[i] < point_lim):
            solved[i] = False
    return solved

def proximity(drone_object,drones,drone,index):
    prox_size = 4
    can_see = []
    my_pos = np.array(drone.cur_pos())
    for i in range(drones):
        if(i != index):
            their_pos = np.array(drone_object[i].cur_pos())
            total_pos = vector_length(their_pos-my_pos)
            if(total_pos < prox_size):
                can_see.append(i)
    return can_see

#Positions is a list of (3,) vectors 
#drones is # of drones
#View size is how far away the drone can see others
def all_proximity(positions,drones,view_size=4):
    can_see = []
    positions=np.array(positions)
    for j in range(drones):
        #New positions is zeroing all of the positions to drone[i]
        new_positions = positions-positions[j]
        #This is getting the length of all of those positions
        total_pos = all_vector_length(new_positions)
        temp_can_see = []
        #This is putting the list index of those lengths under the view_size into the can_see list
        for i in range(len(total_pos)):
            if(total_pos[i] < view_size and i != j):
                temp_can_see.append(i)
        can_see.append(temp_can_see)
    return can_see
#TODO determine whether this should be based on the sum of vectors. I think not.

def separate(drone_object,drone,can_see):
    my_pos = np.array(drone.cur_pos())
    final_vector = np.array([0,0,0])
    for i in can_see:
        their_pos = np.array(drone_object[i].cur_pos())
        total_pos = np.array(their_pos-my_pos)
        total_pos = np.array(scale_vector(total_pos))
        final_vector = np.array(final_vector)+np.array(total_pos)
    final_vector = scale_vector(final_vector)
    final_vector = -1 * np.array(final_vector)    
    return final_vector

def alignment(drone_object,can_see):
    final_vector = np.array([0,0,0])
    for i in can_see:
        their_vel = np.array(scale_vector(drone_object[i].cur_vel()))
        final_vector = np.array(final_vector+their_vel)
    final_vector = scale_vector(final_vector)
    return final_vector
    
def cohesion(drone_object,drone,can_see):
    avg_pos=[0,0,0]
    if(len(can_see)==0):
        return [0,0,0]
    for i in can_see:
        avg_pos = np.array(avg_pos) + np.array(drone_object[i].cur_pos())
    my_pos = np.array(drone.cur_pos())
    avg_pos = np.array(avg_pos) / len(can_see)
    vector = np.array(np.array(avg_pos)-np.array(my_pos))
    return vector

def vector_length(vector):
    current_length = math.sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))
    return current_length

def all_vector_length(vectors):
    return np.array(np.sqrt(np.sum(np.square(vectors),axis=1)))
    
def scale_vector(vector,size=1):
    A = vector_length(vector)
    if(A == 0):
        return [0,0,0]
    return [vector[0]/(A/size), vector[1]/(A/size), vector[2]/(A/size)]

def all_scale_vector(vectors,size=1):
    A = all_vector_length(vectors)
    scaled_vectors = []
    for i in range(len(A)):
        if(A[i]==0):
            scaled_vectors.append([0,0,0])
        else:
            scaled_vectors.append(vectors[i]/(A[i]/size))
    return scaled_vectors

def init_data():
   data = []  
   pos_x = []
   pos_y = []
   pos_z = []
   data.append(pos_x)
   data.append(pos_y)
   data.append(pos_z)
   return data

def new_drone(data):
   data[0].append([])
   data[1].append([])
   data[2].append([])
   return data

def add_data(data,drone,index):
   position = drone.cur_pos()
   pos_x = position[0]
   pos_y = position[1]
   pos_z = position[2]
   data[0][index].append(pos_x)
   data[1][index].append(pos_y)
   data[2][index].append(pos_z)
   return data

def export_csv(data,drones,filename):
    data=np.array(data)
    df = DataFrame()
    for i in range(drones):
        df['d_' + str(i) + '_xpos'] = data[0][i]
        df['d_' + str(i) + '_ypos'] = data[1][i]
        df['d_' + str(i) + '_zpos'] = data[2][i]
    
    df.to_csv('./data/' + filename + '.csv',index=False)
