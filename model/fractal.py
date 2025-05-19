#https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/39559/versions/3/previews/html/terrain_generation_introduction.html
import numpy as np
from scipy.interpolate import griddata
import time

def interpolate(x_old,y_old,z_old,x_new,y_new):
    # add flat points around the map, so when points are extrapolated they will tend towards 0, keeping them bounded and "terrain-like".
    x_padded = np.concatenate((100*np.array([-1, -1, 1, 1]),x_old))
    y_padded = np.concatenate((100*np.array([-1, 1, -1, 1]),y_old))
    z_padded = np.concatenate((np.zeros(4),z_old))
    return griddata((x_padded,y_padded),z_padded,(x_new,y_new),method='linear')

class TerrainGenerator:
    def __init__(self,max_iter,mesh_size,h0=0.1,r0=0.1,rr=0.05):
        '''
        max_iter: Number of iterations to calculate
        mesh_size: Mesh size, should be power of 2 plus 1. Automatically fitted to nearest valid value if not.
        h0=0.0: Initial elevation
        r0=0.1: Initial roughness
        rr=0.05: Initial roughness-roughness (roughness variance per step)
        '''
        self.max_iter = int(np.floor(max_iter))
        self.mesh_size = self.sanitize_mesh_size(mesh_size)
        self.h0 = h0
        self.r0 = r0
        self.rr = rr
    
    def initialize(self,seed):
        self.rng = np.random.default_rng(seed)
        self.num_init_points = self.rng.integers(1,5+1)
        self.growth_rate = 3 #how many points grow from each old point
        self.total_points = self.num_init_points * (self.growth_rate+1)**self.max_iter
        # Initial coordinates
        self.x = np.concatenate(
            (self.rng.normal(size=self.num_init_points),
            np.zeros(self.total_points - self.num_init_points))
        )
        self.y = np.concatenate(
            (self.rng.normal(size=self.num_init_points),
            np.zeros(self.total_points - self.num_init_points))
        )
        # Initial elevations
        self.h = np.concatenate(
            (self.r0 * self.rng.normal(size=self.num_init_points) + self.h0,
            np.zeros(self.total_points - self.num_init_points))
        )
        # Initial roughness
        self.r = np.concatenate(
            (self.rr * self.rng.normal(size=self.num_init_points) + self.h0,
            np.zeros(self.total_points - self.num_init_points))
        )
        


    def sanitize_mesh_size(self,mesh_size):
        ''' Ensure mesh size is power of 2 plus one, e.g. 513'''
        return int(2**(np.floor(np.log2(np.abs(mesh_size)))) + 1)
    

    def run(self):
        print('Generating geometry...')
        self.num_points = self.num_init_points
        for iter in range(1,self.max_iter+1):
            print('Iteration: %i, Points: %i' % (iter,self.num_points))
            start_time = time.time()

            # Calculate new variance for x, y, h and r
            dxy = 0.75**iter
            dh = 0.5**iter

            # Number of new points to generate
            n_new = self.growth_rate * self.num_points

            # Parents for new points
            # TODO: beware the row/column dimensions of this one. Should tile to a matrix, reshape to a vector.
            parents = np.reshape(
                np.tile(
                    np.arange(0,self.num_points),(self.growth_rate,1)),(1,n_new)
                    )
            
            # Calculate indices for new and existing points
            new_indices = np.arange(self.num_points,self.num_points+n_new)
            old_indices = np.arange(0,self.num_points)

            # Calculate new x/y values
            theta = 2*np.pi * self.rng.uniform(size=n_new)
            radius = dxy * (self.rng.uniform(size=n_new) + 1)
            self.x[new_indices] = self.x[parents] + radius * np.cos(theta)
            self.y[new_indices] = self.y[parents] + radius * np.sin(theta)

            # Interpolate for new roughness and elevation values with noise
            interpolated_r = interpolate(self.x[old_indices],
                                              self.y[old_indices],
                                              self.r[old_indices],
                                              self.x[new_indices],
                                              self.y[new_indices])
            interpolated_h = interpolate(self.x[old_indices],
                                              self.y[old_indices],
                                              self.h[old_indices],
                                              self.x[new_indices],
                                              self.y[new_indices])
            self.r[new_indices] = interpolated_r + dh*self.rr*self.rng.normal(size=n_new)
            self.h[new_indices] = interpolated_h + (dh/dxy)*radius*self.r[new_indices] * self.rng.normal(size=n_new)
            self.num_points = self.num_points + n_new

            print('time = %1.5f' % (time.time()-start_time))

        # Normalize map and create mesh
        print('Normalizing and meshing...')
        self.normalize_distribution()
        print('Generation finished.')

    def normalize_distribution(self):
        self.x = (self.x-np.median(self.x))/np.std(self.x)
        self.y = (self.y-np.median(self.y))/np.std(self.y)
        self.x_mesh,self.y_mesh = np.meshgrid(np.linspace(-1.0,1.0, self.mesh_size),
                                            np.linspace(-1.0,1.0, self.mesh_size))
        self.height_mesh = interpolate(self.x,self.y,self.h,self.x_mesh,self.y_mesh)

    def get_height(self,x,y):
        return interpolate(self.x,self.y,self.h,x,y)
        