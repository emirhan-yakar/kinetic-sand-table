#!/usr/bin/env python3
# Mekanizma KESIT diyagrami (yan kesit, semaik). PIL. -> mekanizma_kesit.png
import os, math
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
W,H=1400,1000
im=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(im)
def F(sz,b=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if b else [])+["/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
INK=(30,30,36); BLUE=(20,110,220); MUT=(120,120,130)
WOOD=(150,95,55); GLASS=(150,200,225); SAND=(196,168,110); STEEL=(120,125,135)
ALU=(180,182,188); MOT=(70,75,85); MAG=(225,70,60); BEAR=(120,160,210); RING=(150,120,200)

CX=470; FY=880; s=1.4
def Y(h): return FY-h*s
def X(x): return CX+x*s
def box(x0,h0,x1,h1,fill,outline=INK,wd=2):
    d.rectangle((X(x0),Y(h1),X(x1),Y(h0)),fill=fill,outline=outline,width=wd)

d.text((40,28),"KİNETİK KUM MASASI — MEKANİZMA KESİTİ (şematik, yan kesit)",font=F(26),fill=INK)
d.text((40,62),"θ = dönme (kol) · ρ = yarıçap (taşıyıcı) · bilye kumun altından mıknatısla sürüklenir",font=F(17,False),fill=MUT)

# --- ayaklar (8 derece splay) ---
for sgn in(-1,1):
    top=sgn*210; foot=sgn*254
    d.line((X(top),Y(320),X(foot),Y(0)),fill=WOOD,width=14)

# --- govde (drum) ---
box(-300,320,-270,467,WOOD)      # sol duvar
box(270,320,300,467,WOOD)        # sag duvar
box(-300,320,300,332,WOOD)       # taban
# --- cam ust ---
box(-276,464,276,470,GLASS)
# --- kum tepsisi + kum ---
box(-270,406,270,410,(210,210,214))      # tepsi tabani (ferromanyetik DEGIL)
box(-270,410,270,460,SAND)               # kum
# bilye
br=150; d.ellipse((X(br)-9,Y(462)-9,X(br)+9,Y(462)+9),fill=STEEL,outline=INK)

# --- MEKANIZMA ---
box(-260,356,260,360,ALU)                # sasi plakasi
box(-21,322,21,356,MOT)                  # theta motoru (sasi alti)
d.text((X(0)-70,Y(322)-2),"θ motor +3:1",font=F(13),fill=(255,255,255))
box(-75,360,75,372,BEAR)                 # lazy-susan rulman
box(-14,360,14,374,RING)                 # slip ring (merkez)
# donen kol (saga uzanir)
box(-30,372,250,378,(205,150,90))
# MGN12 ray (kol ustu)
box(0,378,250,381,STEEL)
# tasiyici + miknatis (rho=150)
box(br-25,381,br+25,394,ALU)             # tasiyici (MGN12H)
box(br-12,394,br+12,402,MAG)             # miknatis N52
# rho motoru (kol pivot ucu)
box(-30,378,12,412,MOT)
d.text((X(-30)+4,Y(412)+4),"ρ motor",font=F(13),fill=(255,255,255))

# --- aralik (gap) oku ---
gx=X(br+45)
d.line((gx,Y(402),gx,Y(410)),fill=BLUE,width=2)
d.line((gx-5,Y(402),gx+5,Y(402)),fill=BLUE,width=2); d.line((gx-5,Y(410),gx+5,Y(410)),fill=BLUE,width=2)
d.text((gx+8,(Y(402)+Y(410))//2-9),"aralık ~4–6 mm",font=F(14),fill=BLUE)

# --- theta donme oku (merkez ust) ---
cx0,cy0=X(0),Y(388)
d.arc((cx0-46,cy0-22,cx0+46,cy0+22),200,520,fill=BLUE,width=3)
d.polygon([(cx0+44,cy0-6),(cx0+52,cy0-2),(cx0+42,cy0+6)],fill=BLUE)
d.text((cx0-12,cy0-46),"θ",font=F(22),fill=BLUE)
# --- rho ok (kol boyunca) ---
d.line((X(20),Y(388),X(230),Y(388)),fill=(0,150,80),width=3)
d.polygon([(X(230),Y(388)-6),(X(242),Y(388)),(X(230),Y(388)+6)],fill=(0,150,80))
d.text((X(120),Y(388)-26),"ρ",font=F(22),fill=(0,150,80))

# --- etiketler (sag sutun, leader ile) ---
labels=[
 (276,467,"Temperli cam üst modül (mıknatıslı)"),
 (180,460,"Kum + çelik bilye Ø12"),
 (200,408,"Kum tepsisi tabanı (Al/akrilik ≤4mm, ferromanyetik DEĞİL)"),
 (br+12,398,"N52 mıknatıs (taşıyıcı üstünde)"),
 (br+25,388,"Taşıyıcı = MGN12H araba"),
 (250,379,"MGN12 ray (ρ ekseni)"),
 (250,375,"Dönen kol (Al 5mm)"),
 (75,366,"Lazy-susan / turntable rulman (θ yatak)"),
 (14,367,"Slip ring (ρ motor+endstop kablosu)"),
 (260,358,"Şasi plakası (Al 4mm) — sasi.step"),
 (300,400,"Ahşap gövde (drum)"),
 (254,40,"Ayaklar (4×, 8° splay)"),
]
lx=980; ly=150
d.line((lx-18,140,lx-18,860),fill=(235,235,238),width=1)
for (hx,hh,t) in labels:
    px,py=X(hx),Y(hh)
    d.ellipse((px-4,py-4,px+4,py+4),fill=BLUE)
    d.line((px,py,lx-22,ly+8),fill=(200,205,215),width=1)
    d.text((lx,ly),t,font=F(15,False),fill=INK); ly+=46

# hesap kutusu
d.rounded_rectangle((lx,720,W-30,860),radius=12,outline=(220,220,226),width=2)
d.text((lx+14,732),"Çözünürlük",font=F(16),fill=BLUE)
for i,t in enumerate(["θ: 3200×3 / 360 = 26.667 step/derece  (≈0.16mm @R250)",
                      "ρ: 3200 / 40 = 80 step/mm  (0.0125mm)",
                      "θ redüksiyon 3:1 (GT2 20T→60T) · ρ strok ~250mm"]):
    d.text((lx+14,762+i*30),t,font=F(13,False),fill=INK)

im.save(os.path.join(HERE,"mekanizma_kesit.png"))
print("mekanizma_kesit.png yazildi")
