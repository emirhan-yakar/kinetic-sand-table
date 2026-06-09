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

## Üretim
- Gerber + BOM + CPL üret → JLCPCB "Assembly" servisi (SMT) en ucuz.
- 2 katman, 1.6mm, HASL yeterli. Motor/güç hatlarında bakır genişliğini artır.

> İstersen bu spesifikasyondan **gerçek KiCad şema + PCB dosyalarını** (.kicad_sch /
> .kicad_pcb) ve Gerber'ı üretebilirim — söyle, oluşturayım.
