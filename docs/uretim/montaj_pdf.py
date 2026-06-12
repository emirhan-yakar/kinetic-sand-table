#!/usr/bin/env python3
# IKEA tarzi MONTAJ KILAVUZU PDF olusturur (PIL).
# Onkosul: step1..7.png (seffaf), montaj_patlatma.png, ../../render/room_hero.png
# Calistir: python3 montaj_pdf.py  ->  MONTAJ_KILAVUZU.pdf
import os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
RENDER=os.path.join(HERE,"..","..","render")
W,H=1240,1754  # A4 @150dpi
BLUE=(20,110,220); INK=(28,28,34); MUT=(120,120,130); LINE=(225,225,230)

def font(sz,bold=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else [])+\
             ["/System/Library/Fonts/Supplemental/Arial.ttf","/System/Library/Fonts/Helvetica.ttc"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()

def page():
    im=Image.new("RGB",(W,H),(255,255,255)); return im,ImageDraw.Draw(im)
def paste_fit(im,src,box,white_bg=True):
    x0,y0,x1,y1=box; s=Image.open(src).convert("RGBA")
    bw,bh=x1-x0,y1-y0; sc=min(bw/s.width,bh/s.height); nw,nh=int(s.width*sc),int(s.height*sc)
    s=s.resize((nw,nh)); px=x0+(bw-nw)//2; py=y0+(bh-nh)//2
    if white_bg:
        bg=Image.new("RGBA",(nw,nh),(255,255,255,255)); bg.alpha_composite(s); s=bg
    im.paste(s.convert("RGB"),(px,py))
def header(d,t,sub=""):
    d.rectangle((0,0,W,18),fill=BLUE)
    d.text((60,60),t,font=font(34),fill=INK)
    if sub: d.text((60,108),sub,font=font(19,False),fill=MUT)
    d.line((60,150,W-60,150),fill=LINE,width=2)
def footer(d,n):
    d.line((60,H-70,W-60,H-70),fill=LINE,width=1)
    d.text((60,H-58),"Kinetik Kum Masası · Montaj Kılavuzu",font=font(15,False),fill=MUT)
    d.text((W-90,H-58),str(n),font=font(15),fill=MUT)
def badge(d,x,y,num,r=34):
    d.ellipse((x-r,y-r,x+r,y+r),fill=BLUE)
    f=font(38); tb=d.textbbox((0,0),str(num),font=f)
    d.text((x-(tb[2]-tb[0])/2,y-(tb[3]-tb[1])/2-4),str(num),font=f,fill=(255,255,255))

pages=[]

# ---- KAPAK ----
im,d=page()
d.rectangle((0,0,W,12),fill=BLUE)
d.text((60,150),"KİNETİK KUM",font=font(64),fill=INK)
d.text((60,222),"SANATI MASASI",font=font(64),fill=INK)
d.text((60,310),"Montaj Kılavuzu",font=font(30,False),fill=BLUE)
paste_fit(im,os.path.join(RENDER,"room_hero.png"),(60,380,W-60,1180))
d.text((60,1230),"Ø600 polar (theta-rho) · ayaklı sehpa · 13 parça",font=font(22,False),fill=MUT)
d.text((60,1268),"Montaj öncesi tüm parçaları ve aletleri hazırlayın.",font=font(20,False),fill=MUT)
footer(d,1); pages.append(im)

# ---- PARCALAR ----
im,d=page(); header(d,"PARÇALAR","Patlatılmış görünüm · numaralı parça listesi")
paste_fit(im,os.path.join(HERE,"montaj_patlatma.png"),(40,180,W-40,1300))
d.text((60,1330),"Üst modül (cam+kum) 8× N52 mıknatısla oturur — bakım için elle kalkar.",font=font(19,False),fill=MUT)
footer(d,2); pages.append(im)

# ---- ALETLER ----
im,d=page(); header(d,"GEREKLİ ALETLER")
tools=["Alyan (imbus) anahtar takımı — M3 / M4 / M5 / M6",
       "Yıldız tornavida",
       "Lehim havyası + lehim (kontrol kartı bağlantıları)",
       "Şerit metre / kumpas (kalibrasyon)",
       "Bilgisayar (FluidNC firmware + kalibrasyon)",
       "İnce kuvars kum (~1.5 kg)"]
y=230
for i,t in enumerate(tools,1):
    d.ellipse((70,y-4,94,y+20),fill=BLUE); d.text((76,y-3),str(i),font=font(17),fill=(255,255,255))
    d.text((120,y-4),t,font=font(24,False),fill=INK); y+=70
d.text((60,y+30),"Not: Ayak açısı (8°) eğimli plaka/braketten gelir; elde açı verilmez.",font=font(19,False),fill=MUT)
footer(d,3); pages.append(im)

# ---- ADIMLAR ----
STEP_TXT=[
 ("Mekanizma","θ motor + turntable + dönen kol + ρ motoru şasi plakasına monte et (4× M3, NEMA17 31×31). Slip ring merkeze."),
 ("Taşıyıcı + mıknatıs","Taşıyıcıyı MGN12 arabasına; N52 mıknatısı taşıyıcı cebine tak."),
 ("Kontrol kartı","Kontrol kartını (ESP32 + TMC2209) şasiye 4× M3 standoff ile; motor/LED/endstop kablolarını klemenslere bağla."),
 ("Gövde","Mekanizmayı ahşap gövdenin (drum) içine yerleştir; şasiyi 4× M4 standoff ile sabitle."),
 ("Ayaklar","4 ayağı gövde altına 8° eğimli plakalarla vidala (M6 gömme dişli, PCD Ø420)."),
 ("LED + kum yatağı","WS2812B LED halkayı rim iç kenarına; çelik bilyeyi kuma; üst çerçeveyi yerleştir."),
 ("Cam üst modül","Cam + kum yatağı modülünü 8× N52 mıknatısla rim'e oturt (merkezleme pimleri). Kumu doldur."),
]
for i,(title,txt) in enumerate(STEP_TXT,1):
    im,d=page(); header(d,f"ADIM {i} / 7",title)
    paste_fit(im,os.path.join(HERE,f"step{i}.png"),(40,180,W-40,1180))
    badge(d,110,250,i)
    # aciklama kutusu
    d.rounded_rectangle((60,1240,W-60,1400),radius=16,outline=LINE,width=2)
    # metni sar
    f=font(23,False); words=txt.split(); line=""; yy=1265
    for w in words:
        if d.textlength(line+" "+w,font=f)>W-180: d.text((90,yy),line,font=f,fill=INK); line=w; yy+=38
        else: line=(line+" "+w).strip()
    d.text((90,yy),line,font=f,fill=INK)
    footer(d,3+i); pages.append(im)

# ---- UYARILAR / SON ----
im,d=page(); header(d,"ÖNEMLİ NOTLAR")
notes=["Üst modül güçlü mıknatıslarla tutulur (≈21.6 kgf) — parmak sıkışmasına dikkat.",
       "Kontrol kartı RevB; ilk çalıştırmada bring-up testi yapın (önce motorsuz güç, 5V ölç).",
       "FluidNC kalibrasyonu zorunlu: θ tam tur, ρ menzil/endstop, motor akımı (~0.6–0.9 A).",
       "Desenler .thr (Atatürk imza/spiral) → G-code; SD veya Dune Weaver ile oynatılır.",
       "12V besleme CE'li; sigorta + ters polarite koruması karttadır.",
       "Cam temperli ve rodajlı — kenara dikkat."]
y=230
for t in notes:
    d.ellipse((68,y+2,86,y+20),fill=BLUE)
    f=font(22,False); words=t.split(); line=""; yy=y
    for w in words:
        if d.textlength(line+" "+w,font=f)>W-160: d.text((110,yy),line,font=f,fill=INK); line=w; yy+=34
        else: line=(line+" "+w).strip()
    d.text((110,yy),line,font=f,fill=INK); y=yy+58
d.text((60,y+30),"Detay: docs/uretim/ — montaj.md, URETIM_DOSYASI.md, PCB_inceleme.md",font=font(18,False),fill=MUT)
d.text((60,H-130),"github.com/emirhan-yakar/kinetic-sand-table",font=font(18,False),fill=BLUE)
footer(d,11); pages.append(im)

out=os.path.join(HERE,"MONTAJ_KILAVUZU.pdf")
pages[0].save(out,save_all=True,append_images=pages[1:],resolution=150.0)
print("MONTAJ_KILAVUZU.pdf yazildi:",len(pages),"sayfa",os.path.getsize(out),"byte")
