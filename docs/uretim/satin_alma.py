#!/usr/bin/env python3
# Prototip satin-alma listesi -> satin_alma.csv (siparis/takip) + markdown tablo + toplam.
# Fiyatlar 2026 TR tahmini; siparis aninda DOGRULA.
import csv, os
HERE=os.path.dirname(os.path.abspath(__file__))

# (kategori, parca, spesifikasyon, adet, tedarikci, birim_TL, termin)
ITEMS=[
 ("Elektronik","Kontrol kartı PCB+SMT dizgi","Rev-B, 5 adet (yedekli)",1,"JLCPCB/PCBWay",1600,"1–2 hafta"),
 ("Elektronik","ESP32-DevKitC modülü","ön-sertifikalı, WROOM-32",1,"Robotistan/Motorobit",170,"2–4 gün"),
 ("Elektronik","TMC2209 sürücü modülü","StepStick, UART",2,"Robotistan/Motorobit",125,"2–4 gün"),
 ("Elektronik","Buck konvertör 12→5V","≥5A (LED için)",1,"Robotistan",90,"2–4 gün"),
 ("Elektronik","Klemens/header/jumper sarf","2.54mm + 5mm klemens set",1,"Direnç.net/Robotistan",160,"2–4 gün"),
 ("Motor & hareket","NEMA17 step motor","1.8°, ~0.4 N·m",2,"Robotistan",260,"2–4 gün"),
 ("Motor & hareket","MGN12 ray + araba","~300 mm + MGN12H",1,"lineer hareket satıcı",470,"3–7 gün"),
 ("Motor & hareket","Lazy-susan/turntable rulman","Ø100–150",1,"yatak/robotik",160,"3–7 gün"),
 ("Motor & hareket","GT2 kayış+kasnak seti","6mm kayış 2m + 20T×2 + 60T + idler",1,"Robotistan",260,"2–4 gün"),
 ("Motor & hareket","Kapsül slip ring","Ø12.5 · 8–12 yol · ≥2A",1,"otomasyon/Aliexpress",360,"1–3 hafta"),
 ("Motor & hareket","Endstop","mekanik/opto + kablo",1,"Robotistan",35,"2–4 gün"),
 ("Mıknatıs & bilye","N52 mıknatıs taşıyıcı","Ø20×10",3,"yurtiçi neodyum",45,"3–7 gün"),
 ("Mıknatıs & bilye","N52 mıknatıs üst modül","Ø20×3",8,"yurtiçi neodyum",26,"3–7 gün"),
 ("Mıknatıs & bilye","Krom çelik bilye","Ø12",5,"rulman/bilye satıcı",12,"3–7 gün"),
 ("Güç","12V SMPS (CE'li)","≥6A, kapalı kasa",1,"Samm/Robotistan",320,"2–5 gün"),
 ("Güç","Güç kablosu + fiş","topraklı, IEC",1,"elektrik malz.",60,"2–5 gün"),
 ("LED","WS2812B adreslenebilir","60 LED halka/şerit",1,"Samm/LED Pazarı",210,"2–5 gün"),
 ("Ahşap","Ceviz kaplama gövde (CNC)","drum Ø600, kesim+kaplama (prototip tek)",1,"yerel CNC ahşap atölyesi",3200,"1–2 hafta"),
 ("Ahşap","Masif ceviz ayak (torna)","8° eğimli, L320",4,"ahşap torna/mobilya",200,"1–2 hafta"),
 ("Ahşap","Lake / finiş","mat koruyucu",1,"boya malz.",300,"—"),
 ("Cam","Temperli cam Ø552×6","low-iron, rodajlı",1,"yerel temperli cam",800,"1 hafta"),
 ("Alüminyum","Al lazer kesim (DXF)","şasi Ø520 + kol + 4 ayak plakası",1,"sac/Al lazer atölyesi",750,"3–7 gün"),
 ("Bağlantı/sarf","Vida/somun/standoff/insert","M3/M4/M5/M6 set + gömme dişli",1,"hırdavat/Robotistan",260,"2–5 gün"),
 ("Bağlantı/sarf","Kablo yönetimi","kanal, spiral, ferrül, etiket",1,"elektrik malz.",150,"2–5 gün"),
]
# kum ayrica
ITEMS.append(("Sarf","İnce kuvars kum","~1.5 kg",1,"hobi/akvaryum",80,"2–5 gün"))

rows=[]; total=0
for kat,parca,spec,adet,ted,birim,term in ITEMS:
    tutar=adet*birim; total+=tutar
    rows.append([kat,parca,spec,adet,ted,birim,tutar,term,"sipariş edilecek"])

with open(os.path.join(HERE,"satin_alma.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Kategori","Parça","Spesifikasyon","Adet","Tedarikçi","Birim_TL","Toplam_TL","Termin","Durum"])
    w.writerows(rows)
    w.writerow(["","","","","","MALZEME TOPLAM",total,"",""])

print(f"satin_alma.csv yazildi · {len(rows)} kalem · malzeme toplam {total:,} TL".replace(",","."))
# kategori ozet
from collections import OrderedDict
cat=OrderedDict()
for r in rows: cat[r[0]]=cat.get(r[0],0)+r[6]
for k,v in cat.items(): print(f"  {k}: {v:,} TL".replace(",","."))
