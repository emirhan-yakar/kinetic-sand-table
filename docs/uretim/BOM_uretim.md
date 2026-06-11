# Üretim BOM'u — Kinetik Kum Masası (Ø600, ayaklı sehpa)

Gerçek malzemeler, Türkiye tedarik kaynakları ve **gerçekçi 2026 fiyatları** (₺, KDV dahil yaklaşık).
Tek-adet prototip içindir; seri için "Seri" sütunu (50+ adet, toplu alım + kendi PCB dizgi).
Geometri/açı/PCD değerleri için `montaj.md` ve `montaj_sheet.svg`.

> Kur notu: ₺ oynaktır; elektronik/mıknatıs kalemleri büyük ölçüde döviz endeksli.
> Fiyatlar Haziran 2026 perakende seviyesidir.

---

## 1) Gövde & ahşap (marangoz / CNC ahşap atölyesi)
| Parça | Gerçek malzeme / spec | Adet | Tedarik (TR) | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| Drum gövde silindir | **18 mm huş kontrplak (bükme) veya istif MDF halka**, dış Ø600 × H150, et 18 | 1 | yerel **CNC ahşap/mobilya atölyesi** (Siteler-Ankara, Modoko/Masko-İst.) | 1.600 | 1.600 | 900 |
| Ceviz kaplama + cila | **doğal ceviz kaplama (0.6mm)** + su bazlı mat lake | 1 set | marangoz / kaplama atölyesi | 700 | 700 | 350 |
| Üst çerçeve (rim) | ceviz masif/kaplama, Ø600/iç Ø520, cam rabbet + mıknatıs cebi | 1 | CNC atölye | 450 | 450 | 250 |
| Ayaklar (4) | **masif ceviz/gürgen konik ayak 320mm**, 8° eğimli plakalı — veya hazır mid-century ayak seti | 1 set | **mobilya ayağı satıcıları** / ahşap torna atölyesi | 900 | 900 | 500 |
| Kum yatağı tepsisi | 4mm MDF/alüminyum, Ø520 (mıknatıslı üst modül tabanı) | 1 | CNC / lazer | 250 | 250 | 150 |
| **Ara toplam ahşap** | | | | | **3.900** | 2.150 |

## 2) Cam (temperli cam imalatçısı)
| Parça | Spec | Adet | Tedarik | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| Üst cam | **temperli cam Ø552 × 6mm, kenar rodajlı** (ops. low-iron ekstra şeffaf) | 1 | yerel **temperli cam imalatçısı** (her ilde) | 850 | 850 | 600 |

## 3) Hareket mekaniği (elektronik + lazer kesim + rulmancı)
| Parça | Gerçek malzeme / spec | Adet | Tedarik (TR) | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| NEMA17 step motor | 42×42, 1.5–1.8 A, 1.8° | 2 | **Robotistan / Motorobit** | 420 | 840 | 320/ad |
| Lazy-susan / turntable rulman | Ø150 döner tabla rulmanı (θ ekseni) | 1 | rulmancı / Hepsiburada | 220 | 220 | 150 |
| MGN12H lineer ray + araba | 300 mm (ρ ekseni) | 1 | Robotistan / Aliexpress | 520 | 520 | 380 |
| GT2 kayış 5m + 20T pulley ×2 + F623 idler ×4 | 6mm kayış | 1 set | Robotistan | 320 | 320 | 220 |
| **Slip ring** (kapsül) | 6–12 kanal, 12V/2A — dönen ρ motoru kablosu | 1 | Robotistan / Aliexpress | 380 | 380 | 280 |
| Mekanizma şasi plakası | **alüminyum 6082 / 5754, 4mm lazer kesim**, Ø520 | 1 | **sac/alüminyum lazer kesim atölyesi** | 350 | 350 | 180 |
| Dönen kol (arm) | alüminyum 6082 5mm lazer kesim | 1 | lazer atölye | 180 | 180 | 90 |
| Taşıyıcı + mıknatıs yuvası | 3D baskı PETG veya alüminyum | 1 | kendi baskı / lazer | 120 | 120 | 60 |
| **Ara toplam mekanik** | | | | | **2.930** | 1.680 |

## 4) Mıknatıslar & bilye (neodyum mıknatıs satıcıları)
| Parça | Spec | Adet | Tedarik | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| Bilye sürücü mıknatıs | **N52 neodyum Ø20×10mm** (~9 kgf) | 1 | mıknatıs satıcıları | 140 | 140 | 90 |
| Üst modül tutucu mıknatıs | **N52 Ø20×3mm** (~2.7 kgf) | 8 | mıknatıs satıcıları | 35 | 280 | 22/ad |
| Karşı çelik plaka (mıknatıs için) | **DKP saç 1.5mm**, Ø22 disk | 8 | lazer kesim / sac | 12 | 96 | 6/ad |
| Çelik bilye | **AISI 420 / krom çelik Ø12mm** | 1 | rulmancı | 45 | 45 | 25 |
| **Ara toplam mıknatıs** | | | | | **561** | 360 |

## 5) Aydınlatma & güç
| Parça | Spec | Adet | Tedarik | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| WS2812B adreslenebilir LED şerit | 60 LED/m, ~2 m (kenar halka) | 1 | **Samm Teknoloji / Direnç.net / LED Pazarı** | 280 | 280 | 180 |
| 12V SMPS güç kaynağı | 12V 6A (72W) | 1 | elektronik tedarikçi | 360 | 360 | 250 |
| Buck konvertör 12→5V | 3–5A (LED + lojik) | 1 | Robotistan | 90 | 90 | 55 |
| **Ara toplam güç/LED** | | | | | **730** | 485 |

## 6) Kontrol kartı (bizim tasarım — `hardware/pcb/`)
| Parça | Spec | Adet | Tedarik | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| Kontrol PCB | ESP32 + 2× TMC2209 + WS2812 + güç (`controller.kicad_pcb`) | 1 | **JLCPCB/PCBWay** (Çin, 5 adet min) veya yurtiçi PCB | 450 | 450 | 90/ad |
| ESP32-DevKitC / TMC2209 (prototip modül) | hazır modül (PCB header'a) | 1 set | Robotistan | 720 | 720 | dizgi: 350 |
| **Ara toplam kart** | | | | | **1.170** | 440 |

## 7) Bağlantı elemanları & sarf
| Parça | Spec | Adet | Tedarik | Birim ₺ | Toplam ₺ | Seri ₺ |
|---|---|---|---|---|---|---|
| Gömme dişli (threaded insert) | M4 & M6 ahşap için (ısı/burgu) | ~20 | hırdavat | 6 | 120 | 70 |
| Paslanmaz vida/civata seti | M3×8, M4×16, M5×40, M6×30 + somun/pul | 1 set | hırdavat | 200 | 200 | 120 |
| Pirinç standoff (M4) | mekanizma plakası ayağı | 8 | Robotistan | 12 | 96 | 60 |
| İnce kuvars/silis kum | 0.1–0.3mm, ~1.5 kg | 1 | hobi / dökümhane | 90 | 90 | 50 |
| Kablo, klemens, kablo kanalı, ayak keçesi | — | 1 set | hırdavat | 180 | 180 | 110 |
| **Ara toplam sarf** | | | | | **686** | 410 |

---

## TOPLAM
| | Prototip (1 ad.) | Seri (≥50 ad., parça başı) |
|---|---|---|
| Ahşap | 3.900 | 2.150 |
| Cam | 850 | 600 |
| Mekanik | 2.930 | 1.680 |
| Mıknatıs/bilye | 561 | 360 |
| Güç/LED | 730 | 485 |
| Kontrol kartı | 1.170 | 440 |
| Sarf/bağlantı | 686 | 410 |
| **MALZEME TOPLAM** | **≈ 10.800 ₺** (~$320) | **≈ 6.100 ₺** (~$180) |
| İşçilik/montaj (tahmini) | +2.500–4.000 | +1.200 |
| **GERÇEKÇİ MALİYET** | **≈ 13.500–15.000 ₺** | **≈ 7.300 ₺** |

Yazılım: **0 ₺** (Dune Weaver firmware + Sandify/desen araçları açık kaynak, `firmware/`).

**Satış karşılaştırması:** Nikolatoy $699 (≈ 23.000+ ₺). Seri maliyet/satış oranı **~%32** → sağlıklı marj.

---

## Tedarik özeti — "nereden"
- **Elektronik/motor/ray/slip ring:** robotistan.com, motorobit.com, direnc.net
- **LED (WS2812B):** samm.com, direnc.net, ledpazari.com — toplu: LCSC/Aliexpress
- **Mıknatıs (N52):** yurtiçi neodyum mıknatıs satıcıları (online)
- **Ahşap gövde/CNC + ayak:** yerel CNC ahşap / mobilya atölyesi (Siteler-Ankara, Modoko/Masko-İstanbul, İzmir Karabağlar)
- **Temperli cam:** yerel temperli cam imalatçısı (rodajlı kesim)
- **Alüminyum lazer kesim (şasi/kol/karşı plaka):** sac-alüminyum lazer kesim atölyesi
- **PCB:** JLCPCB/PCBWay (ucuz, dizgi dahil) veya yurtiçi PCB firmaları (Bursa/İstanbul)
- **Hırdavat/bağlantı/insert:** yerel cıvata-hırdavat
