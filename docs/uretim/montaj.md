# Montaj Sheet — Kinetik Kum Masası (Ø600, ayaklı sehpa)

Hesaplanmış geometri, açılar, delik konumları, bağlantı çizelgesi ve **mıknatıslı modüler** yapı.
Çizim: **`montaj_sheet.svg`** (ön + üst görünüş, ölçülü). Geometri üreteci: `montaj_hesap.py`.

> Yapı felsefesi: **birbirine geçen + vidalanan** ana gövde; **güçlü mıknatıslarla** ayrılıp
> birleşen **üst modül** (cam + kum yatağı) → bakım için mekanizmaya kolay erişim.

---

## 1) Hesaplanmış ana ölçüler (mm)
| Büyüklük | Değer | Not |
|---|---|---|
| Drum dış çap | **Ø600** | et 18 (ceviz kaplama) |
| Kum havuzu | **Ø540 × derinlik 50** | cidardan 24 içerde |
| Kum yatağı | **Ø516** | |
| Temperli cam | **Ø552 × 6** | rabbet'e oturur |
| Ayak | **4 × 320 mm, 8° splay** | masif ceviz koni |
| Ayak bağlantı dairesi (PCD) | **Ø420** | açılar 45° / 135° / 225° / 315° |
| Ayak ucu temas dairesi | **Ø509** | dışa kaçış 44.5 mm/ayak |
| Ayak dikey izdüşümü | **316.9 mm** | = 320·cos8° |
| **Toplam masa yüksekliği** | **≈ 467 mm** | drum 150 + ayak 316.9 |

## 2) Ayak montajı (açı kritik)
- 4 ayak, **Ø420 PCD** üzerinde 90°'de, her biri **radyal yönde 8° dışa** eğimli.
- Drum alt tablasına **8° eğimli ayak bağlantı plakası** (hazır mobilya plakası ya da CNC freze cep)
  ile vidalanır. Plaka deliği: **4× M5**, 30×30 desen.
- Ahşaba **M6 gömme dişli (threaded insert)** + **M6×30 paslanmaz civata** (plaka üzerinden).
- Ayak ucu yere temas çapı Ø509 → devrilme stabilitesi yüksek (taban/yükseklik ≈ 1.09).

## 3) Mıknatıslı üst modül (bakım erişimi)
Üst modül = **temperli cam + kum yatağı çerçevesi** tek parça; drum rim'ine **mıknatısla** oturur, elle kaldırılır.
| Parametre | Değer |
|---|---|
| Tutucu mıknatıs | **8 × N52 Ø20×3 mm** @ **Ø572 PCD** (45°) |
| Karşı eleman | rim cebinde mıknatıs / modül çerçevesinde **Ø22 × 1.5 DKP saç** karşı plaka |
| Üst modül ağırlığı | **≈ 4.2 kg** (cam 3.6 + çerçeve 0.6) |
| Toplam tutma kuvveti | **≈ 21.6 kgf** |
| **Güvenlik katsayısı** | **≈ 5.2×** (kaldırmaya karşı; yanal kayma için merkezleme pimleri) |
- 2 adet **Ø6 merkezleme pimi** (çelik) modülün yanal kaymasını engeller; mıknatıslar sadece düşey tutar.

## 4) Mekanizma (drum içi, kum yatağının altında)
| Bileşen | Bağlantı / delik | Eleman |
|---|---|---|
| **Şasi plakası** (Al 4mm Ø520) | drum alt tablasına 4× **M4 standoff** @ Ø500 PCD | M4×... + standoff |
| **θ motoru** (NEMA17, merkez) | **31×31 mm kare M3** delik deseni, merkez Ø22 boşluk | 4× M3×8 |
| **Turntable** (lazy-susan Ø150) | şasiye 4× M4; üstüne dönen kol | 4× M4×10 |
| **Dönen kol** (Al 5mm) | turntable'a 4× M3; ucunda ρ motoru + MGN12 ray | M3 |
| **ρ motoru** (NEMA17, kol ucu) | 31×31 M3; kabloları **slip ring** üzerinden | 4× M3×8 |
| **Taşıyıcı + mıknatıs** | MGN12 araba üzerine; N52 Ø20×10 cebe | 2× M3 |
| **Slip ring** | şasi merkezine bilezik; dönen tarafa kelepçe | M3 |
| **Kontrol kartı (PCB)** | şasiye 4× M3 standoff, yan duvara klemensler | 4× M3×6 |
| **LED halka (WS2812B)** | rim iç kenarına yapışkan + 330Ω + 1000µF | — |

## 5) Bağlantı (vida) çizelgesi
| Yer | Eleman | Adet |
|---|---|---|
| Ayak → drum (eğimli plaka) | M6×30 civata + M6 insert | 16 (4/ayak) |
| Şasi → drum tablası | M4×16 + standoff | 4 |
| θ / ρ motor → şasi/kol | M3×8 | 8 |
| Turntable / kol / taşıyıcı | M3–M4 | ~14 |
| PCB standoff | M3×6 | 4 |
| Rim → gövde | M4×16 (gizli) veya ahşap tutkalı + biskü | 8 |
| Üst modül merkezleme | Ø6 çelik pim | 2 |

## 6) Toleranslar & notlar
- Cam–havuz rabbet boşluğu: **+0.5 mm** çevresel (termal/montaj).
- Mıknatıs–çelik hava aralığı (cam altı, kum üstü): bilye sürücü için **toplam ≤ 12 mm**
  (cam 6 + kum 5) → N52 Ø20×10 ~7g bilyeyi rahat sürükler.
- MGN12 ray paralelliği: kol ekseninde **±0.2 mm**.
- Tüm ahşap kesimler CNC; ayak açısı plakadan gelir (elde açı verilmez).
- Topraklama: alüminyum şasi → güç toprağına; LED 5V hattı ayrı buck.

## 7) Montaj sırası
1. Ahşap gövde + rim + kaplama/cila (atölye çıkışı).
2. Ayakları 8° plakalarla drum altına civatala (PCD Ø420).
3. Şasi plakasını drum tablasına standoff'la monte et; θ motoru + turntable + kol + ρ motor + ray + taşıyıcı/mıknatıs + slip ring.
4. Kontrol kartı + kablolama + LED halka + güç.
5. Firmware (Dune Weaver) yükle, **kalibrasyon** (`firmware/README.md`): θ tam tur, ρ menzil, bilye sürükleme.
6. Kum yatağı + cam → mıknatıslı **üst modül** olarak oturt (merkezleme pimleri).
7. Kum doldur, desen (`firmware/patterns/` → Atatürk imzası / spiral) yükle, test.

---
**İlgili dosyalar:** `BOM_uretim.md` (malzeme+fiyat), `montaj_sheet.svg` (çizim),
`montaj_hesap.py` (parametrik geometri — ölçü değişince yeniden üretir),
`../../hardware/pcb/` (kontrol kartı), `../../hardware/sand_table.scad` (3D model).
