
#https://en.wikipedia.org/wiki/Wavefront_.obj_file
import numpy as np
from datetime import datetime

def make_triangle_faces(Nr,Nc):
    #https://github.com/ryobg/obj2hmap/blob/master/hmap2obj.cpp
    faces = []
    #for i in range(2,Nr*Nc-Nr+1):
    for i in range(4,Nr*Nc-Nr-2):
        if i%Nr:
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
    vertices = list(np.array([x,y,z]).T)
    faces = make_triangle_faces(mesh_width,mesh_height)
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
