#!/usr/bin/env python3
# .thr (theta-rho) -> kum oluğu YUKSEKLIK HARITASI (heightmap).
# Cikti: render/assets/groove_height.png  (gri: 0.5=duz, koyu=çukur, açık=kenar kabarma)
# Blender displacement bunu kullanir -> bilye gercekten kumu oyar (gercek golge/AO).
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
THR=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,"firmware","patterns","ataturk_signature.thr")
if not os.path.isabs(THR): THR=os.path.join(ROOT,"firmware","patterns",THR)
OUT=os.path.join(HERE,"assets","groove_height.png")

IMG=2048
R_CAP=0.26595        # kum diski yarıçapı (WELL_R*0.985, scene.py ile ayni)
SR=0.245             # desen yarıçapı (WELL_R*0.92)
GROOVE_W=9           # oluk piksel genisligi
BERM_W=17            # kenar kabarma genisligi

def main():
    pts=[]
    for ln in open(THR):
        s=ln.split()
        if len(s)==2:
            try:
                th,rho=float(s[0]),float(s[1])
                x=rho*SR*math.cos(th); y=rho*SR*math.sin(th)
                px=(x/R_CAP*0.5+0.5)*IMG; py=(0.5-y/R_CAP*0.5)*IMG
                pts.append((px,py))
            except: pass
    # taban duz (128). once kenar kabarma (acik), sonra oluk (koyu) ust uste
    im=Image.new("L",(IMG,IMG),128); dr=ImageDraw.Draw(im)
    dr.line(pts,fill=158,width=BERM_W,joint="curve")   # berm (hafif yukari)
    dr.line(pts,fill=70 ,width=GROOVE_W,joint="curve") # oluk (asagi)
    im=im.filter(ImageFilter.GaussianBlur(2.2))        # yumusak profil
    im.save(OUT)
    a=np.asarray(im)
    print("groove_height.png:",IMG,"px  oluk piksel:",int((a<110).sum()),
          " min/max:",a.min(),a.max())

main()
