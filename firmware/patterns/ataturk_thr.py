#!/usr/bin/env python3
# Goruntu -> theta-rho (.thr) : dalgali tarama cizgisi portre.
# Karanlik bolgelerde dalga genligi/yogunlugu artar -> sürekli TEK cizgiyle
# taranabilir portre (gercek kum masasinin yapabilecegi geometrik teknik).
import sys, math, os
import numpy as np
from PIL import Image, ImageOps, ImageFilter

HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,"..","..","render","assets","ataturk_src.jpg")
OUT=os.path.join(HERE,"ataturk.thr")

# --- ayarlar ---
ROWS=160          # tarama satiri
XRES=210          # satir basina ornek
CYCLES=30         # genislik boyunca dalga sayisi (yogunluk)
CROP=(0.26,0.02,0.72,0.46)   # (l,t,r,b) portre-oran, yuz odakli
SCALE=1.26        # deseni daireye yay (tam otursun)

def main():
    im=Image.open(SRC).convert("L")
    W,H=im.size
    l,t,r,b=CROP
    im=im.crop((int(l*W),int(t*H),int(r*W),int(b*H)))
    im=ImageOps.autocontrast(im,cutoff=2)
    # yerel kontrast (clarity): yuz ici ozellikler (goz/kas/burun/agiz) belirginlesir
    im=im.filter(ImageFilter.UnsharpMask(radius=14,percent=240,threshold=1))
    im=im.resize((XRES,ROWS),Image.LANCZOS)
    a=np.asarray(im,dtype=np.float32)/255.0
    dark=1.0-a                 # 0(acik)..1(koyu)
    lo,hi=np.percentile(dark,5),np.percentile(dark,95)
    dark=np.clip((dark-lo)/(hi-lo+1e-6),0,1)**1.35

    # daireye sigan dikdortgen (tum noktalar rho<=1)
    aspect=(r-l)*W/((b-t)*H)   # w/h
    hw=1.0/math.sqrt(1.0+1.0/(aspect*aspect))   # yari-yukseklik birimi (R=1)
    ww=hw*aspect
    bandH=2*hw/ROWS

    pts=[]
    for i in range(ROWS):
        yc=hw - (i+0.5)*bandH
        cols=range(XRES) if i%2==0 else range(XRES-1,-1,-1)  # boustrophedon
        for c in cols:
            x=(c/(XRES-1)-0.5)*2*ww
            d=dark[i,c]
            amp=bandH*0.66*d
            ph=(c/(XRES-1))*2*math.pi*CYCLES
            y=yc+amp*math.sin(ph)
            pts.append((x*SCALE,y*SCALE))

    with open(OUT,"w") as f:
        for x,y in pts:
            th=math.atan2(y,x); rho=min(0.985,math.hypot(x,y))
            f.write(f"{th:.5f} {rho:.5f}\n")
    print("ataturk.thr:",len(pts),"nokta  (aspect %.2f)"%aspect)

    # --- onizleme (kum yuzeyi gibi) ---
    from PIL import ImageDraw
    S=760; prev=Image.new("RGB",(S,S),(225,214,190)); dr=ImageDraw.Draw(prev)
    dr.ellipse((6,6,S-6,S-6),outline=(150,140,120),width=3)
    def px(x,y): return (S/2+x*(S/2-14), S/2-y*(S/2-14))
    xy=[px(x,y) for x,y in pts]
    dr.line(xy,fill=(70,55,38),width=1,joint="curve")
    prev.save(os.path.join(HERE,"ataturk_preview.png"))
    print("onizleme: ataturk_preview.png")

main()
