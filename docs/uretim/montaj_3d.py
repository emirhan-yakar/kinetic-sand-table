# ============================================================================
#  Profesyonel/IKEA tarzi PATLATILMIS montaj cizimi (Blender Workbench)
#  table.glb'yi yukler, parcalari ayirir, temiz teknik render uretir +
#  numarali callout'lar icin her parcanin 2D ekran konumunu JSON'a yazar.
#  Calistir: Blender --background --python montaj_3d.py
#  Sonra: python3 montaj_label.py  (numara+aciklama bindirir)
# ============================================================================
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

HERE=os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else \
     "/Users/emirhanyakar/Desktop/design_sale/docs/uretim"
GLB="/Users/emirhanyakar/Desktop/design_sale/render/table.glb"
OUT=os.path.join(HERE,"montaj_patlatma_raw.png")
RES=(1500,1100)

# patlatma ofsetleri (Blender Z-yukari, metre) + numara/aciklama
PART={
 "Glass":      (( 0,0, 0.24), 1,"Temperli cam Ø552×6"),
 "Rim":        (( 0,0, 0.15), 2,"Üst ahşap çerçeve"),
 "Ball":       (( 0,0, 0.31), 3,"Çelik bilye Ø12"),
 "LED_Ring":   (( 0,0, 0.10), 4,"LED halka (WS2812B)"),
 "Sand":       (( 0,0, 0.05), 5,"Kum + desen"),
 "Groove":     (( 0,0, 0.05), None,None),
 "Body":       (( 0,0, 0.00), 6,"Ahşap gövde (drum)"),
 "Arm":        (( 0,0,-0.07), 7,"Dönen kol (θ)"),
 "Rho_Motor":  (( 0.14,0,-0.07), 8,"ρ motoru (NEMA17)"),
 "Carriage":   (( 0.07,0,-0.05), 9,"Taşıyıcı + mıknatıs"),
 "Magnet":     (( 0.07,0,-0.03), None,None),
 "Theta_Motor":(( 0,0,-0.13), 10,"θ motoru (NEMA17)"),
 "theta_shaft":(( 0,0,-0.11), None,None),
 "BasePlate":  (( 0,0,-0.18), 11,"Alüminyum şasi"),
 "PCB":        (( 0.22,0,-0.18), 12,"Kontrol kartı (ESP32+TMC)"),
 "Legs":       (( 0,0,-0.16), 13,"Ayaklar (4×, 8° splay)"),
}

# temiz sahne + glb
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
bpy.ops.import_scene.gltf(filepath=GLB)

# parcalari ayir
def off_for(n):
    for k,v in PART.items():
        if n.startswith(k): return v[0]
    return (0,0,0)
for ob in list(scene.objects):
    if ob.type=='MESH':
        ox,oy,oz=off_for(ob.name)
        ob.location=(ob.location.x+ox, ob.location.y+oy, ob.location.z+oz)

# kamera (patlamis yigini cerceveler)
cam_d=bpy.data.cameras.new("C"); cam_d.lens=62
cam=bpy.data.objects.new("C",cam_d); scene.collection.objects.link(cam); scene.camera=cam
cam.location=(1.55,-1.35,0.95);
tgt=Vector((0,0,0.30)); d=tgt-Vector(cam.location)
cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()

# Workbench: temiz teknik gorunum (clay + kontur + cavity, beyaz zemin)
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading
sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.82,0.82,0.84)
sh.show_object_outline=True; sh.object_outline_color=(0.08,0.08,0.10)
sh.show_cavity=True; sh.cavity_type='WORLD'
scene.display.render_aa='16'
scene.world=bpy.data.worlds.new("W"); scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs[0].default_value=(1,1,1,1)
scene.view_settings.view_transform='Standard'
scene.render.film_transparent=False
scene.render.resolution_x,scene.render.resolution_y=RES
scene.render.image_settings.file_format='PNG'
scene.render.filepath=OUT

# her numarali parcanin 2D ekran konumu (callout icin)
bpy.context.view_layer.update()
labels=[]
done=set()
for ob in scene.objects:
    if ob.type!='MESH': continue
    for k,v in PART.items():
        if ob.name.startswith(k) and v[1] and k not in done:
            co=world_to_camera_view(scene,cam,ob.matrix_world.translation)
            labels.append({"no":v[1],"text":v[2],"x":co.x*RES[0],"y":(1-co.y)*RES[1]})
            done.add(k)
labels.sort(key=lambda l:l["no"])
json.dump({"img":os.path.basename(OUT),"res":RES,"labels":labels},
          open(os.path.join(HERE,"montaj_patlatma_labels.json"),"w"),ensure_ascii=False,indent=1)

print("RENDER ->",OUT)
bpy.ops.render.render(write_still=True)
print("BITTI; etiket sayisi:",len(labels))
