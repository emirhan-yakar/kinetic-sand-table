#!/usr/bin/env python3
# ============================================================================
#  DXF profillerinden 3D KATI + STEP export (cadquery).
#  Fusion/FreeCAD/SolidWorks'te acilip mekanik dogrulamaya baslamak icin.
#  Olculer make_dxf.py / montaj.md ile ayni (mm).
#  Calistir: python3 make_step.py   (cadquery gerekir)
#  NOT: delik konumlari temsilidir; gercek COTS parcalarla dogrulanmali.
# ============================================================================
import math
import cadquery as cq

SASI_D=520.0; DRUM_PCD=500.0; TT_PCD=120.0; NEMA=31.0
M3,M4,M5=3.2,4.5,5.5

def bc(pcd,n,d,a0=45):  # bolt circle -> (x,y,dia)
    return [(pcd/2*math.cos(math.radians(a0+360*i/n)),
             pcd/2*math.sin(math.radians(a0+360*i/n)), d) for i in range(n)]
def nema(cx,cy,bore=22.0):
    h=[(cx,cy,bore)]
    for sx in(-1,1):
        for sy in(-1,1): h.append((cx+sx*NEMA/2,cy+sy*NEMA/2,M3))
    return h

def make(outline, th, holes, slots=()):
    p=outline.extrude(th)
    for (x,y,dia) in holes:
        p=p.cut(cq.Workplane("XY").center(x,y).circle(dia/2).extrude(th+2).translate((0,0,-1)))
    for (x,y,w,h) in slots:
        p=p.cut(cq.Workplane("XY").center(x,y).rect(w,h).extrude(th+2).translate((0,0,-1)))
    return p

# ---- SASI (Ø520, 4mm) ----
sasi_h = bc(DRUM_PCD,4,M4,45)+[(0,0,90.0)]+bc(TT_PCD,4,M4,0)+nema(95,0)
sasi_h += [(-95+sx*46,70+sy*33.5,M3) for sx in(-1,1) for sy in(-1,1)]
sasi=make(cq.Workplane("XY").circle(SASI_D/2), 4.0, sasi_h, [(28,-150,16,30)])
cq.exporters.export(sasi,"sasi.step")
print("sasi.step")

# ---- AYAK PLAKASI (60x60, 4mm) ----
ay_h=[(sx*18,sy*18,M5) for sx in(-1,1) for sy in(-1,1)]+[(0,0,20.0)]
ayak=make(cq.Workplane("XY").rect(60,60), 4.0, ay_h)
cq.exporters.export(ayak,"ayak_plakasi.step")
print("ayak_plakasi.step")

# ---- KOL (320x40, 5mm) ----  pivot ucu x=-30..290 -> merkez 130
L=290.0; W=40.0
kol_outline=cq.Workplane("XY").polyline([(-30,-W/2),(L,-W/2),(L,W/2),(-30,W/2)]).close()
kol_h=bc(30,4,M3,45)+[(0,0,8.0)]+[(40+i*20,0,M3) for i in range(11)]+nema(L-22,0)
kol=make(kol_outline, 5.0, kol_h)
cq.exporters.export(kol,"kol.step")
print("kol.step")
print("BITTI - 3 STEP (Fusion/FreeCAD'de acilabilir)")
