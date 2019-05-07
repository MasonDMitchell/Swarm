import numpy as np
import scipy as sci

#Everything standardized to m/s. Code handles conversion for timesteps

class Drone:
    def __init__(self,x=0,y=0,z=0,v_x=0,v_y=0,v_z=0,a_x=0,a_y=0,a_z=0,at_point=False):
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.a_dX = 0
        self.a_dY = 0 
        self.a_dZ = 0
        self.at_point = False
        self.timestep = .1

    #Returns current position in list [x,y,z]
    def cur_pos(self):
        return [self.x,self.y,self.z]

    def is_solved(self):
        return self.at_point 
    
    def solved(self,booly):
        self.at_point = booly    

    #Returns current velocity in list [x_vel,y_vel,z_vel]
    def cur_vel(self):
        return [self.v_x,self.v_y,self.v_z]
     
    #Returns current acceleration in list [x_accel,y_accel,z_accel]
    def cur_accel(self):
        return [self.a_x,self.a_y,self.a_z]
    
    #Allows for instant setting of position with inputs x, y, z
    def set_pos(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    #Allows for instant setting of velocity with inputs vel_x, vel_y, vel_z
    def set_vel(self,vel_x=0,vel_y=0,vel_z=0):
        self.v_x = vel_x
        self.v_y = vel_y
        self.v_z = vel_z
    
    #Takes inputs delta-X and delta-Y
    #NOTE: Won't be applied until next iteration
    def delta_accel(self,dX=0,dY=0,dZ=0):
        self.a_dX = dX
        self.a_dY = dY
        self.a_dZ = dZ
    
    #Should probably be only run in iterator
    #Will apply the desired accel changes to acceleration
    #Also CLEARS a_dX and a_dY
    def apply_delta_accel(self):
        self.a_x = self.a_x + (self.a_dX * self.timestep)
        self.a_y = self.a_y + (self.a_dY * self.timestep)
        self.a_z = self.a_z + (self.a_dZ * self.timestep)
        self.a_dX = 0
        self.a_dY = 0
        self.a_dZ = 0

    #Will edit position to next value based on velocity
    def apply_vel(self):
        self.x = self.x + (self.v_x * self.timestep)
        self.y = self.y + (self.v_y * self.timestep)
        self.z = self.z + (self.v_z * self.timestep)

    #Will edit velocity to next value based on acceleation
    def apply_accel(self):
        self.v_x = self.v_x + (self.a_x * self.timestep)
        self.v_y = self.v_y + (self.a_y * self.timestep)
        self.v_z = self.v_z + (self.a_z * self.timestep)

    #Takes min/max for x & y, will edit position of drone to anywhere inside the map
    #Visual of expected list: [ min X , min Y , min Z, max X, max Y, max Z ]
    def randomize_pos(self,drone_map):
        self.x = np.random.randint(drone_map[0],drone_map[3]+1)
        self.y = np.random.randint(drone_map[1],drone_map[4]+1)
        self.z = np.random.randint(drone_map[2],drone_map[5]+1)
    
    def randomize_vel(self,min_vel,max_vel):
        self.v_x = min_vel + (np.random.rand() * (max_vel-min_vel))
        self.v_y = min_vel + (np.random.rand() * (max_vel-min_vel))
        self.v_z = min_vel + (np.random.rand() * (max_vel-min_vel))

    #Will run everything through one iteration 
    def iterate(self):
        self.apply_accel()
        self.apply_vel()
        self.apply_delta_accel() 

