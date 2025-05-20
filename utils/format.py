
#https://en.wikipedia.org/wiki/Wavefront_.obj_file
import numpy as np
from datetime import datetime
from fractal import interpolate

def make_faces(Nr,Nc):

    out = np.empty((Nr-1,Nc-1,2,3),dtype=int)

    r = np.arange(Nr*Nc).reshape(Nr,Nc)

    out[:,:, 0,0] = r[:-1,:-1]
    out[:,:, 1,0] = r[:-1,1:]
    out[:,:, 0,1] = r[:-1,1:]

    out[:,:, 1,1] = r[1:,1:]
    out[:,:, :,2] = r[1:,:-1,None]

    out.shape =(-1,3)
    return out

def quad2tri(x_mesh,y_mesh,z_mesh):
    mesh_width,mesh_height = x_mesh.shape
    vertices = []
    faces = make_faces(mesh_width,mesh_height)
    normals = []
    texcoords = []

    x = x_mesh.flatten()
    y = y_mesh.flatten()
    z = z_mesh.flatten()
    #xyz_flat = np.array([x[faces].flatten(),y[faces].flatten(),z[faces].flatten()]).T
    #vertices = list(xyz_flat)
    xyz_flat = np.array([x,y,z]).T
    vertices = list(xyz_flat)

    # for i in range(width-1):
    #     for j in range(height-1):
    #         a = i * height + j + 1
    #         b = i * height + (j+1) + 1
    #         c = (i+1) * height + j + 1
    #         d = (i+1) * height + (j+1) + 1
    #         faces.append((a, b, d, c))

    # for i in range(width):
    #     for j in range(height):
    #         normals.append((0.0,1.0,0.0))

    return vertices,faces,normals,texcoords

def verts2obj(filename,vertices,faces,normals,texcoords):
    file = open(filename,'w')
    file.write('# Terrain_Tools heightmap OBJ file %s\n' % datetime.now())
    for v in vertices:
        file.write('v%s\n' % (' %1.8f'*len(v)) % tuple(v))
    for f in faces:
        file.write('f%s\n' % (' %i'*len(f)) % tuple(f))
    for n in normals:
        file.write('vn%s\n' % (' %1.8f'*len(n)) % tuple(n))
    for t in texcoords:
        file.write('vt%s\n' % (' %1.8f'*len(t)) % tuple(t))
    file.write('s 1\n')
    file.close()
