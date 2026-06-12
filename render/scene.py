# ============================================================================
#  Kinetik Kum Masasi - tam dizgi sahnesi (ayakli sehpa + tum alt bilesenler)
#  - gercek .thr Sandify deseni kuma uygulanir
#  - oturma odasi HDRI + PBR malzemeler
#  - Cikti: Cycles render (hero/dark/room/top) VE web icin table.glb (patlatma)
#  Calistir: Blender --background --python scene.py -- <hero|dark|room|top|glb>
# ============================================================================
import bpy, math, os, sys
from mathutils import Vector

ARGV=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
MODE=ARGV[0] if ARGV else "hero"
DIR=os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/Users/emirhanyakar/Desktop/design_sale/render"
ROOT=os.path.dirname(DIR)
HDRI=os.path.join(DIR,"assets","living_room.hdr")
STUDIO=os.path.join(DIR,"assets","studio.hdr")
WOOD_DIFF=os.path.join(DIR,"assets","wood_diff.jpg")
WOOD_ROUGH=os.path.join(DIR,"assets","wood_rough.jpg")
WOOD_NOR=os.path.join(DIR,"assets","wood_nor.jpg")
SAND_DIFF=os.path.join(DIR,"assets","sand_diff.jpg")
SAND_ROUGH=os.path.join(DIR,"assets","sand_rough.jpg")
SAND_NOR=os.path.join(DIR,"assets","sand_nor.jpg")
GROOVE_HMAP=os.path.join(DIR,"assets","groove_height.png")  # gercek oluk yukseklik haritasi
THR = os.environ.get("PATTERN_THR") or os.path.join(ROOT,"firmware","patterns","spiral_rose.thr")
if not os.path.isabs(THR): THR=os.path.join(ROOT,"firmware","patterns",THR)

# ---- olculer (m) ----
R=0.30; DRUM_H=0.15; LEG_H=0.30
BASE_Z=LEG_H                       # drum tabani
TOP_Z =BASE_Z+DRUM_H               # masa ust kotu (0.45)
WELL_D=0.05; WELL_R=R*0.90
SAND_Z=TOP_Z-WELL_D+0.008
SAND_TOP=SAND_Z+0.006

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
def link(o):
    if o.name not in scene.collection.objects: scene.collection.objects.link(o)

def mat(name,base,rough=0.5,metal=0.0,emis=None,emis_str=0,transmission=0,clear=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*base,1)
    b.inputs["Roughness"].default_value=rough
    b.inputs["Metallic"].default_value=metal
    if transmission: b.inputs["Transmission Weight"].default_value=transmission
    if clear: b.inputs["Coat Weight"].default_value=clear
    if emis:
        b.inputs["Emission Color"].default_value=(*emis,1)
        b.inputs["Emission Strength"].default_value=emis_str
    return m,m.node_tree

def wood_textured(name="Walnut",scale=(2.0,1.0),tint=(0.55,0.42,0.28)):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; n=nt.nodes; l=nt.links
    b=n["Principled BSDF"]; b.inputs["Coat Weight"].default_value=0.25; b.inputs["Coat Roughness"].default_value=0.25
    tc=n.new("ShaderNodeTexCoord"); mp=n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(*scale,1)
    l.new(tc.outputs["UV"],mp.inputs["Vector"])
    di=n.new("ShaderNodeTexImage"); di.image=bpy.data.images.load(WOOD_DIFF)
    ro=n.new("ShaderNodeTexImage"); ro.image=bpy.data.images.load(WOOD_ROUGH); ro.image.colorspace_settings.name='Non-Color'
    no=n.new("ShaderNodeTexImage"); no.image=bpy.data.images.load(WOOD_NOR); no.image.colorspace_settings.name='Non-Color'
    nm=n.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value=0.8
    # koyu ceviz tonu icin diffuse'u hafif karart/renklendir
    mix=n.new("ShaderNodeMixRGB"); mix.blend_type='MULTIPLY'; mix.inputs["Fac"].default_value=0.85
    mix.inputs["Color2"].default_value=(*tint,1)
    for nd in (mp,di,ro,no): l.new(mp.outputs["Vector"],nd.inputs["Vector"]) if nd in (di,ro,no) else None
    l.new(di.outputs["Color"],mix.inputs["Color1"]); l.new(mix.outputs["Color"],b.inputs["Base Color"])
    l.new(ro.outputs["Color"],b.inputs["Roughness"])
    l.new(no.outputs["Color"],nm.inputs["Color"]); l.new(nm.outputs["Normal"],b.inputs["Normal"])
    return m

def wood_grain(m,nt,dark=(0.05,0.026,0.014),light=(0.20,0.11,0.06)):
    n=nt.nodes; l=nt.links; b=n["Principled BSDF"]
    tc=n.new("ShaderNodeTexCoord"); mp=n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(1,1,3.5)
    wv=n.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value=3.2; wv.inputs["Distortion"].default_value=6
    wv.inputs["Detail"].default_value=3
    rp=n.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color=(*dark,1); rp.color_ramp.elements[1].color=(*light,1)
    bm=n.new("ShaderNodeBump"); bm.inputs["Strength"].default_value=0.12
    l.new(tc.outputs["Object"],mp.inputs["Vector"]); l.new(mp.outputs["Vector"],wv.inputs["Vector"])
    l.new(wv.outputs["Fac"],rp.inputs["Fac"]); l.new(rp.outputs["Color"],b.inputs["Base Color"])
    l.new(wv.outputs["Fac"],bm.inputs["Height"]); l.new(bm.outputs["Normal"],b.inputs["Normal"])

# ---------- primitifler ----------
def cyl(name,r,d,z,v=96,r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,vertices=v,location=(0,0,z))
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r,radius2=r2,depth=d,vertices=v,location=(0,0,z))
    o=bpy.context.active_object; o.name=name; bpy.ops.object.shade_smooth(); return o
def box(name,sx,sy,sz,loc):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.active_object; o.name=name
    o.scale=(sx/2,sy/2,sz/2); bpy.ops.object.transform_apply(scale=True); return o

# ============================ GEOMETRI ============================
# --- govde (drum) + kum havuzu ---
body=cyl("Body",R,DRUM_H,BASE_Z+DRUM_H/2,128)
wellcut=cyl("wc",WELL_R,WELL_D+0.02,TOP_Z-WELL_D/2+0.01,128)
md=body.modifiers.new("w","BOOLEAN"); md.operation='DIFFERENCE'; md.object=wellcut
bpy.context.view_layer.objects.active=body; bpy.ops.object.modifier_apply(modifier="w")
bpy.data.objects.remove(wellcut,do_unlink=True)
mb=body.modifiers.new("b","BEVEL"); mb.width=0.004; mb.segments=3

# --- ayaklar (4, hafif acik, konik) -> tek "Legs" ---
legs=[]
for i in range(4):
    a=math.radians(45+i*90)
    lx,ly=0.205*math.cos(a),0.205*math.sin(a)
    bpy.ops.mesh.primitive_cone_add(radius1=0.020,radius2=0.011,depth=LEG_H,vertices=24,
        location=(lx,ly,LEG_H/2))
    o=bpy.context.active_object; o.name=f"leg{i}"
    o.rotation_euler=(math.radians(7)*math.sin(a),-math.radians(7)*math.cos(a),0)
    bpy.ops.object.shade_smooth(); legs.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in legs: o.select_set(True)
bpy.context.view_layer.objects.active=legs[0]; bpy.ops.object.join()
Legs=bpy.context.active_object; Legs.name="Legs"

# --- ust ahsap cerceve ---
bpy.ops.mesh.primitive_torus_add(major_radius=(R+WELL_R)/2,minor_radius=(R-WELL_R)/2,
    location=(0,0,TOP_Z),major_segments=160,minor_segments=20)
Rim=bpy.context.active_object; Rim.name="Rim"; bpy.ops.object.shade_smooth()

# --- kum diski (still'de gercek oluk displacement; video'da duz kum + ilerleyen tube; glb'de silindir) ---
R_CAP=WELL_R*0.985
GROOVE3D = (MODE not in ("glb","video")) and os.path.exists(GROOVE_HMAP)
if GROOVE3D:
    import bmesh
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=600,y_subdivisions=600,size=2*R_CAP,location=(0,0,SAND_TOP))
    Sand=bpy.context.active_object; Sand.name="Sand"
    bm=bmesh.new(); bm.from_mesh(Sand.data); R2=R_CAP*R_CAP
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x*v.co.x+v.co.y*v.co.y>R2],context='VERTS')
    bm.to_mesh(Sand.data); bm.free(); bpy.ops.object.shade_smooth()
else:
    Sand=cyl("Sand",R_CAP,0.012,SAND_Z,256)

# --- .thr deseni -> oluk egrisi ---
def load_thr(p):
    out=[]
    for ln in open(p):
        s=ln.split()
        if len(s)==2:
            try: out.append((float(s[0]),float(s[1])))
            except: pass
    return out
_raw=load_thr(THR); thr=_raw[::(4 if len(_raw)>9000 else 3)]
sr=WELL_R*0.92
pts=[(rho*sr*math.cos(th),rho*sr*math.sin(th)) for th,rho in thr]
cu=bpy.data.curves.new("GrooveC","CURVE"); cu.dimensions='3D'
sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
for i,(x,y) in enumerate(pts): sp.points[i].co=(x,y,SAND_TOP-0.0006,1)
# yogun portre desenlerinde cizgiler birlesmesin -> ince oluk (hafif geometri)
cu.bevel_depth=(0.0007 if len(pts)>6000 else 0.0015); cu.bevel_resolution=1
Groove=bpy.data.objects.new("Groove",cu); link(Groove)
# still'de oluk = displacement (tube gizli); video'da tube gorunur (ilerleyen cizim)
if GROOVE3D: Groove.hide_render=True
ball_xy=pts[-1]

# --- celik bilye (desenin ucunda) ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.009,location=(ball_xy[0],ball_xy[1],SAND_TOP+0.006))
Ball=bpy.context.active_object; Ball.name="Ball"; bpy.ops.object.shade_smooth()

# --- LED halka ---
bpy.ops.mesh.primitive_torus_add(major_radius=WELL_R*0.99,minor_radius=0.004,
    location=(0,0,TOP_Z-0.006),major_segments=180,minor_segments=12)
LED=bpy.context.active_object; LED.name="LED_Ring"; bpy.ops.object.shade_smooth()

# --- cam ust (hero/top'ta kameradan gizli -> kum deseni net) ---
Glass=cyl("Glass",R*0.92,0.005,TOP_Z-0.004,128)
Glass.visible_camera = MODE in ("dark","room")

# ===== ic mekanizma (drum icinde, kumun altinda) =====
MECH_Z=BASE_Z+0.012
BasePlate=cyl("BasePlate",WELL_R*0.98,0.006,BASE_Z+0.006,96)
PCB=box("PCB",0.10,0.075,0.004,(0.12,0.0,BASE_Z+0.02)); PCB.rotation_euler=(0,0,math.radians(20))
ThetaMotor=box("Theta_Motor",0.042,0.042,0.04,(0,0,MECH_Z+0.02))
cyl("ts",0.011,0.02,MECH_Z+0.05,16); shaft=bpy.context.active_object; shaft.name="theta_shaft"
# kol
Arm=box("Arm",WELL_R*1.5,0.03,0.01,(WELL_R*0.30,0,MECH_Z+0.06))
RhoMotor=box("Rho_Motor",0.03,0.03,0.028,(WELL_R*0.80,0,MECH_Z+0.06))
Carriage=box("Carriage",0.03,0.03,0.012,(WELL_R*0.45,0,MECH_Z+0.072))
Magnet=cyl("Magnet",0.009,0.01,MECH_Z+0.084,24)
# birlestir: kol grubu
for o in (shaft,):
    pass

# --- zemin (room disinda da hafif yansima icin) ---
bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,0))
Floor=bpy.context.active_object; Floor.name="Floor"

# ============================ MALZEMELER ============================
FINISH=os.environ.get("FINISH","walnut")  # endustriyel tasarim varyantlari
_TINT={"walnut":(0.55,0.42,0.28),"noir":(0.14,0.12,0.13),"ash":(2.0,1.85,1.45)}  # ash: multiply>1 -> acik mese
wm=wood_textured(FINISH.title(),scale=(2.4,1.4),tint=_TINT.get(FINISH,_TINT["walnut"])) if os.path.exists(WOOD_DIFF) else mat("Walnut",(0.12,0.07,0.04),0.42,clear=0.15)[0]
for o in (body,Legs): o.data.materials.append(wm)
if FINISH=="noir":  # fircali celik rim (kontrast)
    _rs,_=mat("RimSteel",(0.62,0.63,0.66),rough=0.34,metal=1.0); Rim.data.materials.append(_rs)
else:
    Rim.data.materials.append(wm)
gm,_=mat("Glass",(0.92,0.96,1.0),rough=0.03,transmission=1.0); gm.node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value=1.5
Glass.data.materials.append(gm)
# kum: gercek PBR doku haritalari (renk/rough/normal) + sicak ton + ince gren
sm,snt=mat("Sand",(0.86,0.74,0.55),rough=0.92)
sn=snt.nodes; sl=snt.links; sb=sn["Principled BSDF"]
if os.path.exists(SAND_DIFF):
    tcs=sn.new("ShaderNodeTexCoord"); mps=sn.new("ShaderNodeMapping"); mps.inputs["Scale"].default_value=(7,7,7)
    sl.new(tcs.outputs["UV"],mps.inputs["Vector"])
    sd=sn.new("ShaderNodeTexImage"); sd.image=bpy.data.images.load(SAND_DIFF)
    sr=sn.new("ShaderNodeTexImage"); sr.image=bpy.data.images.load(SAND_ROUGH); sr.image.colorspace_settings.name='Non-Color'
    sno=sn.new("ShaderNodeTexImage"); sno.image=bpy.data.images.load(SAND_NOR); sno.image.colorspace_settings.name='Non-Color'
    snm=sn.new("ShaderNodeNormalMap"); snm.inputs["Strength"].default_value=0.8
    sb.inputs["Specular IOR Level"].default_value=0.0     # tam mat kuru kum -> tepe yansimasi (oval leke) yok
    tnt=sn.new("ShaderNodeMixRGB"); tnt.blend_type='MULTIPLY'; tnt.inputs["Fac"].default_value=1.0; tnt.inputs["Color2"].default_value=(1.5,1.16,0.74,1)
    for nd in (sd,sr,sno): sl.new(mps.outputs["Vector"],nd.inputs["Vector"])
    sl.new(sd.outputs["Color"],tnt.inputs["Color1"]); sl.new(tnt.outputs["Color"],sb.inputs["Base Color"])
    sl.new(sr.outputs["Color"],sb.inputs["Roughness"])
    sl.new(sno.outputs["Color"],snm.inputs["Color"]); sl.new(snm.outputs["Normal"],sb.inputs["Normal"])
else:
    tcs=sn.new("ShaderNodeTexCoord"); n1=sn.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value=300
    b1=sn.new("ShaderNodeBump"); b1.inputs["Strength"].default_value=0.1
    sl.new(tcs.outputs["Object"],n1.inputs["Vector"]); sl.new(n1.outputs["Fac"],b1.inputs["Height"]); sl.new(b1.outputs["Normal"],sb.inputs["Normal"])
Sand.data.materials.append(sm)

# --- GERCEK OLUK: yuksek-coz grid + Displace modifier (bounded, OOM yok) ---
if GROOVE3D:
    gtex=bpy.data.textures.new("groove","IMAGE"); gtex.image=bpy.data.images.load(GROOVE_HMAP)
    gtex.image.colorspace_settings.name='Non-Color'; gtex.extension='EXTEND'
    dm=Sand.modifiers.new("groove","DISPLACE")
    dm.texture=gtex; dm.texture_coords='UV'; dm.direction='Z'
    dm.mid_level=0.5; dm.strength=0.007    # oluk ~1.6mm cukur + kenar kabarma
# video'da gorunur ilerleyen oluk: acik, hafif isikli (taze cizilmis kum gibi)
if MODE=="video":
    grm,_=mat("Groove",(0.90,0.78,0.52),rough=0.7,emis=(0.95,0.82,0.55),emis_str=0.55)
else:
    grm,_=mat("Groove",(0.42,0.33,0.21),rough=0.97)
Groove.data.materials.append(grm)
stm,_=mat("Steel",(0.80,0.80,0.82),rough=0.07,metal=1.0); Ball.data.materials.append(stm)
# LED: goze batmayan yumusak/los glow -> dusuk emisyon (glare esigi 1.7'yi gecip
# hafif halo verir ama beyaz yanmaz); hafif sicak-beyaz-mavi ton
LEDc=(0.45,0.62,0.95) if MODE=="dark" else (0.55,0.68,0.92)
lm,_=mat("LED",(0,0,0),emis=LEDc,emis_str=(6.0 if MODE=="dark" else 3.2)); LED.data.materials.append(lm)
alu,_=mat("Aluminum",(0.55,0.56,0.58),rough=0.35,metal=1.0)
for o in (ThetaMotor,RhoMotor,shaft,Carriage): o.data.materials.append(alu)
arm_m,_=mat("ArmAlu",(0.7,0.71,0.73),rough=0.3,metal=1.0); Arm.data.materials.append(arm_m)
mag,_=mat("Magnet",(0.15,0.15,0.17),rough=0.4,metal=1.0); Magnet.data.materials.append(mag)
pcbm,_=mat("PCB",(0.06,0.30,0.16),rough=0.45); PCB.data.materials.append(pcbm)
bpm,_=mat("BasePlate",(0.08,0.08,0.09),rough=0.6,metal=0.6); BasePlate.data.materials.append(bpm)
# parlak studyo zemini (yansima + HDRI) -> premium urun cekimi
flcol=(0.04,0.04,0.05) if MODE in ("hero","top","dark") else (0.14,0.13,0.12)
flm,_=mat("FloorMat",flcol,rough=0.18,clear=0.3); Floor.data.materials.append(flm)

# ============================ DUNYA / ISIK ============================
world=bpy.data.worlds.new("W"); scene.world=world; world.use_nodes=True
wn=world.node_tree; bg=wn.nodes["Background"]
hdri_path = STUDIO if (MODE in ("hero","top","dark") and os.path.exists(STUDIO)) else HDRI
if os.path.exists(hdri_path):
    env=wn.nodes.new("ShaderNodeTexEnvironment"); env.image=bpy.data.images.load(hdri_path)
    mapp=wn.nodes.new("ShaderNodeMapping"); texc=wn.nodes.new("ShaderNodeTexCoord")
    wn.links.new(texc.outputs["Generated"],mapp.inputs["Vector"]); wn.links.new(mapp.outputs["Vector"],env.inputs["Vector"])
    mapp.inputs["Rotation"].default_value=(0,0,math.radians(40))
    wn.links.new(env.outputs["Color"],bg.inputs["Color"])
    bg.inputs["Strength"].default_value=(0.25 if MODE=="dark" else (1.0 if MODE=="room" else 0.7))
else:
    bg.inputs["Color"].default_value=(0.3,0.32,0.36,1); bg.inputs["Strength"].default_value=0.6

def area(name,loc,e,sz,col=(1,1,1),spec=0.15):
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=e; ld.size=sz; ld.color=col; ld.specular_factor=spec
    o=bpy.data.objects.new(name,ld); o.location=loc; link(o)
    d=Vector((0,0,TOP_Z))-Vector(loc); o.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); return o
if MODE=="dark":
    area("Key",(0.7,-0.6,1.2),45,0.7,spec=0.3); area("Rim",(-0.7,0.5,1.0),35,0.6,(0.6,0.7,1.0))
else:
    area("Key",(1.0,-0.9,1.5),90,1.2,spec=0.35); area("Top",(0.1,-0.1,1.7),52,1.6,spec=0.0)
    if MODE=="top": area("Graze",(1.5,-1.1,0.52),85,0.8,spec=0.0)  # alcak siyirgan: oluk golgesi belirsin

# ============================ KAMERA ============================
CAMS={
 "hero":((1.25,-1.25,1.05),(0,0,0.30),50),
 "room":((1.7,-1.5,0.9),(0,0,0.34),38),
 "dark":((1.15,-1.15,1.0),(0,0,0.32),52),
 "top": ((0.0,-0.42,1.6),(0,0,0.30),50),
}
def setcam(mode):
    loc,tgt,lens=CAMS.get(mode,CAMS["hero"])
    cd=bpy.data.cameras.new("Cam"); cd.lens=lens
    c=bpy.data.objects.new("Cam",cd); c.location=loc; link(c); scene.camera=c
    d=Vector(tgt)-Vector(loc); c.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    cd.dof.use_dof=True; cd.dof.focus_distance=(Vector(tgt)-Vector(loc)).length; cd.dof.aperture_fstop=3.6

# ============================ CIKTI ============================
def gpu():
    try:
        pr=bpy.context.preferences.addons['cycles'].preferences
        pr.compute_device_type='METAL'; pr.get_devices()
        for d in pr.devices: d.use=True
        scene.cycles.device='GPU'
    except Exception as e: print("GPU?",e)

def add_post():  # LED bloom (glare) + vignette
    scene.use_nodes=True; nt=scene.node_tree; nt.nodes.clear()
    rl=nt.nodes.new("CompositorNodeRLayers")
    gl=nt.nodes.new("CompositorNodeGlare"); gl.glare_type='FOG_GLOW'; gl.quality='HIGH'; gl.threshold=1.7; gl.size=8
    em=nt.nodes.new("CompositorNodeEllipseMask"); em.width=0.82; em.height=0.86
    bl=nt.nodes.new("CompositorNodeBlur"); bl.filter_type='FAST_GAUSS'; bl.use_relative=True; bl.factor_x=0.22; bl.factor_y=0.22
    rp=nt.nodes.new("CompositorNodeValToRGB")
    rp.color_ramp.elements[0].color=(0.52,0.52,0.52,1); rp.color_ramp.elements[1].color=(1,1,1,1)
    mu=nt.nodes.new("CompositorNodeMixRGB"); mu.blend_type='MULTIPLY'; mu.inputs[0].default_value=0.9
    co=nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"],gl.inputs["Image"])
    nt.links.new(em.outputs["Mask"],bl.inputs["Image"]); nt.links.new(bl.outputs["Image"],rp.inputs["Fac"])
    nt.links.new(gl.outputs["Image"],mu.inputs[1]); nt.links.new(rp.outputs["Image"],mu.inputs[2])
    nt.links.new(mu.outputs["Image"],co.inputs["Image"])

if MODE=="glb":
    # patlatma viewer'i icin: Floor'u sil, glb export
    bpy.data.objects.remove(Floor,do_unlink=True)
    out=os.path.join(DIR,"table.glb")
    bpy.ops.export_scene.gltf(filepath=out,export_format='GLB',export_apply=True,
                              export_yup=True,use_selection=False)
    print("GLB yazildi:",out, os.path.getsize(out))
elif MODE=="video":
    # ---- reklam animasyonu: kamera yorungede doner + bilye deseni cizer ----
    N=96; DRAW_END=N-15
    emp=bpy.data.objects.new("tgt",None); emp.location=(0,0,0.30); link(emp)
    cd=bpy.data.cameras.new("Cam"); cd.lens=46; cd.dof.use_dof=True; cd.dof.aperture_fstop=6.3
    cam=bpy.data.objects.new("Cam",cd); link(cam); scene.camera=cam
    con=cam.constraints.new('TRACK_TO'); con.target=emp; con.track_axis='TRACK_NEGATIVE_Z'; con.up_axis='UP_Y'
    for f,ang in ((1,math.radians(-32)),(N,math.radians(32))):
        r=1.62; cam.location=(r*math.sin(ang),-r*math.cos(ang),1.35); cam.keyframe_insert("location",frame=f)  # daha tepeden -> imza okunur
    cd.dof.focus_distance=2.1
    Groove.data.bevel_factor_start=0.0
    for f in range(1,DRAW_END+1):
        fac=(f-1)/(DRAW_END-1)
        Groove.data.bevel_factor_end=fac; Groove.data.keyframe_insert("bevel_factor_end",frame=f)
        x,y=pts[int(fac*(len(pts)-1))]; Ball.location=(x,y,SAND_TOP+0.006); Ball.keyframe_insert("location",frame=f)
    Groove.data.bevel_factor_end=1.0; Groove.data.keyframe_insert("bevel_factor_end",frame=N)
    Ball.location=(pts[-1][0],pts[-1][1],SAND_TOP+0.006); Ball.keyframe_insert("location",frame=N)
    scene.render.engine='CYCLES'; gpu()
    scene.cycles.samples=64; scene.cycles.use_denoising=True
    scene.view_settings.view_transform='Filmic'; scene.view_settings.look='Medium High Contrast'; scene.view_settings.exposure=0.15
    scene.render.resolution_x=1280; scene.render.resolution_y=720
    scene.frame_start=1; scene.frame_end=N; scene.render.fps=25
    scene.render.image_settings.file_format='FFMPEG'
    scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'
    scene.render.ffmpeg.constant_rate_factor='HIGH'; scene.render.ffmpeg.ffmpeg_preset='GOOD'; scene.render.ffmpeg.audio_codec='NONE'
    scene.render.filepath=os.path.join(DIR,"table_ad.mp4")
    add_post()
    if os.environ.get("ONEFRAME"):  # tek kare PNG (dogrulama)
        fr=int(os.environ["ONEFRAME"]); scene.frame_set(fr)
        scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(DIR,"vid_check.png")
        bpy.ops.render.render(write_still=True); print("ONEFRAME BITTI",fr)
    else:
        print("VIDEO render: %d frame @720p"%N); bpy.ops.render.render(animation=True); print("VIDEO BITTI",scene.render.filepath)
else:
    setcam(MODE)
    scene.render.engine='CYCLES'
    try:
        pr=bpy.context.preferences.addons['cycles'].preferences
        pr.compute_device_type='METAL'; pr.get_devices()
        for d in pr.devices: d.use=True
        scene.cycles.device='GPU'
    except Exception as e: print("GPU?",e)
    scene.cycles.samples=512; scene.cycles.use_denoising=True
    try:  # AgX = Blender'in modern/gercekci tone mapping'i (Filmic'ten ustun)
        scene.view_settings.view_transform='AgX'; scene.view_settings.look='AgX - Punchy'
        scene.view_settings.exposure=0.45
    except Exception:
        scene.view_settings.view_transform='Filmic'; scene.view_settings.look='Medium High Contrast'
        scene.view_settings.exposure=0.15
    scene.render.resolution_x=2000; scene.render.resolution_y=1375
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath=os.path.join(DIR,(f"variant_{FINISH}.png" if FINISH!="walnut" else f"room_{MODE}.png"))
    # ---- kompozitor post: LED bloom (glare) + vignette ----
    scene.use_nodes=True; nt=scene.node_tree; nt.nodes.clear()
    rl=nt.nodes.new("CompositorNodeRLayers")
    gl=nt.nodes.new("CompositorNodeGlare"); gl.glare_type='FOG_GLOW'; gl.quality='HIGH'; gl.threshold=1.7; gl.size=8
    em=nt.nodes.new("CompositorNodeEllipseMask"); em.width=0.82; em.height=0.86
    bl=nt.nodes.new("CompositorNodeBlur"); bl.filter_type='FAST_GAUSS'; bl.use_relative=True; bl.factor_x=0.22; bl.factor_y=0.22
    rp=nt.nodes.new("CompositorNodeValToRGB")
    rp.color_ramp.elements[0].color=(0.52,0.52,0.52,1); rp.color_ramp.elements[1].color=(1,1,1,1)
    mu=nt.nodes.new("CompositorNodeMixRGB"); mu.blend_type='MULTIPLY'; mu.inputs[0].default_value=0.9
    co=nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"],gl.inputs["Image"])
    nt.links.new(em.outputs["Mask"],bl.inputs["Image"]); nt.links.new(bl.outputs["Image"],rp.inputs["Fac"])
    nt.links.new(gl.outputs["Image"],mu.inputs[1]); nt.links.new(rp.outputs["Image"],mu.inputs[2])
    nt.links.new(mu.outputs["Image"],co.inputs["Image"])
    print("RENDER:",MODE,"(2K/384spp + post)"); bpy.ops.render.render(write_still=True); print("BITTI",scene.render.filepath)
