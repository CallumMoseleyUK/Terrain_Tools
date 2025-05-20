import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import numpy as np
import io

def plot_terrain(X,Y,Z,scale,min_height=-1000):
    #plt.style.use('dark_background')
    I = np.where(Z<min_height)
    Z[I] = min_height
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 8), constrained_layout=True)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, antialiased=False, cmap=cm.terrain)
    ax.set_box_aspect((1, 1, scale))
    plt.axis('off')
    return fig

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def make_gif(max_iters,seed,terrain,scale):
    frames = []
    for max_iter in max_iters:
        terrain.max_iter = max_iter
        terrain.initialize(seed)
        terrain.run()
        fig = plot_terrain(terrain.x_mesh,terrain.y_mesh,terrain.z_mesh,scale)
        frame = fig2img(fig)
        frames.append(frame)
    frames[0].save("animation.gif", save_all=True, append_images=frames[1:], duration=300, loop=0)
