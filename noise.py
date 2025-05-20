import numpy as np

_numpy_height_dtype = np.float32

def pink_noise(seed, size, roughness):
    rng = np.random.default_rng(seed)
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
