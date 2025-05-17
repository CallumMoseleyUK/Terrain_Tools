import matplotlib.pyplot as plt
from matplotlib import cm
from fractal import TerrainGenerator

def plot_terrain(self,scale):
    #plt.style.use('dark_background')
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 8), constrained_layout=True)
    ax.plot_surface(self.x_mesh, self.y_mesh, self.height_mesh, rstride=1, cstride=1, antialiased=False, cmap=cm.terrain)
    ax.set_box_aspect((1, 1, scale))
    plt.axis('off')

if __name__ == '__main__':
    seed = 137
    max_iter = 7
    mesh_size = 257
    terrain_generator = TerrainGenerator(max_iter,mesh_size)
    terrain_generator.initialize(seed)
    terrain_generator.run()

    
    terrain_generator.plot_terrain(0.4)
    plt.show()