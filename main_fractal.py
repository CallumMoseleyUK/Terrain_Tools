import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import numpy as np
from model.fractal import TerrainGenerator
import io

def plot_terrain(terrain,scale,min_height=-1000):
    #plt.style.use('dark_background')
    height_mesh = terrain.height_mesh
    I = np.where(height_mesh<min_height)
    height_mesh[I] = np.zeros(height_mesh[I].shape)
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 8), constrained_layout=True)
    ax.plot_surface(terrain.x_mesh, terrain.y_mesh, height_mesh, rstride=1, cstride=1, antialiased=False, cmap=cm.terrain)
    ax.set_box_aspect((1, 1, scale))
    plt.axis('off')
    return fig

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def make_gif(max_iters,seed,terrain,scale):
    frames = []
    for max_iter in max_iters:
        terrain_generator.max_iter = max_iter
        terrain_generator.initialize(seed)
        terrain_generator.run()
        fig = plot_terrain(terrain_generator,scale)
        frame = fig2img(fig)
        frames.append(frame)
    frames[0].save("animation.gif", save_all=True, append_images=frames[1:], duration=300, loop=0)

if __name__ == '__main__':
    seed = 137
    max_iter = 7
    mesh_size = 257
    r0 = 0.1
    rr = 1.0
    scale = 0.4

    terrain_generator = TerrainGenerator(max_iter,mesh_size,r0=r0,rr=rr)
    terrain_generator.initialize(seed)
    terrain_generator.run()

    #make_gif(np.arange(1,9),seed,terrain_generator,scale)

    image = Image.fromarray(np.float64(terrain_generator.height_mesh)*255.0)
    plt.figure()
    plt.imshow(image, cmap='gray')

    plot_terrain(terrain_generator,scale)
    plt.show()