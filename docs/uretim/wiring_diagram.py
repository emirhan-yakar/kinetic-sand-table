#!/usr/bin/env python3
# Profesyonel BAGLANTI / HARNESS semasi (PIL). -> wiring_diagram.png
# Kart <-> 12V SMPS / theta motor / slip ring -> rho motor + endstop / LED.
import os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
W,H=1560,1080
im=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(im)
def F(sz,b=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if b else [])+["/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
INK=(28,28,34); MUT=(120,120,130); BLUE=(20,110,220)
RED=(210,55,45); BLK=(40,40,46); GRN=(35,150,70); BLU=(40,90,210); YEL=(225,180,30); WHT=(180,180,186)

def box(x0,y0,x1,y1,fill=(245,247,250),outline=INK,wd=2,r=10):
    d.rounded_rectangle((x0,y0,x1,y1),radius=r,fill=fill,outline=outline,width=wd)
def label(x,y,t,f=None,fill=INK,anchor="la"):
    d.text((x,y),t,font=f or F(16,False),fill=fill,anchor=anchor)
def wires(p0,p1,cols,lbl="",dx=0):
    # paralel renkli teller
    n=len(cols); x0,y0=p0; x1,y1=p1
    for i,c in enumerate(cols):
        off=(i-(n-1)/2)*7
        d.line((x0,y0+off,x1,y1+off),fill=c,width=4)
    if lbl: label((x0+x1)//2+dx,min(y0,y1)-26,lbl,F(14,True),MUT,"ma")

d.text((40,30),"BAĞLANTI / HARNESS ŞEMASI",font=F(30),fill=INK)
d.text((40,72),"Kontrol kartı ↔ güç · motorlar · slip ring · LED   (tel rengi + AWG + net)",font=F(17,False),fill=MUT)

# ---- KART ----
bx0,by0,bx1,by1=590,430,970,700
box(bx0,by0,bx1,by1,(238,242,248),BLUE,3,14)
label((bx0+bx1)//2,by0+18,"KONTROL KARTI",F(20),INK,"ma")
label((bx0+bx1)//2,by0+46,"ESP32 + 2× TMC2209 (Rev-B)",F(14,False),MUT,"ma")
def conn(x,y,ref,fn):
    d.rectangle((x-26,y-13,x+26,y+13),fill=(255,255,255),outline=INK,width=2)
    label(x,y,ref,F(14),INK,"mm");
J1=(bx0+120,by0); J2=(bx0,by0+90); J3=(bx1,by0+90); J5=(bx1,by0+190); J4=(bx0+200,by1)
for p,r in [(J1,"J1"),(J2,"J2"),(J3,"J3"),(J5,"J5"),(J4,"J4")]: conn(p[0],p[1],r,"")

# ---- 12V SMPS ----
box(560,170,820,290); label(690,196,"12V 6A SMPS",F(19),INK,"ma"); label(690,230,"(CE’li, sigortalı)",F(14,False),MUT,"ma")
label(690,258,"220VAC → 12VDC",F(13,False),MUT,"ma")
wires((690,290),(J1[0],J1[1]),[RED,BLK],"12V / GND · 18AWG")
label(J1[0]+40,J1[1]-60,"J1: 1=12V(kırmızı) 2=GND(siyah)",F(12,False),MUT)

# ---- THETA motor ----
box(120,470,360,610); label(240,498,"NEMA17 — θ",F(19),INK,"ma"); label(240,532,"dönen kol tahriki",F(13,False),MUT,"ma"); label(240,558,"GT2 3:1",F(13,False),MUT,"ma")
wires((360,540),(J2[0],J2[1]),[BLK,GRN,RED,BLU],"A1 A2 B1 B2 · 22AWG")
label(120,624,"J2: 1=A1(siyah) 2=A2(yeşil) 3=B1(kırmızı) 4=B2(mavi)",F(12,False),MUT)

# ---- SLIP RING + RHO + ENDSTOP ----
sx0,sy0,sx1,sy1=1080,430,1320,540
box(sx0,sy0,sx1,sy1,(244,238,250),(150,120,200),3); label((sx0+sx1)//2,sy0+22,"SLIP RING",F(19),INK,"ma")
label((sx0+sx1)//2,sy0+54,"kapsül · 8 yol · ≥2A",F(13,False),MUT,"ma"); label((sx0+sx1)//2,sy0+80,"(dönen tarafa)",F(13,False),MUT,"ma")
wires((J3[0],J3[1]),(sx0,sy0+40),[BLK,GRN,RED,BLU],"ρ motor 4 tel",dx=-30)
wires((J5[0],J5[1]),(sx0,sy0+90),[YEL,BLK],"endstop 2 tel",dx=-20)
box(1080,580,1320,690); label(1200,606,"NEMA17 — ρ",F(19),INK,"ma"); label(1200,640,"taşıyıcı (kolda)",F(13,False),MUT,"ma"); label(1200,666,"MGN12 + GT2",F(12,False),MUT,"ma")
wires((1200,540),(1200,580),[BLK,GRN,RED,BLU])
box(1080,730,1320,820); label(1200,756,"ENDSTOP (ρ home)",F(16),INK,"ma"); label(1200,788,"merkez referans",F(13,False),MUT,"ma")
wires((1150,540),(1150,730),[YEL,BLK])
label(980,360,"J3→slip ring→ρ motor · J5→slip ring→endstop",F(12,False),MUT)

# ---- LED ----
box(560,860,860,960); label(710,886,"WS2812B LED halka",F(18),INK,"ma"); label(710,920,"60 LED · rim içi (SABİT)",F(13,False),MUT,"ma")
wires((J4[0],J4[1]),(710,860),[RED,WHT,BLK],"5V / DIN / GND · 20AWG")
label(J4[0]-40,J4[1]+30,"J4: 1=5V 2=DIN(level-shift’li) 3=GND",F(12,False),MUT)

# ---- LEGEND ----
lx,ly=40,150
box(lx,ly,lx+330,ly+250,(250,250,252),(225,225,230),1)
label(lx+16,ly+12,"TEL RENK KODU",F(15),BLUE)
leg=[("Kırmızı","12V / 5V (+)",RED),("Siyah","GND / A1",BLK),("Yeşil","A2",GRN),
     ("Kırmızı","B1",RED),("Mavi","B2",BLU),("Sarı","endstop sinyal",YEL),("Beyaz","LED DIN",WHT)]
yy=ly+44
for c,t,col in leg:
    d.line((lx+18,yy+8,lx+54,yy+8),fill=col,width=5); label(lx+66,yy,f"{c} — {t}",F(13,False),INK); yy+=27
label(lx+16,ly+230,"AWG: güç 18–20, motor 22, sinyal 26",F(12,False),MUT)

im.save(os.path.join(HERE,"wiring_diagram.png")); print("wiring_diagram.png yazildi")
