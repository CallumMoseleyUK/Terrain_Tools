
#https://en.wikipedia.org/wiki/Wavefront_.obj_file
import numpy as np
from datetime import datetime
from fractal import interpolate
from scipy.spatial import Delaunay

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

def make_faces2(Nr,Nc):
    Nfaces=(Nr-1)*(Nc-1)*2
    Faces=np.zeros((Nfaces,3),dtype=np.int32)
    for r in range(Nr-1):
        for c in range(Nc-1):
            fi=(r*(Nc-1)+c)*2
            l1=r*Nc+c
            l2=l1+1
            l3=l1+Nc
            l4=l3+1
            Faces[fi]=[l1,l2,l3]
            Faces[fi+1]=[l2,l4,l3]
    return Faces

def make_faces3(Nr,Nc):
    m = np.arange(Nr * Nc).reshape(Nr, Nc)
    c1 = np.concatenate((m[:-1, :-1].ravel(), m[1:, 1:].ravel()))
    c2 = np.concatenate((m[:-1, 1:].ravel(), m[:-1, 1:].ravel()))
    c3 = np.concatenate((m[1:, :-1].ravel(), m[1:, :-1].ravel()))
    faces = list(zip(c1, c2, c3))
    return faces

def make_faces4(x,y,z):
    hull = Delaunay(np.array([x,y,z]).T)
    faces = []
    for simplex in hull.simplices:
        faces.append([simplex[0],simplex[1],simplex[2]])
        faces.append([simplex[0],simplex[1],simplex[3]])
        
    return faces

def make_faces5(Nr,Nc):
    #https://github.com/ryobg/obj2hmap/blob/master/hmap2obj.cpp
    faces = []
    #for i in range(2,Nr*Nc-Nr+1):
    for i in range(4,Nr*Nc-Nr-2):
        if i%Nr:
            # v1 = i+1
            # v2 = i
            # v3 = i+Nr
            # faces.append([v1,v2,v3])
            # v1 = i+Nr
            # v2 = i+Nr+1
            # v3 = i+1
            # faces.append([v1,v2,v3])
            v1 = i+1
            v2 = i
            v3 = i+Nr
            faces.append([v3,v2,v1])
            v2 = i+Nr
            v3 = i+Nr+1
            faces.append([v3,v2,v1])

    return faces



def quad2tri(x_mesh,y_mesh,z_mesh):
    mesh_width,mesh_height = x_mesh.shape
    vertices = []
    faces = []
    normals = []
    texcoords = []

    x = x_mesh.flatten()
    y = y_mesh.flatten()
    z = z_mesh.flatten()
    #xyz_flat = np.array([x[faces].flatten(),y[faces].flatten(),z[faces].flatten()]).T
    #vertices = list(xyz_flat)
    xyz_flat = np.array([x,y,z]).T
    vertices = list(xyz_flat)
    faces = make_faces5(mesh_width,mesh_height)
    #faces = list(np.array(faces)+1)

    # for i in range(mesh_width):
    #     for j in range(mesh_height):
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
