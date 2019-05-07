import numpy as np
from include import *

#Everything standard to m/s

class Swarm:
    def __init__(self,size):
        self.size = size
        self.position = np.random.rand(size,3)*2
        self.velocity = np.random.rand(size,3)

        self.can_see = []
        for i in range(size):
            self.can_see.append([])

        self.can_see_pos = []
        for i in range(size):
            self.can_see_pos.append([])

        self.can_see_vel = []
        for i in range(size):
            self.can_see_vel.append([])
        
        self.separate = []
        for i in range(size):
            self.separate.append([])

        self.alignment = []
        for i in range(size):
            self.alignment.append([])

        self.cohesion = []
        for i in range(size):
            self.cohesion.append([])

    def cur_pos(self):
        return self.position
    
    def cur_vel(self):
        return self.velocity
    
    def proximity(self,prox_size):
        for j in range(self.size):  
            pos_from_j = np.subtract(self.position,self.position[j])
            dist_from_j = all_vector_length(pos_from_j)
            
            temp_can_see = []
            temp_can_see_pos = []
            temp_can_see_vel = []
            for i in range(len(dist_from_j)):
                if(dist_from_j[i] < prox_size and i != j):
                    temp_can_see.append(i)
                    temp_can_see_pos.append(self.position[i])
                    temp_can_see_vel.append(self.velocity[i])
            self.can_see[j] = temp_can_see
            self.can_see_pos[j] = temp_can_see_pos
            self.can_see_vel[j] = temp_can_see_vel
        return self.can_see         
    
    def separate(self):
        total_pos_arr = []
        for i in range(size):
            total_pos = np.sum(np.subtract(self.can_see_pos[i],position[i]))
            total_pos_arr.append(total_pos)
        self.separate = all_scale_vector(total_pos_arr)
        return self.separate

    def alignment(self):
        total_vel_arr = []
        for i in range(size):
            total_vel = np.sum(np.subtract(self.can_see_vel[i],velocity[i]))
            total_vel_arr.append(total_vel)
        self.alignment = all_scale_vector(total_vel_arr)
        return self.alignment

    def cohesion(self): 
        avg_pos_arr = []
        for i in range(size):
            if(len(can_see) == 0):
                avg_pos_arr.append(np.zeros(3,dtype=int))
            else:
                avg_pos = np.sum(self.can_see_pos[i])/len(self.can_see)     
                avg_pos_arr.append(np.subtract(avg_pos,position[i]))
        self.cohesion = all_scale_vector(avg_pos_arr)
        return cohesion

    def separation_alignment_cohesion(self):
        total_pos_arr = []
        total_vel_arr = []
        avg_pos_arr = []
        for i in range(self.size):

            if(len(self.can_see[i])==0):
                total_pos_arr.append(np.zeros(3,dtype=int))
                total_vel_arr.append(np.zeros(3,dtype=int))
                avg_pos_arr.append(np.zeros(3,dtype=int))

            else:

                total_pos = np.sum(np.subtract(self.can_see_pos[i],self.position[i]),axis=0)
                total_pos_arr.append(total_pos)

                total_vel = np.sum(np.subtract(self.can_see_vel[i],self.velocity[i]),axis=0)
                total_vel_arr.append(total_vel)

                avg_pos = np.sum(self.can_see_pos[i],axis=0)/len(self.can_see)     
                avg_pos_arr.append(np.subtract(avg_pos,self.position[i]))
        self.separate = np.array([-1,-1,-1])*np.array(all_scale_vector(total_pos_arr))
        self.alignment = all_scale_vector(total_vel_arr)
        self.cohesion = all_scale_vector(avg_pos_arr)
        return [self.separate,self.alignment,self.cohesion]

    #Weights is [separation,alignment,cohesion]
    def simulate(self,time,timestep,weight):
        for i in np.arange(0,time,timestep):
            self.proximity(4)
            self.separation_alignment_cohesion()
            self.velocity = np.sum([(self.separate*weight[0]),(self.alignment*weight[1]),(self.cohesion*weight[2])],axis=0)
            self.position = self.position+self.velocity
            #print(self.position) 