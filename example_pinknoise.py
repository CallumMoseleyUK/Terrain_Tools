import numpy as np
import matplotlib.pyplot as plt
from noise import *
import time
from matplotlib import cm
from PIL import Image

def plot_terrain(T,scale):
    X,Y,Z = T
    #plt.style.use('dark_background')
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 8), constrained_layout=True)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, antialiased=False, cmap=cm.terrain)
    ax.set_box_aspect((1, 1, scale))
    plt.axis('off')

if __name__ == '__main__':

    seed = 137
    roughness = 1.0
    bParallel=False
    sizes = np.array(
        [512]
        )
    times = np.zeros(sizes.shape)
    for i,size in enumerate(sizes):
        start_time = time.time()
        T0 = generate_noise_map(seed=seed, size=size, roughness=roughness, bParallel=bParallel)
        end_time = time.time()
        exec_time = end_time-start_time
        times[i] = exec_time
        print('Execution time: ', exec_time)
        if i==0:
            TPlot = T0

    image = Image.fromarray(np.float64(T0[2])*255.0)
    plt.figure()
    plt.imshow(image, cmap='gray')

    plt.figure()
    plt.plot(sizes,times)

    polyfit = np.polyfit(sizes,times,2)
    print('%1.2f + %1.2fx + %1.2fx^2' % tuple(p for p in polyfit))
    plot_terrain(TPlot,1/4)

    plt.show()