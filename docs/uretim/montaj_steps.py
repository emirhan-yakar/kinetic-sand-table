# ============================================================================
#  IKEA tarzi montaj adimlari - kumulatif assembly render (Blender Workbench)
#  Her adim: o ana kadarki parcalar gri, YENI parca turuncu vurgulu. step1..7.png
#  Calistir: Blender --background --python montaj_steps.py
# ============================================================================
import bpy, os
from mathutils import Vector
HERE=os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else \
     "/Users/emirhanyakar/Desktop/design_sale/docs/uretim"
GLB="/Users/emirhanyakar/Desktop/design_sale/render/table.glb"
RES=(1200,1000)

# adim -> bu adimda EKLENEN parca prefixleri
STEPS=[
 ["BasePlate","Theta_Motor","theta_shaft","Arm","Rho_Motor"],   # 1 mekanizma
 ["Carriage","Magnet"],                                          # 2 tasiyici+miknatis
 ["PCB"],                                                         # 3 kontrol karti
 ["Body"],                                                        # 4 govde
 ["Legs"],                                                        # 5 ayaklar
 ["LED_Ring","Sand","Groove","Ball","Rim"],                       # 6 LED + kum
 ["Glass"],                                                       # 7 cam ust
]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
bpy.ops.import_scene.gltf(filepath=GLB)
meshes=[o for o in scene.objects if o.type=='MESH']
def step_of(name):
    for i,s in enumerate(STEPS):
        if any(name.startswith(p) for p in s): return i
    return 99

# kamera (tum masayi cerceveler, 3/4)
cam_d=bpy.data.cameras.new("C"); cam_d.lens=52
cam=bpy.data.objects.new("C",cam_d); scene.collection.objects.link(cam); scene.camera=cam
cam.location=(1.25,-1.12,0.78); d=Vector((0,0,0.22))-Vector(cam.location)
cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()

# Workbench teknik gorunum, OBJECT renk (vurgu icin)
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading
sh.light='STUDIO'; sh.color_type='OBJECT'; sh.show_object_outline=True
sh.object_outline_color=(0.06,0.06,0.08); sh.show_cavity=True; sh.cavity_type='WORLD'
scene.render.film_transparent=True   # seffaf zemin -> PDF'te beyaza bindirilir
scene.display.render_aa='16'
scene.world=bpy.data.worlds.new("W"); scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs[0].default_value=(1,1,1,1)
scene.view_settings.view_transform='Standard'
scene.render.resolution_x,scene.render.resolution_y=RES
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'

GRAY=(0.82,0.82,0.85,1); NEW=(1.0,0.5,0.05,1)
for i in range(len(STEPS)):
    for o in meshes:
        s=step_of(o.name)
        o.hide_render = (s>i)            # gelecek parcalar gizli
        o.color = NEW if s==i else GRAY  # yeni parca turuncu
    scene.render.filepath=os.path.join(HERE,f"step{i+1}.png")
    bpy.ops.render.render(write_still=True)
    print("step",i+1,"render edildi")
print("BITTI")
