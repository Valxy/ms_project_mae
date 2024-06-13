import bpy

obj_file = "/Users/valentina/Documents/UCSC Grad Courses/3D face reconstruction/blender_script/F1001.obj"
color_texture = "/Users/valentina/Documents/UCSC Grad Courses/3D face reconstruction/blender_script/textures/L0.jpg"
roughness_texture = bpy.data.images.load("/Users/valentina/Documents/UCSC Grad Courses/3D face reconstruction/blender_script/textures/roughness.png")
subsurface_map = bpy.data.images.load("/Users/valentina/Documents/UCSC Grad Courses/3D face reconstruction/blender_script/textures/subsurface.png")
normal_map = bpy.data.images.load("/Users/valentina/Documents/UCSC Grad Courses/3D face reconstruction/blender_script/textures/L0_normals.png")

# Import the OBJ file
bpy.ops.import_scene.obj(filepath=obj_file)

# Get the imported object
obj = bpy.context.selected_objects[0]


# Set the material index you want to assign the texture to (0 for the first material)
material_index = 0

# Load the image texture
image_texture = bpy.data.images.load(color_texture)


# Ensure the object has a material (create one if it doesn't)
if len(obj.data.materials) <= material_index:
    bpy.ops.object.material_slot_add()
    
# Assign the image texture to the selected material
material = obj.data.materials[material_index]
if material.node_tree is None:
    material.use_nodes = True
    material.node_tree = bpy.data.node_groups.new(name="Material Node Tree", type='ShaderNodeTree')

material.node_tree.nodes["Principled BSDF"].inputs[7].default_value=0

# Create an image texture node
image_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
image_texture_node.location = (-300, 400)  # Set the location of the node

roughness_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
roughness_texture_node.location = (-700, 0)  # Adjust the node location

subsurface_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
subsurface_node.location = (-300, 100)

normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')
normal_map_node.location = (-200, -200)

normal_map_img_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
normal_map_img_node.location = (-500, -300)

# Link the image texture to the base color input of the principled shader
material.node_tree.links.new(
    image_texture_node.outputs["Color"],
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
)

# Link the roughness map to the roughness input of the Principled BSDF shader
material.node_tree.links.new(
    roughness_texture_node.outputs["Color"],
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"]
)

material.node_tree.links.new(
    subsurface_node.outputs["Color"],
    material.node_tree.nodes["Principled BSDF"].inputs["Subsurface"]
)

material.node_tree.links.new(
    normal_map_node.outputs["Normal"],
    material.node_tree.nodes["Principled BSDF"].inputs["Normal"]
)

material.node_tree.links.new(
    normal_map_img_node.outputs["Color"],
    material.node_tree.nodes["Normal Map"].inputs["Color"]
)

# Set the image texture to use your loaded texture
image_texture_node.image = image_texture
roughness_texture_node.image = roughness_texture
subsurface_node.image = subsurface_map
normal_map_img_node.image = normal_map