import numpy as np

class Debris():
    def __init__(self,pos,velocity,frame_time,cam1_com,cam2_com):
        self.velocity = velocity
        self.distance = 0
        self.timelist = [frame_time]
        self.cam1_comlist = [cam1_com]
        self.cam2_comlist = [cam2_com]
        self.positionlist = [pos]
        
    def distance_min(self):
        """ Compute the mean minimal distance computed with the measured position and the velocity

        Returns:
            float: [m] estimation of the minimale distance between the debris and the bottom camera
        """
        distance_min_list = []
        for position in self.positionlist:
            c = position[0]**2 + position[1]**2 + position[2]**2
            b = 2*(self.velocity[0]+self.velocity[1]+self.velocity[2])
            a = 1 #'''(self.velocity[0]**2 + self.velocity[1]**2 + self.velocity[2]**2)'''
            t_min = -b/(2*a)
            #distance_min_list.append(np.sqrt(a*t_min**2+b*t_min+c))
            distance_min_list.append(np.sqrt(c))
        return min(distance_min_list)
        #return (sum(distance_min_list)/len(distance_min_list))
    
    def velocity_calc(self):
        """Computes the speed vector of the debris based on all the previous positions
        """
        '''
        if (len(self.positionlist)<3):
            velocity = (self.positionlist[1]-self.positionlist[0])/(self.timelist[1]-self.timelist[0])
        else:
            x_list = self.positionlist[:,0]
            y_list = self.positionlist[:,1]
            z_list = self.positionlist[:,2]
            t_list = self.timelist
            res_x = stats.linregress(t_list, x_list)
            res_y = stats.linregress(t_list, y_list)
            res_z = stats.linregress(t_list, z_list)
            if ((res_x.rvalue**2 < 0.9)or(res_x.rvalue**2)or(res_x.rvalue**2)):
                print("/!\ Low precision /!\ ")
                print(f"R-squared for the x: {res_x.rvalue**2:.6f}")
                print(f"R-squared for the y: {res_y.rvalue**2:.6f}")
                print(f"R-squared for the z: {res_z.rvalue**2:.6f}")
            velocity(res_x.slope, res_y.slope, res_z.slope)
            '''
        velocity = [0,0,0]
        return(velocity)
         
