# ============================================================================
#  MEKANIZMA patlatilmis gorunum (yakin) - sadece tahrik bilesenleri, net.
#  table.glb'den kabugu siler, mekanizmayi patlatir, zoom render + json.
#  Blender --background --python mekanizma_patlatma.py ; sonra montaj_label.py
# ============================================================================
import bpy, os, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else \
     "/Users/emirhanyakar/Desktop/design_sale/docs/uretim"
GLB="/Users/emirhanyakar/Desktop/design_sale/render/table.glb"
OUT=os.path.join(HERE,"mekanizma_patlatma_raw.png"); RES=(1500,1100)

# mekanizma parcalari: prefix -> (patlatma ofset z+yan, no, etiket)
PART={
 "BasePlate":   ((0,0,-0.10), 1,"Şasi plakası (Al 4mm)"),
 "PCB":         ((0.05,0,-0.10), 8,"Kontrol kartı (ESP32+TMC)"),
 "Theta_Motor": ((0.02,0,-0.04), 2,"θ motoru (NEMA17)"),
 "theta_shaft": ((0,0,0.015), 3,"Turntable + slip ring + θ kasnak"),
 "Arm":         ((0,0,0.085), 4,"Dönen kol + MGN12 ray"),
 "Carriage":    ((0,0,0.14), 5,"Taşıyıcı (MGN12H araba)"),
 "Magnet":      ((0,0,0.185), 6,"N52 mıknatıs"),
 "Rho_Motor":   ((0,0,0.075), 7,"ρ motoru (NEMA17, kolda)"),
}
KEEP=set(PART)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
bpy.ops.import_scene.gltf(filepath=GLB)
def part_of(n):
    for k in PART:
        if n.startswith(k): return k
    return None
# kabugu sil, mekanizmayi patlat
for ob in list(scene.objects):
    if ob.type!='MESH': continue
    k=part_of(ob.name)
    if k is None: bpy.data.objects.remove(ob,do_unlink=True)
    else:
        ox,oy,oz=PART[k][0]; ob.location=(ob.location.x+ox,ob.location.y+oy,ob.location.z+oz)

mesh=[o for o in scene.objects if o.type=='MESH']
# bbox merkez+boyut
cos=[o.matrix_world@Vector(c) for o in mesh for c in o.bound_box]
mn=Vector((min(c.x for c in cos),min(c.y for c in cos),min(c.z for c in cos)))
mx=Vector((max(c.x for c in cos),max(c.y for c in cos),max(c.z for c in cos)))
ctr=(mn+mx)/2; size=(mx-mn).length
# kamera (3/4, bbox'a gore)
cam_d=bpy.data.cameras.new("C"); cam_d.lens=58
cam=bpy.data.objects.new("C",cam_d); scene.collection.objects.link(cam); scene.camera=cam
cam.location=ctr+Vector((size*0.9,-size*0.85,size*0.65))
dd=ctr-Vector(cam.location); cam.rotation_euler=dd.to_track_quat('-Z','Y').to_euler()

# Workbench temiz teknik
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading; sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.80,0.81,0.84)
sh.show_object_outline=True; sh.object_outline_color=(0.07,0.07,0.09); sh.show_cavity=True; sh.cavity_type='WORLD'
scene.display.render_aa='16'; scene.render.film_transparent=False
scene.world=bpy.data.worlds.new("W"); scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs[0].default_value=(1,1,1,1)
scene.view_settings.view_transform='Standard'
scene.render.resolution_x,scene.render.resolution_y=RES
scene.render.image_settings.file_format='PNG'; scene.render.filepath=OUT

bpy.context.view_layer.update()
labels=[]; done=set()
for o in mesh:
    k=part_of(o.name)
    if k and k not in done:
        co=world_to_camera_view(scene,cam,o.matrix_world.translation)
        labels.append({"no":PART[k][1],"text":PART[k][2],"x":co.x*RES[0],"y":(1-co.y)*RES[1]}); done.add(k)
labels.sort(key=lambda l:l["no"])
def proj(z):
    co=world_to_camera_view(scene,cam,Vector((ctr.x,ctr.y,z))); return [co.x*RES[0],(1-co.y)*RES[1]]
axis=[proj(mx.z+0.03),proj(mn.z-0.03)]
json.dump({"img":os.path.basename(OUT),"res":RES,"labels":labels,"axis":axis,"title":"MEKANİZMA — PATLATILMIŞ"},
          open(os.path.join(HERE,"mekanizma_patlatma_labels.json"),"w"),ensure_ascii=False,indent=1)
bpy.ops.render.render(write_still=True); print("MEK BITTI",len(labels))
