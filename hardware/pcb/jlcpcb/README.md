# JLCPCB Üretim Paketi — Rev-B

Kontrol kartını **JLCPCB**'de (veya PCBWay) üretip dizdirmek için hazır dosyalar.

> ⚠️ **Bu Rev-B tasarımıdır — fiziksel olarak henüz test EDİLMEDİ.** Üretim öncesi
> bir donanımcının son incelemesi önerilir (`../../../docs/uretim/PCB_inceleme.md`).
> İlk siparişte **5 adet** (yedekli) öneririz.

## Dosyalar
| Dosya | Ne |
|---|---|
| `gerbers_revB.zip` | Fab dosyaları (Gerber + Excellon) — JLCPCB "Add gerber file" |
| `BOM_jlcpcb.csv` | SMD dizgi malzeme listesi (Comment, Designator, Footprint, LCSC) |
| `CPL_jlcpcb.csv` | Pick & place konumları (Designator, Mid X/Y, Layer, Rotation) |
| `pos_raw.csv` | KiCad ham pozisyon (ara dosya) |

## JLCPCB akışı
1. **PCB:** gerbers_revB.zip yükle → 2 katman, 1.6mm, HASL (veya ENIG). Önizlemede kontrol et.
2. **Assembly (SMT):** "PCB Assembly" aç → **BOM_jlcpcb.csv** + **CPL_jlcpcb.csv** yükle.
3. **Parça eşleştir:** her satır LCSC ile eşleşmeli. `DOGRULA` yazan 3 parça (aşağıda) JLCPCB
   kütüphanesinden seçilmeli. Diğerleri (R/C/Q1) yaygın Basic parçalar.
4. **Rotation/önizleme:** JLCPCB dizgi önizlemesinde **her parçanın dönüşünü kontrol et**
   (KiCad↔JLCPCB rotasyon farkı olabilir — özellikle SOT-23/SOT-23-5 ve polariteli D1).
5. Sipariş → ~$30–60 (5 adet, ekonomik SMT).

## ⚠️ LCSC doğrulanacak (3 parça)
| Ref | Parça | Not |
|---|---|---|
| **U2** | 74AHCT1G125 (SOT-23-5) | 3.3→5V level shifter. JLCPCB'de yoksa eşdeğer (74LVC1G125 + dikkat) veya Extended. |
| **D1** | 10V zener (SOD-323) | BZT52C10 / MMSZ5240 — polariteyi önizlemede doğrula. |
| **F1** | PTC sigorta 1206 | Akıma göre seç (~3A hold). |

> Tüm LCSC kodları sipariş anında **stok/geçerlilik** açısından doğrulanmalı (kodlar değişir).

## Elle lehimlenecek (JLCPCB SMT'ye DAHİL DEĞİL)
Bunlar modül/soket/klemens — kart geldikten sonra elle takılır/lehimlenir:
- **U1L/U1R** — ESP32-DevKitC için 1×15 soketler (modül takılır)
- **A1/A2** — TMC2209 modülleri için 2×08 soketler
- **BK1** — buck modülü için 1×04 soket
- **J1–J5** — vidalı klemensler (12V, θ/ρ motor, LED, endstop)
- **C1 (1000µF), C6 (100µF)** — elektrolitik kondansatörler (THT)

## Üretim sonrası
Kart geldiğinde **bring-up testi** yap: `../../../docs/uretim/URETIM_DOSYASI.md` §5.1
(motor bağlamadan güç → 5V ölç → FluidNC flash → UART adres oku → LED test).

## Yeniden üretmek
```
kicad-cli pcb export pos --format csv --units mm --side both --use-drill-file-origin -o jlcpcb/pos_raw.csv controller.kicad_pcb
python3 make_jlcpcb.py
```
