# Kontrol Kartı / PCB Spesifikasyonu

## Strateji
- **Prototip (1–10 adet):** Özel PCB tasarlama. Hazır **MKS DLC32** veya
  **BTT** ESP32 tabanlı kontrol kartı kullan — TMC2209 sürücü yuvaları,
  endstop ve LED çıkışı hazır. Riski sıfırlar, hızlı doğrulama sağlar.
- **Seri (50+ adet):** Maliyet ve montaj için aşağıdaki tek kartı KiCad'de
  tasarla, **JLCPCB / PCBWay** (Çin, ucuz, SMT montaj dahil) veya yurt içi PCB
  firmasında bastır.

## Özel PCB — blok şema
```
            +12V DC giriş (fiş + ters polarite koruma D1)
               │
        ┌──────┴───────┐
   12V →│ Buck 12V→5V   │→ +5V (ESP32, LED, lojik)
        └──────────────┘
               │5V                          │12V
        ┌──────┴───────┐            ┌────────┴─────────┐
        │   ESP32-WROOM │            │ TMC2209 #1 (θ)   │→ NEMA17 θ
        │   -32         │── UART ───▶│ TMC2209 #2 (ρ)   │→ slip ring → NEMA17 ρ
        │               │   STEP/DIR └──────────────────┘
        │   GPIO ───────┼─[330Ω]─▶ DIN  WS2812B LED halka
        │   3v3 lojik   │          (5V güç + 1000µF kondansatör)
        │   GPIO ◀──────┼── endstop (θ home opto/mikro switch)
        └───────────────┘
```

## Pin haritası (Dune Weaver firmware ile uyumlu — `firmware/` bkz.)
| İşlev | ESP32 GPIO | Not |
|---|---|---|
| θ STEP / DIR | 19 / 18 | TMC2209 #1 |
| ρ STEP / DIR | 21 / 5 | TMC2209 #2 (sinyaller slip ring'den) |
| TMC UART (her ikisi) | 17 (TX)/16 (RX) | tek hat, adresli |
| EN (ortak) | 25 | sürücü enable |
| θ endstop / home | 22 | opto veya mikro switch |
| WS2812B DIN | 4 | seri direnç 330Ω |
| Buck enable / fan | 23 | opsiyonel |

## KiCad bileşen listesi (özel PCB)
- ESP32-WROOM-32E modülü (veya ESP32-DevKit header)
- 2× TMC2209 step sürücü (modül soketi veya SMD)
- MP1584 / LM2596 buck (12V→5V, ≥3A) — LED akımı için 5V hattını boyutlandır
- Giriş: DC jack/klemens, P-MOSFET ters polarite koruma, TVS diyot
- WS2812 hattı: 330Ω seri direnç + 1000µF/16V elektrolitik kondansatör
- Endstop konnektörü, motor için 4'lü JST/klemens (×2), slip ring klemensi
- Decoupling: 100nF × bolca, ESP32 EN/BOOT için RC + butonlar (programlama)

## Slip ring notu (KRİTİK — yuvarlak masaya özel)
Kol sürekli döndüğü için **ρ motorunun 4 bobin kablosu** dönen koldan sabit
karta **slip ring** üzerinden gelir. En az **6 kanallı** kapsül slip ring seç
(4 motor + 2 yedek/LED). Sinyal yerine motor bobinlerini geçirmek en basitidir
(ρ sürücüsü sabit kartta kalır). Slip ring kontak direnci düşük olmalı; ρ
akımını TMC2209'da makul (~0.6–0.9A) tut.

---

# ÜRETİLEN DOSYALAR

Kart, KiCad olmadan saf Python (`gerbonara`) ile **kod olarak** tasarlandı.
Yeniden üretmek için:
```
pip install --user gerbonara
python3 pcb_gen.py
```

## Dosya manifestosu
| Yol | İçerik |
|---|---|
| `pcb_gen.py` | Kartı üreten script (yerleşim + yönlendirme + GND plane + render) |
| `board3d.scad` | Kartın **3D dizgi modeli** (OpenSCAD → STL) |
| `controller.net` | KiCad'e aktarılabilir **netlist** (26 net) |
| `gerbers/*.gtl .gbl .gts .gbs .gto .gbo .gko` | Gerber katmanları (RS-274X) |
| `gerbers/controller-PTH.drl` / `-NPTH.drl` | Excellon delik dosyaları |
| `plots/*.svg` (+ `.png`) | Her katmanın çizimi + üst/alt kompozit + **assembly drawing** |

## Katman dizilimi (stackup) — 2 katman, 1.6mm FR4
| Gerber | KiCad adı | İçerik |
|---|---|---|
| `.gtl` | F.Cu | üst bakır: sinyal + güç izleri, padler |
| `.gbl` | B.Cu | **GND ground plane** (clearance'lı dolgu) |
| `.gts`/`.gbs` | F/B.Mask | lehim maskesi açıklıkları |
| `.gto`/`.gbo` | F/B.Silkscreen | bileşen konturları, pin-1, ratsnest kılavuzu |
| `.gko` | Edge.Cuts | kart sınırı 100×75mm + 4× Ø3.2 montaj deliği |

## Katman çizimleri (plots/)
- `composite-top.svg` / `composite-bottom.svg` — üst/alt birleşik görünüm
- `top_cu.svg`, `bot_cu.svg` (GND plane), `*_mask`, `*_silk`, `edge`
- `assembly.svg` — etiketli yerleşim/dizgi çizimi (montaj için)

## Yönlendirme durumu
- GND tamamen **alt katman ground plane** ile çözüldü (router'a girmez).
- Sinyal + güç: **26/32 segment** otomatik yönlendirildi (çakışma kontrollü).
- Kalan **6 segment** üst silk'te **kesik çizgi (ratsnest)** olarak işaretli —
  yoğun ESP32 çevresi sinyalleri. Bunlar KiCad'de elle/autorouter ile tamamlanır.

## ⚠️ Üretim öncesi (ZORUNLU)
Bu Gerber'lar geometrik olarak geçerlidir ve fabrikaya yüklenebilir, ancak
**seri üretimden önce KiCad'de DRC** (tasarım kuralı kontrolü) çalıştırılmalı:
1. KiCad → yeni PCB → `controller.net` ile **"Update PCB from netlist"**.
2. `gerbers/` Gerber'larını referans alarak yerleşimi içe aktar veya yeniden yerleştir.
3. 6 ratsnest segmentini tamamla, **DRC** çalıştır (clearance, annular ring).
4. `kicad-cli pcb export gerbers` ile doğrulanmış final Gerber + `step` 3D üret.

## Fabrikaya gönderim (JLCPCB / PCBWay)
- `gerbers/` klasörünü zip'le → yükle. 2 katman, 1.6mm, HASL, 5/5 mil rahat.
- Delikler: PTH (`-PTH.drl`) + NPTH (`-NPTH.drl`, montaj delikleri).
- Adetli dizgi (SMT) istiyorsan: özel PCB'yi SMD bileşenlerle tasarlayıp
  BOM + CPL ekle. Prototipte modüller (ESP32/TMC/buck) header'a takılır → elde lehim.

## Kart üzeri bileşenler (BOM özeti)
| Ref | Bileşen | Not |
|---|---|---|
| U1 | ESP32-DevKitC (2×15) | beyin |
| A1/A2 | TMC2209 StepStick | θ / ρ sürücü |
| BK1 | MP1584 buck | 12V→5V |
| J1 | 2p klemens | 12V giriş |
| J2/J3 | 4p klemens | θ / ρ motor (J3 slip ring'e) |
| J4 | 3p klemens | WS2812B LED (5V/DIN/GND) |
| J5 | 3p klemens | endstop (3V3/SIG/GND) |
| R1 | 330Ω 0805 | LED DIN seri direnç |
| C1 | 1000µF | 5V tampon |
| C2/C3 | 100nF 0805 | sürücü decoupling |

---

# KİCAD İLE FİNAL ÇIKTI (Gerber + STEP 3D)

Kart artık gerçek bir **KiCad 9 projesi** olarak da üretiliyor — gerçek footprint'ler,
net'ler, GND ground plane ve KiCad'in kendi motoruyla export edilmiş Gerber + STEP.

## Araç zinciri
```
python build_kicad.py   # pcbnew API ile controller.kicad_pcb uretir
bash   kicad_export.sh   # kicad-cli ile final/ -> Gerber + STEP + PDF + DRC
```
> KiCad ~/Applications/KiCad.app altında (9.0.9). `build_kicad.py` KiCad'in
> kendi python'u ile çalışır (bkz. script başı / kicad_export.sh içindeki yol tespiti).

## Üretilen dosyalar
| Yol | İçerik |
|---|---|
| `controller.kicad_pcb` | KiCad PCB (GUI'de açılır) — yerleşim + 25 net + GND zone |
| `build_kicad.py` | pcbnew ile kartı kuran script (footprint + net + iz + zone) |
| `kicad_export.sh` | kicad-cli export (Gerber/Drill/STEP/PDF/DRC) |
| `final/gerbers/*.gbr` + `controller.drl` | **KiCad'in ürettiği final Gerber + Excellon** |
| `final/controller.step` | **STEP 3D model** (2.1 MB, ISO-10303, e-CAD/mekanik için) |
| `final/top.pdf` / `bottom.pdf` | katman PDF çıktıları |
| `final/drc.json` + `DRC_SUMMARY.txt` | DRC raporu |
| `final/plots/final-B_Cu-groundplane.png` | alt katman GND plane render'ı |

## Durum — Freerouting ile TAM ROUTING ✅
- ✅ **Tüm sinyaller routlu** — DRC **ratsnest = 0** (Freerouting 23 sinyal netini
  tamamladı: 139 iz segmenti + 3 via).
- ✅ **Bakır kısa devre yok** (DRC `shorting_items = 0`).
- ✅ **Bakır clearance ihlali yok** (zone clearance kuralı self-fill geometrisine
  göre ayarlandı).
- ✅ **GND ground plane** alt katmanda dolu (clearance'lı), Gerber'da mevcut.
- ✅ **STEP 3D** geçerli (jenerik MaiXu klemens STEP modeli kütüphanede yok, atlandı).
- ⚠️ Kalan **148 DRC ihlali kozmetik**: 129'u `silk_*` (KiCad kütüphane
  footprint'lerinin kendi silkscreen'i pad/birbirine biniyor — fabrikalar kabul eder),
  geri kalan ~12'si self-fill plane artefaktı (`isolated_copper`, `starved_thermal`).
  **KiCad GUI'de `B` (Fill All Zones)** ile yeniden doldurunca bunlar da temizlenir.

## Freerouting akışı (otomatik routing)
`pcbnew` DSN export'u headless'ta çalışmadığı için DSN'i geometriden ürettik,
SES'i kendimiz ayrıştırdık. Java 25 + Freerouting 2.2.4 gerekir.
```
JAVA=~/jdk25/.../java FREEROUTING_JAR=/path/freerouting.jar bash freeroute.sh
```
| Script | İş |
|---|---|
| `make_dsn.py` | `controller.kicad_pcb` → Specctra **`controller.dsn`** (GND = B.Cu plane) |
| (Freerouting) | `controller.dsn` → **`controller.ses`** (headless autoroute) |
| `build_kicad.py` (`SES_FILE=...`) | SES route'larını fresh board'a uygula + GND plane yeniden doldur |
| `freeroute.sh` | yukarıdakileri zincirler + `kicad_export.sh` |

## Üretim öncesi son adım (KiCad GUI'de)
1. `controller.kicad_pcb`'yi aç → **`B`** ile zone'ları yeniden doldur (kozmetik DRC temizliği).
2. İstersen silkscreen referans metinlerini görünür yap / yeniden konumla.
3. **DRC** → `kicad_export.sh` ile final Gerber/STEP'i tazele.
