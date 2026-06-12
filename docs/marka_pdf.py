#!/usr/bin/env python3
# DEVRAN profesyonel datasheet + pitch one-pager (PIL, acik tema, markali).
# -> DEVRAN_datasheet.pdf , DEVRAN_pitch.pdf
import os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
W,H=1240,1754
INK=(26,28,34); MUT=(110,114,122); ACC=(196,128,52); ACCD=(150,95,40); LINE=(224,224,230); HEAD=(247,242,234)
def F(sz,b=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if b else [])+["/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
MARK=os.path.join(ROOT,"assets","mark.png")
def page(): im=Image.new("RGB",(W,H),(255,255,255)); return im,ImageDraw.Draw(im)
def brandbar(d,im,sub,right=""):
    d.rectangle((0,0,W,8),fill=ACC)
    try:
        m=Image.open(MARK).convert("RGBA").resize((58,58)); im.paste(m,(56,40),m)
    except: pass
    d.text((126,46),"DEVRAN",font=F(40),fill=INK)
    d.text((128,96),sub,font=F(15,False),fill=MUT)
    if right: d.text((W-56,58),right,font=F(20),fill=ACCD,anchor="ra")
    d.line((56,130,W-56,130),fill=LINE,width=2)
def foot(d,t):
    d.line((56,H-70,W-56,H-70),fill=LINE,width=1)
    d.text((56,H-56),t,font=F(13,False),fill=MUT)
    d.text((W-56,H-56),"github.com/emirhan-yakar/kinetic-sand-table",font=F(13,False),fill=ACCD,anchor="ra")
def imgfit(im,src,box):
    x0,y0,x1,y1=box; s=Image.open(src).convert("RGB"); bw,bh=x1-x0,y1-y0
    sc=min(bw/s.width,bh/s.height); s=s.resize((int(s.width*sc),int(s.height*sc)))
    im.paste(s,(x0+(bw-s.width)//2,y0+(bh-s.height)//2))

# ============== DATASHEET ==============
im,d=page(); brandbar(d,im,"Kinetik Kum Sanatı Masası · Teknik Veri Sayfası","Model D60")
imgfit(im,os.path.join(ROOT,"render","room_hero.png"),(56,160,W-56,610))
d.rounded_rectangle((56,160,W-56,610),radius=14,outline=LINE,width=2)
# ozellik bullet'lari
d.text((56,650),"ÖNE ÇIKANLAR",font=F(15),fill=ACCD)
feats=["Sonsuz, tekrarsız kinetik kum deseni — çelik bilye mıknatısla sürüklenir",
 "Sessiz çalışma (TMC2209 sessiz sürüş) · adreslenebilir LED ambiyans",
 "Wi-Fi / WebUI kontrol · SD desen kütüphanesi (.thr) · sınırsız desen",
 "Premium ceviz gövde + temperli cam · Türkiye'de üretilebilir",
 "Açık kaynak yazılım (FluidNC + Dune Weaver)"]
y=685
for t in feats:
    d.ellipse((60,y+5,72,y+17),fill=ACC); d.text((86,y),t,font=F(16,False),fill=INK); y+=38
# spec tablosu
d.text((56,y+18),"TEKNİK ÖZELLİKLER",font=F(15),fill=ACCD); y+=48
specs=[("Genel boyut","Ø600 mm × H 467 mm"),("Çalışma alanı","Ø540 kum havuzu"),
 ("Ağırlık","≈ 14 kg"),("Mekanizma","Polar (θ-ρ) · dönen kol + MGN12 taşıyıcı"),
 ("Çözünürlük","θ ≈ 0.16 mm @R250 · ρ 0.0125 mm"),("Tahrik","2× NEMA17 + TMC2209"),
 ("Manyetik kuplaj","N52 mıknatıs · çelik bilye Ø12"),("Kontrol","ESP32 + FluidNC (WebUI)"),
 ("LED","WS2812B adreslenebilir halka (60)"),("Cam","Temperli Ø552 × 6 mm"),
 ("Gövde / ayak","Ceviz kaplama / masif ceviz (8° splay)"),("Güç","12V DC · CE'li adaptör"),
 ("Desen formatı",".thr (theta-rho) → G-code"),("Üretim","Türkiye")]
colw=(W-112)//2
for i,(k,v) in enumerate(specs):
    cx=56+(i%2)*colw; cy=y+(i//2)*42
    d.rectangle((cx,cy,cx+colw,cy+42),outline=LINE,width=1)
    if i%2==0 or True: pass
    d.text((cx+12,cy+21),k,font=F(13),fill=MUT,anchor="lm")
    d.text((cx+colw-12,cy+21),v,font=F(13,False),fill=INK,anchor="rm")
foot(d,"Teknik veriler ön tasarıma aittir · fiziksel doğrulama (prototip) önerilir.")
im.save(os.path.join(HERE,"DEVRAN_datasheet.pdf"),resolution=150.0)
print("DEVRAN_datasheet.pdf")

# ============== PITCH ==============
pages=[]
im,d=page(); brandbar(d,im,"Kinetik Kum Sanatı Masası · İş / Yatırım Özeti","Pitch")
def block(d,y,t,body,h=130):
    d.rounded_rectangle((56,y,W-56,y+h),radius=12,outline=LINE,width=2)
    d.text((76,y+16),t,font=F(18),fill=ACCD)
    f=F(16,False); ln=""; yy=y+50
    for w in body.split():
        if d.textlength(ln+" "+w,font=f)>W-150: d.text((76,yy),ln,font=f,fill=INK); ln=w; yy+=30
        else: ln=(ln+" "+w).strip()
    d.text((76,yy),ln,font=f,fill=INK); return y+h+18
y=160
y=block(d,y,"PROBLEM","Premium kinetik sanat masaları pahalı ($699+) ve çoğunlukla ithal; Türkiye'de yerli üretilen, tasarım odaklı, açık yazılımlı bir alternatif yok.")
y=block(d,y,"ÇÖZÜM — DEVRAN","Yerli üretilebilen, premium ceviz + temperli cam gövdeli, sessiz polar mekanizmalı kinetik kum sanatı masası. Wi-Fi/WebUI, sınırsız desen, ambiyans LED.")
y=block(d,y,"PAZAR","Premium ev dekoru · tasarım objesi · kurumsal hediye · ofis/lobi. Benzer ürün $699; artan kinetik-sanat ilgisi.",110)
y=block(d,y,"İŞ MODELİ & BİRİM EKONOMİ","Doğrudan satış (D2C) + butik tasarım/mobilya kanalları. Seri COGS ≈ 7.800 TL → MSRP ≈ 21.900 TL (~$650), brüt marj ~%64. Yazılım açık kaynak (0 TL).",130)
y=block(d,y,"DURUM & YOL HARİTASI","Tam mühendislik paketi hazır (PCB Rev-B, mekanizma, BOM, montaj, firmware). Sıradaki: prototip → CE belgesi → küçük seri (PVT) → satış.",130)
y=block(d,y,"TALEP","Ortaklık / yatırım / üretim iş birliği. Tüm tasarım açık kaynak — repo'da incelenebilir.",90)
foot(d,"DEVRAN · açık kaynak üretim paketi")
im.save(os.path.join(HERE,"DEVRAN_pitch.pdf"),resolution=150.0)
print("DEVRAN_pitch.pdf")
