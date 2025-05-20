import matplotlib.pyplot as plt
from fractal import TerrainGenerator
import sys
import os
from WizardQuest.game import Game
from WizardQuest.entities.entity import Entity
from utils.render import *
from utils.format import *

submodule_name = 'WizardQuest'
(parent_folder_path, current_dir) = os.path.split(os.path.dirname(__file__))
sys.path.append(os.path.join(parent_folder_path, submodule_name))


if __name__ == '__main__':
    seed = None
    max_iter = 5 #12 = 6000sec, 11 = 700sec, 10 = 75sec
    mesh_size = 128
    r0 = 0.1
    rr = 0.05
    scale = 0.2
    obj_file = 'WizardQuest/data/terrain.obj'

    terrain_generator = TerrainGenerator(max_iter,mesh_size,r0=r0,rr=rr)
    terrain_generator.initialize(seed)
    terrain_generator.run()

    # Export to obj format
    X,Y,Z = terrain_generator.x_mesh,terrain_generator.y_mesh,terrain_generator.z_mesh
    vertices,faces,normals,texcoords = quad2tri(X,Y,Z)
    verts2obj(obj_file,vertices,faces,normals,texcoords)

    ## Render result
    mesh_path = 'data/terrain.obj'
    texture_path = None
    shader_paths = [ r'data\shaders\terrain_vert.glsl', r'data\shaders\terrain_frag.glsl' ]
    
    game = Game()
    ent = Entity()
    ent.add_render_model(game.asset_manager.load_render_model(mesh_path,texture_path=texture_path,shader_paths=shader_paths))
    ent.position = [3.0,0.0,-2]
    game.world.spawn_entity(ent)
    game.run()

    #make_gif(np.arange(1,9),seed,terrain_generator,scale)

    #image = Image.fromarray(np.float64(terrain_generator.z_mesh)*255.0)
    #plt.figure()
    #plt.imshow(image, cmap='gray')

    # plot_terrain(terrain_generator.x_mesh,
    #              terrain_generator.y_mesh,
    #              terrain_generator.z_mesh,scale,min_height=-100)
    # plt.show()

