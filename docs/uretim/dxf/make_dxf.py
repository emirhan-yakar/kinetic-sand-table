#!/usr/bin/env python3
# ============================================================================
#  CNC/lazer DXF kesim dosyalari — alüminyum sasi, ayak plakasi, donen kol.
#  Olculer montaj_hesap.py / montaj.md ile tutarli (mm). Cikti: *.dxf + onizleme.
#  Calistir: python3 make_dxf.py
#  NOT: delik konumlari TEMSILIDIR; nihai mekanik CAD ile dogrulanmali.
# ============================================================================
import math, os
import ezdxf
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))

# ---- olculer (mm) ----
WELL_R=270.0          # kum havuzu yaricapi (drum ic)
SASI_D=520.0          # sasi disk capi (Al 4mm)
DRUM_PCD=500.0        # drum baglanti deligi PCD
TT_PCD=120.0          # turntable (lazy susan) civata dairesi
NEMA=31.0             # NEMA17 delik karesi
M3,M4,M5=3.2,4.5,5.5  # delik caplari (gecme)

def hole(g,x,y,d): g.append(("c",x,y,d/2))
def boltcircle(g,pcd,n,d,a0=45):
    for i in range(n):
        a=math.radians(a0+360*i/n); hole(g,pcd/2*math.cos(a),pcd/2*math.sin(a),d)
def nema17(g,cx,cy,bore=22.0):
    hole(g,cx,cy,bore)
    for sx in(-1,1):
        for sy in(-1,1): hole(g,cx+sx*NEMA/2,cy+sy*NEMA/2,M3)
def rect(g,cx,cy,w,h):
    g.append(("p",[(cx-w/2,cy-h/2),(cx+w/2,cy-h/2),(cx+w/2,cy+h/2),(cx-w/2,cy+h/2)]))
def rect_holes(g,cx,cy,w,h,d):
    for sx in(-1,1):
        for sy in(-1,1): hole(g,cx+sx*w/2,cy+sy*h/2,d)

# ============ PARCALAR (geometri listesi) ============
def sasi():
    g=[]
    g.append(("c",0,0,SASI_D/2))                 # dis kontur
    boltcircle(g,DRUM_PCD,4,M4,45)               # drum baglanti 4x M4
    g.append(("c",0,0,45.0))                     # merkez: slip ring + kayis bosluk Ø90
    boltcircle(g,TT_PCD,4,M4,0)                  # turntable civata dairesi 4x M4
    nema17(g,95,0)                               # theta motoru (kayis tahrik, offset)
    rect_holes(g,-95,70,92,67,M3)                # kontrol karti 4x M3 (standoff)
    rect(g,28,-150,16,30)                        # kablo yuvasi (slot, temsili)
    return g,"sasi"

def ayak_plakasi():
    g=[]
    rect(g,0,0,60,60)                            # 60x60 plaka
    rect_holes(g,0,0,36,36,M5)                   # 4x M5 (ayak->drum)
    hole(g,0,0,20.0)                             # ayak tenon/spigot Ø20
    return g,"ayak_plakasi"

def kol():
    L=290.0; W=40.0
    g=[]
    g.append(("p",[(-30,-W/2),(L,-W/2),(L,W/2),(-30,W/2)]))  # bar (pivot ucu -30)
    boltcircle(g,30,4,M3,45)                     # pivot: turntable'a 4x M3
    hole(g,0,0,8)                                # pivot merkez
    for i in range(11):                          # MGN12 ray M3 @ 20mm
        hole(g,40+i*20,0,M3)
    nema17(g,L-22,0)                             # rho motoru kol ucunda
    return g,"kol"

# ============ DXF + ONIZLEME yaz ============
def write(part):
    g,name=part
    doc=ezdxf.new("R2010"); doc.units=ezdxf.units.MM; msp=doc.modelspace()
    for e in g:
        if e[0]=="c": msp.add_circle((e[1],e[2]),e[3])
        else: msp.add_lwpolyline(e[1],close=True)
    doc.saveas(os.path.join(HERE,name+".dxf"))
    # onizleme
    xs=[]; ys=[]
    for e in g:
        if e[0]=="c": xs+= [e[1]-e[3],e[1]+e[3]]; ys+=[e[2]-e[3],e[2]+e[3]]
        else:
            for p in e[1]: xs.append(p[0]); ys.append(p[1])
    minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys); pad=20
    W=maxx-minx+2*pad; H=maxy-miny+2*pad; sc=min(900/W,900/H)
    IW,IH=int(W*sc),int(H*sc)
    im=Image.new("RGB",(IW,IH),(255,255,255)); dr=ImageDraw.Draw(im)
    def X(x):return (x-minx+pad)*sc
    def Y(y):return IH-(y-miny+pad)*sc
    for e in g:
        if e[0]=="c":
            dr.ellipse((X(e[1]-e[3]),Y(e[2]+e[3]),X(e[1]+e[3]),Y(e[2]-e[3])),outline=(0,80,200),width=2)
        else:
            pts=[(X(p[0]),Y(p[1])) for p in e[1]]+[(X(e[1][0][0]),Y(e[1][0][1]))]
            dr.line(pts,fill=(0,80,200),width=2)
    try: f=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf",22)
    except: f=ImageFont.load_default()
    dr.text((10,8),f"{name}.dxf  ({maxx-minx:.0f} x {maxy-miny:.0f} mm)",font=f,fill=(20,20,20))
    im.save(os.path.join(HERE,name+"_preview.png"))
    print(f"{name}.dxf  ({maxx-minx:.0f}x{maxy-miny:.0f}mm)  delik/eleman: {len(g)}")

for p in (sasi(),ayak_plakasi(),kol()): write(p)
print("Bitti. Ayak plakasi: 4 adet kesilecek.")
