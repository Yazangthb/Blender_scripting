
import bpy
import random

# Delete all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Step 1: Load the image and get its aspect ratio
random_im = random.randint(1, 99)
image_path = fr"E:\blend\test_images\test_images\{random_im}.jpeg"  # Update this with your image path
image = bpy.data.images.load(image_path)

# Get image dimensions
img_width = image.size[0]
img_height = image.size[1]

# Calculate the aspect ratio of the image
aspect_ratio = img_width / img_height

# Step 2: Create a thin plane (paper-like object)
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 5))
paper = bpy.context.object

# Step 3: Scale the plane based on the image's aspect ratio
paper_width = 1  # You can set the width you want, or keep it as 1 unit
paper_height = paper_width / aspect_ratio
paper.scale = (paper_width, paper_height, 0.01)  # The Z scale remains thin to resemble paper

# Step 4: Subdivide the plane to give it more vertices (for smooth bending)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=7)
bpy.ops.object.mode_set(mode='OBJECT')

# Step 5: Randomly move vertices to simulate bending
mesh = paper.data

for vertex in mesh.vertices:
    vertex.co.z += random.uniform(-1, 1)  # Z axis random movement (bending)
    vertex.co.x += random.uniform(-0.02, 0.02)  # Slight X-axis movement
    vertex.co.y += random.uniform(-0.02, 0.02)  # Slight Y-axis movement

mesh.update()

# Step 6: Optionally, smooth the shading
bpy.ops.object.shade_smooth()
#mode_d=paper.modifiers.new("ds",'DISPLACE')
# Step 7: Create a new material
material = bpy.data.materials.new(name="PaperMaterial")
material.use_nodes = True  # Use the node system for more flexibility

# Step 8: Get the nodes of the material
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add Principled BSDF Shader
bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
bsdf_node.location = (0, 0)

# Add Material Output node
output_node = nodes.new(type="ShaderNodeOutputMaterial")
output_node.location = (300, 0)

# Link BSDF to Material Output
links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

# Step 9: Add an image texture node
texture_node = nodes.new(type="ShaderNodeTexImage")
texture_node.location = (-300, 0)

# Assign the image to the texture node
texture_node.image = image

# Step 10: Link the texture to the Base Color of the BSDF
links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])

# Step 11: Assign the material to the paper object
if paper.data.materials:
    paper.data.materials[0] = material  # Replace existing material
else:
    paper.data.materials.append(material)  # Add new material

# Step 12: Add a light source
# Add a point light
bpy.ops.object.light_add(type='POINT', radius=1, location=(5, 0, 3))  # Adjust location to right

# Get the light object
light = bpy.context.object

# Set light properties
light.data.energy = 1000  # Increase brightness

# Optionally, change the color of the light
light.data.color = (1, 1, 1)  # White light

# Step 13: Adjust the camera for better view (optional)
# Set the camera position
import bpy
import random

# Step 1: Load a random image for the world texture
random_im = random.randint(1, 99)
world_image_path = fr"E:\chd\illovo_beach_balcony_2k.exr"  # Path to your world texture images
world_image = bpy.data.images.load(world_image_path)

# Step 2: Get the world and use nodes for it
world = bpy.context.scene.world
world.use_nodes = True

# Get the node tree of the world
nodes = world.node_tree.nodes
links = world.node_tree.links

# Clear existing nodes
for node in nodes:
    nodes.remove(node)

# Step 3: Add necessary nodes

# Background Node
background_node = nodes.new(type="ShaderNodeBackground")
background_node.location = (0, 0)

# Environment Texture Node (this will load the image as world texture)
texture_node = nodes.new(type="ShaderNodeTexEnvironment")
texture_node.image = world_image
texture_node.location = (-300, 0)

# Output Node
output_node = nodes.new(type="ShaderNodeOutputWorld")
output_node.location = (300, 0)

# Step 4: Link the nodes
links.new(texture_node.outputs['Color'], background_node.inputs['Color'])
links.new(background_node.outputs['Background'], output_node.inputs['Surface'])

# Optionally, adjust the strength of the background (brightness)
background_node.inputs['Strength'].default_value = 1.0  # Increase or decrease this value as needed
# Add a cube under the paper
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, -0.5))  # Adjust the location as needed
cube = bpy.context.object
bpy.context.view_layer.objects.active = paper

# Add Cloth Physics to the paper
bpy.ops.object.modifier_add(type='CLOTH')
cloth_modifier = paper.modifiers['Cloth']

# Configure the cloth settings
cloth_settings = cloth_modifier.settings
cloth_settings.quality = 5  # Adjust quality for better simulation
cloth_settings.mass = 0.3  # Set mass to a low value to simulate light paper
cloth_settings.bending_stiffness = 5  # Make the paper less stiff (for more realistic bending)
cloth_settings.air_damping = 5  # Damping in air to slow down movement slightly

# Enable collisions for the paper
cloth_collision_settings = cloth_modifier.collision_settings
cloth_collision_settings.use_self_collision = True  # Enable self-collision for better accuracy
bpy.context.view_layer.objects.active = cube
bpy.ops.object.modifier_add(type='COLLISION')
bpy.context.scene.gravity = (0, 0, -10.81)  # Gravity strength, default is Earth-like gravity

bpy.ops.object.camera_add(location=(0, -5, 5))

camera = bpy.context.object
camera.data.lens = 18
camera.rotation_euler = (3.14/4, 0, 0)  # Adjust the rotation to face the object
bpy.context.scene.camera = camera
