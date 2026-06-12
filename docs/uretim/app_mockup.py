#!/usr/bin/env python3
# DEVRAN companion uygulama UX mockup (3 telefon ekrani). PIL. -> app_mockup.png
import os, math
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
BG=(238,239,242); SCR=(20,23,29); CARD=(31,36,45); INK=(238,240,243); MUT=(150,156,166)
ACC=(227,165,91); ACC2=(240,195,137); GOOD=(95,207,134)
W,H=1560,920
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
def F(sz,b=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if b else [])+["/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
def phone(x,y,w=400,h=820):
    d.rounded_rectangle((x,y,x+w,y+h),radius=44,fill=SCR,outline=(60,66,76),width=3)
    d.rounded_rectangle((x+18,y+18,x+w-18,y+h-18),radius=30,fill=SCR)
    d.rounded_rectangle((x+w/2-46,y+24,x+w/2+46,y+40),radius=8,fill=(10,12,16))  # notch
    return x+18,y+44,w-36
def header(ox,top,wd,title):
    d.text((ox+18,top+8),title,font=F(22),fill=INK)
    d.ellipse((ox+wd-44,top+6,ox+wd-18,top+32),outline=ACC,width=2)
def navbar(ox,top,wd,h,active=0):
    yy=top+h-100; d.line((ox,yy,ox+wd,yy),fill=(45,50,60),width=1)
    icons=["▷","▦","◐","⚙"]
    for i,ic in enumerate(icons):
        cx=ox+wd*(i+0.5)/4
        d.text((cx,yy+34),ic,font=F(26),fill=ACC if i==active else MUT,anchor="mm")

d.text((50,30),"DEVRAN — Companion Uygulaması (UX konsept)",font=F(30),fill=(28,30,36))
d.text((50,72),"FluidNC + Dune Weaver üstüne markalı kabuk · OTA ile zenginleşir",font=F(17,False),fill=(110,114,122))

P=[("Şimdi Oynuyor",0),("Desen Kütüphanesi",1),("Sahneler & Zamanlama",2)]
x0=120
for idx,(title,act) in enumerate(P):
    ox,top,wd=phone(x0+idx*470,110)
    header(ox,top,wd,title); navbar(ox,top,wd,820,act)
    cy=top+70
    if idx==0:  # now playing
        ccx,ccy,R=ox+wd/2,cy+180,150
        d.ellipse((ccx-R,ccy-R,ccx+R,ccy+R),fill=CARD,outline=(50,56,66),width=2)
        # spiral desen
        pts=[];th=0
        while th<5*math.pi:
            r=R*0.82*th/(5*math.pi); pts.append((ccx+r*math.cos(th),ccy+r*math.sin(th))); th+=0.15
        d.line(pts,fill=ACC2,width=3)
        d.ellipse((pts[-1][0]-4,pts[-1][1]-4,pts[-1][0]+4,pts[-1][1]+4),fill=(255,255,255))
        d.text((ox+wd/2,ccy+R+34),"Atatürk İmzası",font=F(20),fill=INK,anchor="mm")
        d.text((ox+wd/2,ccy+R+62),"sonsuz desen · θ-ρ",font=F(14,False),fill=MUT,anchor="mm")
        # progress
        py=ccy+R+100; d.rounded_rectangle((ox+24,py,ox+wd-24,py+8),radius=4,fill=(45,50,60))
        d.rounded_rectangle((ox+24,py,ox+24+(wd-48)*0.62,py+8),radius=4,fill=ACC)
        # controls
        d.text((ox+wd/2,py+70),"⏸",font=F(46),fill=INK,anchor="mm")
        d.text((ox+24,py+120),"Hız",font=F(14,False),fill=MUT)
        d.rounded_rectangle((ox+80,py+118,ox+wd-24,py+126),radius=4,fill=(45,50,60))
        d.rounded_rectangle((ox+80,py+118,ox+80+(wd-104)*0.5,py+126),radius=4,fill=ACC2)
        d.ellipse((ox+80+(wd-104)*0.5-7,py+115,ox+80+(wd-104)*0.5+7,py+129),fill=ACC2)
    elif idx==1:  # library
        d.rounded_rectangle((ox+24,cy,ox+wd-24,cy+40),radius=20,fill=CARD)
        d.text((ox+40,cy+10),"🔍  desen ara…",font=F(16,False),fill=MUT)
        names=["Spiral","İmza","Gül","Dalga","Mandala","Labirent"]
        gy=cy+70
        for i,nm in enumerate(names):
            gx=ox+24+(i%2)*(wd-48)/2+ (i%2)*8; gw=(wd-64)/2
            gx=ox+24+(i%2)*((wd-40)/2);
            cyy=gy+(i//2)*150
            d.rounded_rectangle((gx,cyy,gx+gw,cyy+130),radius=16,fill=CARD)
            mcx,mcy=gx+gw/2,cyy+52
            pts=[];th=0;turns=2+i*0.4
            while th<turns*2*math.pi:
                r=34*th/(turns*2*math.pi); pts.append((mcx+r*math.cos(th),mcy+r*math.sin(th))); th+=0.2
            d.line(pts,fill=ACC2 if i==1 else (170,176,186),width=2)
            d.text((mcx,cyy+104),nm,font=F(15),fill=INK,anchor="mm")
    else:  # scenes/schedule
        d.text((ox+24,cy),"LED Sahnesi",font=F(16),fill=MUT)
        sw=[ACC,(95,150,230),(120,200,140),(220,120,200),(240,240,240)]
        for i,c in enumerate(sw):
            sx=ox+24+i*((wd-48)/5)
            d.rounded_rectangle((sx,cy+30,sx+(wd-48)/5-10,cy+74),radius=12,fill=c,
                                outline=INK if i==0 else None,width=2)
        d.text((ox+24,cy+96),"Parlaklık (loş)",font=F(14,False),fill=MUT)
        d.rounded_rectangle((ox+24,cy+122,ox+wd-24,cy+130),radius=4,fill=(45,50,60))
        d.rounded_rectangle((ox+24,cy+122,ox+24+(wd-48)*0.28,cy+130),radius=4,fill=ACC)
        d.text((ox+24,cy+165),"ZAMANLAMA",font=F(14),fill=ACC2)
        rows=[("19:00","Loş + Yavaş","açık"),("23:30","Uyku","açık"),("08:00","Uyanış","kapalı")]
        ry=cy+200
        for t,lbl,st in rows:
            d.rounded_rectangle((ox+24,ry,ox+wd-24,ry+64),radius=14,fill=CARD)
            d.text((ox+42,ry+12),t,font=F(20),fill=INK); d.text((ox+42,ry+40),lbl,font=F(13,False),fill=MUT)
            on= st=="açık"
            d.rounded_rectangle((ox+wd-86,ry+20,ox+wd-44,ry+44),radius=12,fill=GOOD if on else (60,66,76))
            d.ellipse((ox+wd-66 if on else ox+wd-84,ry+22,ox+wd-46 if on else ox+wd-64,ry+42),fill=(255,255,255))
            ry+=80

im.save(os.path.join(HERE,"app_mockup.png")); print("app_mockup.png yazildi")
