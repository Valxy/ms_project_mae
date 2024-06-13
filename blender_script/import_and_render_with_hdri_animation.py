import bpy
import os
import math

# Models should be saved in folder name "models" placed in the same directory of this blender file
blender_directory = os.path.dirname(os.path.abspath(__file__))

enclosed_folder_dir = os.path.dirname(blender_directory)

model_directory = enclosed_folder_dir + "/models"

render_save_directory = enclosed_folder_dir + "/renders"

model_scale = 20

target_frames = 250

models = list()
for model in os.listdir(model_directory):
    if model.endswith(".obj") and model.split('.')[0].isdigit:
        models.append(model)
models = sorted(models, key=lambda f: int(f.split('.')[0]))

num_of_models = len(models)

frames_per_model = math.ceil(target_frames / num_of_models)

actual_frames = frames_per_model * num_of_models

rad_per_model = round((math.pi * 2) / actual_frames, 5)

rad = 0

render_count = 0

for file in models:
    model_filepath = os.path.join(model_directory, file)
    bpy.ops.wm.obj_import(filepath=model_filepath,
                    directory=model_directory,
                      files=[{"name":file, "name":file}])
    bpy.ops.object.shade_smooth()
    bpy.ops.transform.resize(value=(model_scale, model_scale, model_scale),
                            orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            orient_matrix_type='GLOBAL')
    
    for f in range(frames_per_model):
        bpy.data.worlds["World"].node_tree.nodes["Mapping.001"].inputs[2].default_value[2] = rad
        bpy.context.scene.render.filepath = os.path.join(render_save_directory, str(render_count))
        bpy.ops.render.render(animation=False, write_still=True)
        rad += rad_per_model
        render_count += 1  
        
    bpy.context.object.hide_render = True
    
