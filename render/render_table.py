# ============================================================================
#  Kinetik Kum Sanati Masasi - Blender fotogercekci render (Cycles)
#  Calistir:  Blender --background --python render_table.py -- [hero|dark]
#  sand_table.scad olculeriyle (Ø60cm) prosedurel kurulum. Cikti: render/*.png
# ============================================================================
import bpy, math, sys, os
from mathutils import Vector

ARGV = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
MODE = ARGV[0] if ARGV else "hero"        # hero | dark
HERE = os.path.dirname(os.path.abspath(bpy.data.filepath)) or os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.dirname(__file__) if "__file__" in globals() else ".", f"table_{MODE}.png")
OUT  = os.path.join("/Users/emirhanyakar/Desktop/design_sale/render", f"table_{MODE}.png")

# ---- temiz sahne ----
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---- olculer (m) ----
D   = 0.60                 # masa capi
R   = D/2
H   = 0.34                 # govde yuksekligi
GLASS_Z = H
SAND_Z  = H-0.012

def add_cyl(name, r, depth, z, verts=128):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=(0,0,z))
    o=bpy.context.active_object; o.name=name
    bpy.ops.object.shade_smooth()
    return o

def new_mat(name):
    m=bpy.data.materials.new(name); m.use_nodes=True
    return m, m.node_tree.nodes, m.node_tree.links

# =========================== GEOMETRI ===========================
WELL_D=0.05; WELL_R=R*0.90
SAND_TOPZ=H-WELL_D+0.014
# govde (ahsap kabin) -> ust kisma kum havuzu oyulur
body = add_cyl("Body", R, H, H/2)
bpy.ops.mesh.primitive_cylinder_add(radius=WELL_R, depth=WELL_D+0.02, vertices=128,
                                    location=(0,0,H-WELL_D/2+0.01))
well=bpy.context.active_object
mod=body.modifiers.new("well","BOOLEAN"); mod.operation='DIFFERENCE'; mod.object=well
bpy.context.view_layer.objects.active=body; bpy.ops.object.modifier_apply(modifier="well")
bpy.data.objects.remove(well, do_unlink=True)
bpy.context.view_layer.objects.active=body; bpy.ops.object.shade_flat()
# kum diski (havuzun icinde)
sand = add_cyl("Sand", WELL_R*0.985, 0.012, H-WELL_D+0.008, 256)
# cam ust  (hero'da kameradan gizli -> kum deseni net gorunur; dark modda gorunur)
glass= add_cyl("Glass", R*0.92, 0.005, H-0.004)
glass.visible_camera = (MODE=="dark")
# celik bilye
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.009, location=(WELL_R*0.42, WELL_R*0.16, SAND_TOPZ+0.006))
ball=bpy.context.active_object; ball.name="Ball"; bpy.ops.object.shade_smooth()
# LED halka (havuz ust ic kenari)
bpy.ops.mesh.primitive_torus_add(major_radius=WELL_R*0.99, minor_radius=0.004, location=(0,0,H-0.006),
                                 major_segments=180, minor_segments=12)
led=bpy.context.active_object; led.name="LED"; bpy.ops.object.shade_smooth()
# ust kenar ahsap cerceve
bpy.ops.mesh.primitive_torus_add(major_radius=(R+WELL_R)/2, minor_radius=(R-WELL_R)/2, location=(0,0,H),
                                 major_segments=160, minor_segments=20)
rim=bpy.context.active_object; rim.name="Rim"; bpy.ops.object.shade_smooth()
base=rim   # malzeme atamalarinda kullaniliyor

# kenar yumusatma (bevel) govde
m=body.modifiers.new("bev","BEVEL"); m.width=0.003; m.segments=3

# zemin
bpy.ops.mesh.primitive_plane_add(size=8, location=(0,0,0))
floor=bpy.context.active_object; floor.name="Floor"

# =========================== MALZEMELER ===========================
# --- ahsap (koyu ceviz, prosedurel grain) ---
mat,n,l = new_mat("Wood")
bsdf=n["Principled BSDF"]
bsdf.inputs["Roughness"].default_value=0.82      # tam mat
bsdf.inputs["Specular IOR Level"].default_value=0.25
tc=n.new("ShaderNodeTexCoord")
mp=n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(1.0,1.0,3.5)  # damari uzat
l.new(tc.outputs["Object"], mp.inputs["Vector"])
wv=n.new("ShaderNodeTexWave"); wv.wave_type='BANDS'
wv.inputs["Scale"].default_value=3.5; wv.inputs["Distortion"].default_value=7
wv.inputs["Detail"].default_value=3; wv.inputs["Detail Scale"].default_value=1.6
l.new(mp.outputs["Vector"], wv.inputs["Vector"])
ramp=n.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color=(0.040,0.020,0.010,1)   # koyu damar
ramp.color_ramp.elements[1].color=(0.185,0.100,0.052,1)   # ceviz
l.new(wv.outputs["Fac"], ramp.inputs["Fac"])
l.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
bump=n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.12
l.new(wv.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
for ob in (body,base,rim): ob.data.materials.append(mat)

# --- cam ---
matg,ng,lg = new_mat("Glass")
g=ng["Principled BSDF"]
g.inputs["Base Color"].default_value=(0.92,0.96,1.0,1)
g.inputs["Roughness"].default_value=0.02
g.inputs["Transmission Weight"].default_value=1.0
g.inputs["IOR"].default_value=1.5
glass.data.materials.append(matg)

# --- kum (spiral oluklu) ---
mats,ns,ls = new_mat("Sand")
s=ns["Principled BSDF"]
s.inputs["Base Color"].default_value=(0.85,0.73,0.54,1)
s.inputs["Roughness"].default_value=0.92
tcs=ns.new("ShaderNodeTexCoord")
# spiral: Wave Rings + buyuk distortion
wring=ns.new("ShaderNodeTexWave"); wring.wave_type='RINGS'; wring.rings_direction='Z'
wring.inputs["Scale"].default_value=30.0; wring.inputs["Distortion"].default_value=1.6
wring.inputs["Detail"].default_value=2.0; wring.inputs["Detail Scale"].default_value=1.4
bumpS=ns.new("ShaderNodeBump"); bumpS.inputs["Strength"].default_value=1.1; bumpS.inputs["Distance"].default_value=0.009
# ince kum gren noise
noi=ns.new("ShaderNodeTexNoise"); noi.inputs["Scale"].default_value=300
bump2=ns.new("ShaderNodeBump"); bump2.inputs["Strength"].default_value=0.08
ls.new(tcs.outputs["Object"], wring.inputs["Vector"])
ls.new(wring.outputs["Color"], bumpS.inputs["Height"])
ls.new(tcs.outputs["Object"], noi.inputs["Vector"])
ls.new(noi.outputs["Fac"], bump2.inputs["Height"])
ls.new(bumpS.outputs["Normal"], bump2.inputs["Normal"])
ls.new(bump2.outputs["Normal"], s.inputs["Normal"])
sand.data.materials.append(mats)

# --- celik bilye ---
matb,nb,lb=new_mat("Steel")
b=nb["Principled BSDF"]
b.inputs["Base Color"].default_value=(0.78,0.78,0.80,1)
b.inputs["Metallic"].default_value=1.0; b.inputs["Roughness"].default_value=0.08
ball.data.materials.append(matb)

# --- LED emission ---
matl,nl,ll=new_mat("LED")
em=nl.new("ShaderNodeEmission")
LED_COLOR=(0.15,0.55,1.0,1) if MODE=="dark" else (0.3,0.65,1.0,1)
em.inputs["Color"].default_value=LED_COLOR
em.inputs["Strength"].default_value=22 if MODE=="dark" else 14
out=nl["Material Output"]; ll.new(em.outputs["Emission"], out.inputs["Surface"])
led.data.materials.append(matl)

# --- zemin ---
matf,nf,lf=new_mat("Floor")
f=nf["Principled BSDF"]
fcol=(0.018,0.018,0.022,1) if MODE=="dark" else (0.10,0.10,0.115,1)
f.inputs["Base Color"].default_value=fcol; f.inputs["Roughness"].default_value=0.42
floor.data.materials.append(matf)

# =========================== ISIK / DUNYA ===========================
world=bpy.data.worlds.new("W"); scene.world=world; world.use_nodes=True
bg=world.node_tree.nodes["Background"]
if MODE=="dark":
    bg.inputs["Color"].default_value=(0.01,0.01,0.015,1); bg.inputs["Strength"].default_value=0.3
else:
    bg.inputs["Color"].default_value=(0.32,0.34,0.38,1); bg.inputs["Strength"].default_value=0.5

def area(name, loc, energy, size, rot=(0,0,0), color=(1,1,1), spec=0.15):
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=energy; ld.size=size; ld.color=color
    ld.specular_factor=spec   # dusuk -> cam/bilye isiklari aynalamaz (beyaz blok yok)
    ob=bpy.data.objects.new(name,ld); ob.location=loc; ob.rotation_euler=rot
    scene.collection.objects.link(ob); return ob

# bakis hedefi
target=Vector((0,0,H))
def aim(ob):
    d=target-Vector(ob.location); ob.rotation_euler=d.to_track_quat('-Z','Y').to_euler()

if MODE=="dark":
    k=area("Key",(0.6,-0.5,0.9),60,0.6); aim(k)
    r=area("Rim",(-0.7,0.4,0.8),40,0.5,color=(0.6,0.7,1.0)); aim(r)
else:
    k=area("Key",(0.9,-0.8,1.3),130,1.2,spec=0.4); aim(k)   # bilye highlight icin
    fll=area("Fill",(-1.0,-0.3,0.9),45,1.5,spec=0.1); aim(fll)
    rm=area("Rim",(-0.5,0.9,1.1),75,1.0,color=(0.8,0.85,1.0),spec=0.1); aim(rm)
    top=area("Top",(0.05,-0.05,1.5),48,1.4,spec=0.1); aim(top)   # yumusak tepe dolgu (oluk golgesi korunur)

# =========================== KAMERA ===========================
cam_target=Vector((0,0,0.20))
cam_d=bpy.data.cameras.new("Cam"); cam_d.lens=50
cam=bpy.data.objects.new("Cam",cam_d)
cam.location=(1.18,-1.18,1.06)
scene.collection.objects.link(cam); scene.camera=cam
d=cam_target-Vector(cam.location); cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
cam_d.dof.use_dof=True; cam_d.dof.focus_distance=(target-Vector(cam.location)).length
cam_d.dof.aperture_fstop=5.6

# =========================== RENDER AYAR ===========================
scene.render.engine='CYCLES'
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use=True
    scene.cycles.device='GPU'
except Exception as e:
    print("GPU ayarlanamadi, CPU:", e)
scene.cycles.samples=220
scene.cycles.use_denoising=True
scene.view_settings.view_transform='Filmic'  # ahsap tonunu daha az soldurur
scene.view_settings.look='Medium Contrast'
scene.view_settings.exposure=0.0
scene.render.resolution_x=1600
scene.render.resolution_y=1200
scene.render.image_settings.file_format='PNG'
scene.render.filepath=OUT

print(f"RENDER baslama: MODE={MODE} -> {OUT}")
bpy.ops.render.render(write_still=True)
print("RENDER bitti:", OUT)
