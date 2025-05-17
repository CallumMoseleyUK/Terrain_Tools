import numpy as np
import taichi as ti
ti.init(ti.cpu)

_taichi_height_dtype = ti.f16
_numpy_height_dtype = np.float16

@ti.kernel
def _rand_normal(out: ti.template()):
    ti.loop_config(serialize=False,parallelize=4)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i,j] = ti.random(dtype=out.dtype)

def parallel_rand_normal(width,height):
    out = ti.field(dtype=_taichi_height_dtype,shape=(width,height))
    _rand_normal(out)
    return out.to_numpy(dtype=_numpy_height_dtype)

def pink_noise(seed, size, roughness, bParallel=False):
    rng = np.random.default_rng(seed)
    if bParallel:
        white = parallel_rand_normal(size,size)
    else:
        white = _numpy_height_dtype(rng.normal(size=(size, size)))
        
    white_ft = np.fft.fftshift(np.fft.fft2(white))

    hsize = size / 2
    y, x = np.ogrid[-hsize:hsize, -hsize:hsize]
    freq = (x**2 + y**2) ** (1 / roughness)
    pink_ft = np.divide(white_ft, freq,
      out=np.zeros_like(white_ft), where=freq!=0)

    pink = np.fft.ifft2(np.fft.ifftshift(pink_ft)).real
    lo, hi = np.min(pink), np.max(pink)
    return (pink - lo) / (hi - lo)

def generate_noise_map(seed, size, roughness=1.0, bParallel=False):
    Z = pink_noise(seed, size, roughness, bParallel=bParallel)
    Y, X = np.ogrid[0:size, 0:size]
    return X,Y,_numpy_height_dtype(Z)
