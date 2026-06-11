#!/usr/bin/env python3
# Ataturk imzasi -> tek surekli iz (.thr). Bilye imza CIZGILERINI izler
# (gerisi puruzsuz kum). skeleton + en-yakin-komsu siralama.
import math, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from skimage.morphology import skeletonize

HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,"..","..","render","assets","ataturk_sig.png")
OUT=os.path.join(HERE,"ataturk_signature.thr")
PAD=0.07

def main():
    im=Image.open(SRC)
    ink=im.split()[-1] if im.mode in ("LA","RGBA") else im.convert("L")
    a=np.asarray(ink)
    ys,xs=np.where(a>60); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    ink=ink.crop((x0-8,y0-8,x1+8,y1+8))
    # olcekle (skeleton icin makul cozunurluk) + hafif blur
    W=900; H=int(W*ink.size[1]/ink.size[0])
    ink=ink.resize((W,H)).filter(ImageFilter.GaussianBlur(1.0))
    b=np.asarray(ink)>70
    sk=skeletonize(b)
    pts=np.argwhere(sk)              # (row,col)
    # seyreklestir (hiz + puruzsuzluk)
    if len(pts)>2600:
        idx=np.linspace(0,len(pts)-1,2600).astype(int); pts=pts[idx]
    P=pts[:, ::-1].astype(np.float32)   # (x,y) ekseni
    P[:,1]=H-P[:,1]                     # y yukari

    # en-yakin-komsu siralama (vektorize)
    n=len(P); used=np.zeros(n,bool)
    start=int(np.argmin(P[:,0]))        # en soldan basla
    order=[start]; used[start]=True; cur=start
    for _ in range(n-1):
        d=((P[:,0]-P[cur,0])**2+(P[:,1]-P[cur,1])**2)
        d[used]=1e18; nxt=int(np.argmin(d)); order.append(nxt); used[nxt]=True; cur=nxt
    Q=P[order]

    # daireye sigdir (genis aspect)
    minx,miny=Q.min(0); maxx,maxy=Q.max(0)
    cx,cy=(minx+maxx)/2,(miny+maxy)/2; w=maxx-minx; h=maxy-miny
    aspect=w/h
    ww=aspect/math.sqrt(1+aspect*aspect)*(1-PAD)
    hw=1.0/math.sqrt(1+aspect*aspect)*(1-PAD)
    X=(Q[:,0]-cx)/(w/2)*ww; Y=(Q[:,1]-cy)/(h/2)*hw

    with open(OUT,"w") as f:
        for x,y in zip(X,Y):
            f.write(f"{math.atan2(y,x):.5f} {min(0.985,math.hypot(x,y)):.5f}\n")
    print("ataturk_signature.thr:",len(X),"nokta (iz, aspect %.2f)"%aspect)

    S=760; pv=Image.new("RGB",(S,S),(225,214,190)); dr=ImageDraw.Draw(pv)
    dr.ellipse((6,6,S-6,S-6),outline=(150,140,120),width=3)
    sc=[ (S/2+x*(S/2-14), S/2-y*(S/2-14)) for x,y in zip(X,Y)]
    dr.line(sc,fill=(60,45,30),width=3,joint="curve")
    pv.save(os.path.join(HERE,"ataturk_signature_preview.png")); print("onizleme yazildi")

main()
