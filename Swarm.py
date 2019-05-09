import numpy as np
from include import *
from scipy import spatial
import pickle
import datetime
#Everything standard to m/s

class Swarm:
    def __init__(self,size):
        self.size = size
        self.position = np.random.rand(size,3)*-5
        self.velocity = np.random.rand(size,3)*.2

        self.can_see = [[]]*size

        self.can_see_pos = [[]]*size

        self.can_see_vel = [[]]*size
        
        self.separate = [[]]*size

        self.alignment = [[]]*size

        self.cohesion = [[]]*size

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
    
    def efficient_prox(self,prox_size):
        tree = spatial.cKDTree(self.position)
        is_close = tree.query_ball_tree(tree,prox_size)

        self.can_see = [np.array(i) for i in is_close]
        self.can_see_pos = [self.position[i] for i in self.can_see]
        self.can_see_vel = [self.velocity[i] for i in self.can_see]
        return self.can_see

    def separation_alignment_cohesion_discrete(self,weight,timestep):
        for i in range(self.size):
            if(i==0):
                print(len(self.can_see[i]))
                print(self.can_see[i])
            if(len(self.can_see[i])<2):
                self.separate[i] = (np.zeros(3,dtype=int))
                self.alignment[i] = (np.zeros(3,dtype=int))
                self.cohesion[i] = (np.zeros(3,dtype=int))
            else:
                total_pos = np.sum(np.subtract(self.can_see_pos[i],self.position[i]),axis=0)
                total_vel = np.sum(self.can_see_vel[i],axis=0)
                avg_pos = (np.sum(self.can_see_pos[i],axis=0)/len(self.can_see[i]))-self.position[i]  

                self.separate[i] = np.array(np.array([-1,-1,-1])*np.array(scale_vector(total_pos)))
                self.alignment[i] = np.array(scale_vector(total_vel))
                self.cohesion[i] = np.array(scale_vector(avg_pos))
            #self.position[i] = self.position[i]+self.velocity[i]
        return [self.separate,self.alignment,self.cohesion]

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

                total_vel = np.sum(self.can_see_vel[i],axis=0)
                total_vel_arr.append(total_vel)

                avg_pos = (np.sum(self.can_see_pos[i],axis=0)/len(self.can_see[i]))-self.position[i]  
                avg_pos_arr.append(np.subtract(avg_pos,self.position[i]))

        self.separate = np.array([-1,-1,-1])*np.array(all_scale_vector(total_pos_arr))
        self.alignment = all_scale_vector(total_vel_arr)
        self.cohesion = all_scale_vector(avg_pos_arr)
        return [self.separate,self.alignment,self.cohesion]

    #Weights is [proximity,separation,alignment,cohesion]
    def simulate(self,time,timestep,weight):
        total_data = []
        total_pos = []
        total_can_see = []
        for i in np.arange(0,time,timestep):
            self.efficient_prox(weight[0])
            self.separation_alignment_cohesion()            
            self.velocity = all_scale_vector(np.sum([(self.separate*weight[1]),(self.alignment*weight[2]),(self.cohesion*weight[3])],axis=0),timestep)
            self.position = self.position+self.velocity
            total_pos.append(self.position)
            total_can_see.append(self.can_see)
        x = datetime.datetime.now()
        tot_time = x.strftime("%m")+"_"+x.strftime("%d")+"_"+x.strftime("%X")
        total_data.append(total_pos)
        total_data.append(total_can_see)
        total_data.append(weight)
        pickle.dump(total_data,open('data/'+tot_time+'.p','wb'))
