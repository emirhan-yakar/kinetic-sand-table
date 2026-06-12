#!/usr/bin/env python3
# Workbench render'ina IKEA tarzi numarali callout + lejant bindirir.
# Kullanim: python3 montaj_label.py [labels.json]
import os, json, sys
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
JF=sys.argv[1] if len(sys.argv)>1 else "montaj_patlatma_labels.json"
d=json.load(open(os.path.join(HERE,JF)))
TITLE=d.get("title","MONTAJ — PATLATILMIŞ GÖRÜNÜM")
OUTNAME=d["img"].replace("_raw","")
img=Image.open(os.path.join(HERE,d["img"])).convert("RGB")
W,H=img.size
LEGW=360
canvas=Image.new("RGB",(W+LEGW,H),(255,255,255)); canvas.paste(img,(0,0))
dr=ImageDraw.Draw(canvas)
def font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf","/System/Library/Fonts/Helvetica.ttc"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
fnum=font(22); fleg=font(20); ftitle=font(26)

# montaj ekseni (dash-dot) - parcalarin altinda
ax=d.get("axis")
if ax:
    (ax0,ay0),(ax1,ay1)=ax; import math
    L=math.hypot(ax1-ax0,ay1-ay0); ux,uy=(ax1-ax0)/L,(ay1-ay0)/L; t=0
    while t<L:
        seg=18 if int(t/18)%2==0 else 2   # uzun-kisa (dash-dot benzeri)
        x0=ax0+ux*t; y0=ay0+uy*t; x1=ax0+ux*min(t+seg,L); y1=ay0+uy*min(t+seg,L)
        dr.line((x0,y0,x1,y1),fill=(150,160,180),width=2); t+=seg+8

# baslik
dr.text((W+24,30),TITLE,font=ftitle,fill=(20,20,28))
dr.text((W+24,64),"parçalar montaj ekseni boyunca dizilir",font=font(14),fill=(140,140,150))
dr.line((W+24,88,W+LEGW-24,88),fill=(180,180,190),width=2)

R=19
for L in d["labels"]:
    x,y=int(L["x"]),int(L["y"]); n=L["no"]
    x=max(R+2,min(W-R-2,x)); y=max(R+2,min(H-R-2,y))
    # numara baloncugu
    dr.ellipse((x-R,y-R,x+R,y+R),fill=(20,110,220),outline=(255,255,255),width=3)
    tb=dr.textbbox((0,0),str(n),font=fnum); tw,th=tb[2]-tb[0],tb[3]-tb[1]
    dr.text((x-tw/2,y-th/2-2),str(n),font=fnum,fill=(255,255,255))
    # lejant satiri
    ly=104+(n-1)*30
    dr.ellipse((W+26,ly-2,W+26+22,ly+20),fill=(20,110,220))
    tb=dr.textbbox((0,0),str(n),font=fleg)
    dr.text((W+26+11-(tb[2]-tb[0])/2,ly-1),str(n),font=fleg,fill=(255,255,255))
    dr.text((W+60,ly-1),L["text"],font=fleg,fill=(25,25,32))

dr.text((W+24,H-44),"Ölçüler: montaj_sheet.svg · Vida çizelgesi: montaj.md",font=font(15),fill=(110,110,120))
canvas.save(os.path.join(HERE,OUTNAME))
print(OUTNAME,"yazildi", canvas.size)
