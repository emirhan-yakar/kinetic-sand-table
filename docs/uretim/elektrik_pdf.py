#!/usr/bin/env python3
# Profesyonel ELEKTRIK MONTAJ & TEST TALIMATI PDF (PIL).
# Onkosul: wiring_diagram.png
import os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
W,H=1240,1754
BLUE=(20,110,220); INK=(28,28,34); MUT=(120,120,130); LINE=(225,225,230); HEAD=(232,238,247)

def font(sz,b=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if b else [])+["/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
def page():
    im=Image.new("RGB",(W,H),(255,255,255)); return im,ImageDraw.Draw(im)
def header(d,t,sub=""):
    d.rectangle((0,0,W,18),fill=BLUE); d.text((60,54),t,font=font(32),fill=INK)
    if sub: d.text((60,100),sub,font=font(18,False),fill=MUT)
    d.line((60,140,W-60,140),fill=LINE,width=2)
def footer(d,n,tot=5):
    d.line((60,H-66,W-60,H-66),fill=LINE,width=1)
    d.text((60,H-54),"Kinetik Kum Masası · Elektrik Montaj & Test Talimatı",font=font(14,False),fill=MUT)
    d.text((W-120,H-54),f"{n} / {tot}",font=font(14),fill=MUT)
def table(d,x,y,cols,rows,header=True,fs=15,rh=40):
    tw=sum(cols)
    for ri,row in enumerate(rows):
        cy=y+ri*rh
        if ri==0 and header: d.rectangle((x,cy,x+tw,cy+rh),fill=HEAD)
        d.rectangle((x,cy,x+tw,cy+rh),outline=LINE,width=1)
        cx=x
        for ci,cell in enumerate(row):
            d.rectangle((cx,cy,cx+cols[ci],cy+rh),outline=LINE,width=1)
            d.text((cx+8,cy+rh//2),str(cell),font=font(fs, ri==0 and header),fill=INK,anchor="lm")
            cx+=cols[ci]
    return y+len(rows)*rh

pages=[]

# ---- p1 KAPAK ----
im,d=page()
d.rectangle((0,0,W,12),fill=BLUE)
d.text((60,180),"ELEKTRİK MONTAJ",font=font(58),fill=INK)
d.text((60,250),"& TEST TALIMATI",font=font(58),fill=INK)
d.text((60,340),"Kinetik Kum Sanatı Masası · Üretim dokümanı",font=font(24,False),fill=BLUE)
d.rounded_rectangle((60,440,W-60,820),radius=16,outline=LINE,width=2)
d.text((90,470),"İçindekiler",font=font(26),fill=INK)
toc=["1 · Bağlantı / harness şeması","2 · Konnektör pinout + slip ring tel haritası",
     "3 · Elektrik montaj adımları (6)","4 · QA / Fonksiyonel test fişi (FCT)"]
for i,t in enumerate(toc):
    d.text((90,540+i*56),t,font=font(22,False),fill=INK)
d.text((60,880),"⚠ 220VAC içerir — mains bağlantıları yetkili tarafından. Topraklama zorunlu. ESD’ye dikkat.",font=font(18,False),fill=(200,60,50))
d.text((60,930),"Materyal/mekanik montaj ayrı: MONTAJ_KILAVUZU.pdf · montaj.md",font=font(18,False),fill=MUT)
footer(d,1); pages.append(im)

# ---- p2 WIRING ----
im,d=page(); header(d,"1 · BAĞLANTI / HARNESS ŞEMASI","Kart ↔ güç · motorlar · slip ring · LED")
w=Image.open(os.path.join(HERE,"wiring_diagram.png")); sc=(W-120)/w.width
w=w.resize((int(w.width*sc),int(w.height*sc))); im.paste(w,(60,180))
d.text((60,200+w.height),"Tel rengi + AWG + net şemada. Slip ring dönen tarafa (ρ motor + endstop) güç/sinyal taşır.",font=font(16,False),fill=MUT)
footer(d,2); pages.append(im)

# ---- p3 PINOUT ----
im,d=page(); header(d,"2 · KONNEKTÖR PINOUT + SLIP RING")
y=table(d,60,180,[120,360,300,300],[
 ["Konnektör","Pin → Net","Tel (renk · AWG)","Gider"],
 ["J1 güç","1=12V 2=GND","kırmızı/siyah · 18","12V SMPS"],
 ["J2 θ motor","1=A1 2=A2 3=B1 4=B2","siyah/yeşil/kırmızı/mavi · 22","NEMA17 θ"],
 ["J3 ρ motor","1=A1 2=A2 3=B1 4=B2","siyah/yeşil/kırmızı/mavi · 22","slip ring → ρ motor"],
 ["J4 LED","1=5V 2=DIN 3=GND","kırmızı/beyaz/siyah · 20","WS2812B (shifter’lı)"],
 ["J5 endstop","1=3V3 2=SİNYAL 3=GND","—/sarı/siyah · 26","slip ring → endstop"],
])
d.text((60,y+24),"Slip ring tel haritası (8 yollu kapsül, ≥2A):",font=font(18),fill=BLUE)
table(d,60,y+56,[160,300,250,250],[
 ["Tel","Sinyal","Stator (baz)","Rotor (kol)"],
 ["W1–W4","ρ A1/A2/B1/B2","J3-1..4","ρ motor"],
 ["W5","endstop sinyal","J5-2","endstop"],
 ["W6","GND (lojik)","J5-3","endstop GND"],
 ["W7,W8","yedek","—","—"],
])
d.text((60,y+56+5*40+20),"NEMA17 bobin çiftlerini ohmmetre ile doğrula (çift ~2–4Ω). LED sabit → slip ring’e girmez.",font=font(15,False),fill=MUT)
footer(d,3); pages.append(im)

# ---- p4 ADIMLAR ----
im,d=page(); header(d,"3 · ELEKTRİK MONTAJ ADIMLARI")
steps=[("SMPS girişi (mains)","220VAC L/N + topraklama(PE) → SMPS; girişe sigorta; ferrül+yalıtım."),
 ("12V → J1","SMPS 12V/GND → J1 (kırmızı/siyah 18AWG). Polarite doğru (ters koruma yedek)."),
 ("θ motor → J2","Bobin çiftlerini ohmmetre ile bul; A1A2/B1B2 sırasıyla bağla."),
 ("Slip ring","Stator W1–W6→J3(4)+J5(2); Rotor W1–W6→ρ motor(4)+endstop(2). Eksene merkezle."),
 ("LED → J4","5V/DIN/GND; DIN level-shifter çıkışından ilk LED’e. 60 LED ~3.6A için 5V hattı yeterli."),
 ("Kablo yönetimi","Kanal+strain relief; dönen kol kablosuna bükülme payı; tümünü etiketle."),]
yy=200
for i,(t,x) in enumerate(steps,1):
    d.ellipse((70,yy,108,yy+38),fill=BLUE); d.text((89,yy+19),str(i),font=font(22),fill=(255,255,255),anchor="mm")
    d.text((130,yy+2),t,font=font(22),fill=INK)
    f=font(17,False); words=x.split(); line=""; ly=yy+38
    for w in words:
        if d.textlength(line+" "+w,font=f)>W-200: d.text((130,ly),line,font=f,fill=(70,70,78)); line=w; ly+=30
        else: line=(line+" "+w).strip()
    d.text((130,ly),line,font=f,fill=(70,70,78)); yy=ly+52
d.text((60,yy+10),"İlk güç verme motorsuz → QA §2 (12V/5V/3V3) → sonra motorları bağla.",font=font(17,False),fill=MUT)
footer(d,4); pages.append(im)

# ---- p5 QA ----
im,d=page(); header(d,"4 · QA / FONKSİYONEL TEST FİŞİ (FCT)","Seri no: ________  Tarih: ______  Operatör: ______  Sonuç: ☐GEÇTİ ☐KALDI")
y=table(d,60,180,[90,470,330,130],[
 ["#","Kontrol","Beklenen / Ölçüm","✓/✗"],
 ["1.2","12V–GND kısa devre (ohm)","> 1 kΩ : ______","☐"],
 ["2.1","J1 giriş gerilimi","11.4–12.6 V : ______","☐"],
 ["2.2","5V rayı (buck)","4.90–5.10 V : ______","☐"],
 ["2.3","3V3 rayı (ESP32)","3.25–3.35 V : ______","☐"],
 ["2.4","Boşta akım (12V)","< 0.30 A : ______","☐"],
 ["3.1","FluidNC açılıyor","banner var","☐"],
 ["4.1","TMC akım/faz","0.6–0.9 A : ______","☐"],
 ["4.2","θ tam tur","kayma yok","☐"],
 ["4.4","ρ homing (endstop)","tetikler/durur","☐"],
 ["5.1","Tüm LED yanıyor","eksik/renk yok","☐"],
 ["6.1","Mıknatıs bilyeyi sürüklüyor","kaçırma yok","☐"],
 ["6.2","Tam desen (imza/spiral)","temiz oluk","☐"],
 ["7.1","24h burn-in","hata/ısınma yok","☐"],
 ["8.1","Üst modül mıknatıs oturuyor","boşluk yok","☐"],
], fs=15, rh=42)
d.text((60,y+20),"Tam fiş: QA_kontrol_listesi.md. Test noktaları: 12V=J1, 5V=BK1, 3V3=ESP32; akım=seri ampermetre.",font=font(15,False),fill=MUT)
d.text((60,y+54),"İmza: ____________________",font=font(18),fill=INK)
footer(d,5); pages.append(im)

out=os.path.join(HERE,"ELEKTRIK_TALIMATI.pdf")
pages[0].save(out,save_all=True,append_images=pages[1:],resolution=150.0)
print("ELEKTRIK_TALIMATI.pdf:",len(pages),"sayfa",os.path.getsize(out),"byte")
