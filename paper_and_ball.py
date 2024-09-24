import bpy
from math import radians
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'  # For NVIDIA GPUs
# Uncomment the following line for OptiX if your GPU supports it (RTX cards):
# bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'OPTIX'

# Set the devices for rendering (assuming you're using a single GPU)
bpy.context.preferences.addons['cycles'].preferences.get_devices()

# Enable GPU rendering for the scene
bpy.context.scene.cycles.device = 'GPU'

# Set up Cycles rendering settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'  # For displacement

# Ensure the GPU is selected
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    if device.type == 'CUDA' or device.type == 'OPTIX':
        device.use = True

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


#bpy.ops.mesh.primitive_cube_add()

#so = bpy.context.active_object
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
paper = bpy.context.active_object
paper.name = "Paper"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=50)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='CLOTH')
cloth_modifier = paper.modifiers['Cloth']

cloth_modifier.settings.quality = 5  # Higher for more realistic crumbling
cloth_modifier.settings.mass = 0.1
cloth_modifier.settings.tension_stiffness = 5  # Control how the paper behaves (crumple stiffness)
cloth_modifier.settings.compression_stiffness = 50  # Higher for crumbling behavior
cloth_modifier.settings.bending_stiffness = 0.2
cloth_modifier.settings.air_damping = 10  # Makes the paper feel lighter

# Create a Sphere (collision object to crumple the paper)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, enter_editmode=False, align='WORLD', location=(0, 0, 1))
sphere = bpy.context.active_object
sphere.name = "Crumple_Sphere"

# Add Collision physics to the sphere
bpy.ops.object.modifier_add(type='COLLISION')
collision_modifier = sphere.modifiers['Collision']

# Animate the Sphere to pass through the paper and crumple it
sphere.location = (0, 0, 2)
sphere.keyframe_insert(data_path="location", frame=1)
sphere.location = (0, 0, -1)
sphere.keyframe_insert(data_path="location", frame=50)

# Add a Force Field (Turbulence) for extra crumple effect
bpy.ops.object.effector_add(type='TURBULENCE', enter_editmode=False, align='WORLD', location=(0, 0, 2))
turbulence = bpy.context.active_object
turbulence.field.strength = 30  # You can adjust this for stronger crumple
turbulence.field.size = 0.5  # Affects the scale of the turbulence

# Bake the cloth simulation
bpy.context.view_layer.objects.active = paper
bpy.ops.ptcache.free_bake_all()
bpy.ops.ptcache.bake_all(bake=True)

# Set the end frame to fit the animation length
bpy.context.scene.frame_end = 100

