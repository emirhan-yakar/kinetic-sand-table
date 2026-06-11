#!/usr/bin/env python3
# Workbench render'ina IKEA tarzi numarali callout + lejant bindirir.
import os, json
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(HERE,"montaj_patlatma_labels.json")))
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

# baslik
dr.text((W+24,30),"MONTAJ — PATLATILMIŞ GÖRÜNÜM",font=ftitle,fill=(20,20,28))
dr.line((W+24,70,W+LEGW-24,70),fill=(180,180,190),width=2)

R=19
for L in d["labels"]:
    x,y=int(L["x"]),int(L["y"]); n=L["no"]
    x=max(R+2,min(W-R-2,x)); y=max(R+2,min(H-R-2,y))
    # numara baloncugu
    dr.ellipse((x-R,y-R,x+R,y+R),fill=(20,110,220),outline=(255,255,255),width=3)
    tb=dr.textbbox((0,0),str(n),font=fnum); tw,th=tb[2]-tb[0],tb[3]-tb[1]
    dr.text((x-tw/2,y-th/2-2),str(n),font=fnum,fill=(255,255,255))
    # lejant satiri
    ly=92+(n-1)*30
    dr.ellipse((W+26,ly-2,W+26+22,ly+20),fill=(20,110,220))
    tb=dr.textbbox((0,0),str(n),font=fleg)
    dr.text((W+26+11-(tb[2]-tb[0])/2,ly-1),str(n),font=fleg,fill=(255,255,255))
    dr.text((W+60,ly-1),L["text"],font=fleg,fill=(25,25,32))

dr.text((W+24,H-44),"Ölçüler: montaj_sheet.svg · Vida çizelgesi: montaj.md",font=font(15),fill=(110,110,120))
canvas.save(os.path.join(HERE,"montaj_patlatma.png"))
print("montaj_patlatma.png yazildi", canvas.size)
