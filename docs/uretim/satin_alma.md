# Prototip Satın-Alma & Tedarikçi Listesi

**Bir adet çalışan prototip** için somut alışveriş listesi. Para harcama anına en yakın doküman.

- 💰 **Malzeme toplamı ≈ 11.400 TL** (+ kargo + ~%10 yedek pay → bütçe **~13–14k TL**)
- 📋 Sipariş/takip için tablo: [`satin_alma.csv`](satin_alma.csv) (üreteç: `satin_alma.py`)
- ⚠️ Fiyat/stok **2026 TR tahmini** — sipariş anında doğrula. Tedarikçi adları + arama terimi verildi
  (canlı link/fiyat değişir).

## Sipariş stratejisi (önce uzun-terminliler!)
| Öncelik | Kalem | Termin | Neden |
|---|---|---|---|
| 1 | **PCB+SMT (JLCPCB)** · **slip ring** · **CNC ahşap gövde** | 1–2 hafta+ | en uzun termin → ilk sipariş et |
| 2 | MGN12 ray · lazy-susan · GT2 set · cam · Al lazer | 3–7 gün | orta termin |
| 3 | ESP32/TMC2209/buck/motor/LED/mıknatıs/sarf | 2–5 gün | hızlı, son sipariş |

> PCB: hazır [JLCPCB paketi](../../hardware/pcb/jlcpcb/) (Gerber+BOM+CPL) yükle.
> Alüminyum/ayak plakaları: [DXF + STEP](dxf/) atölyeye gönder. Cam: [montaj_sheet](montaj_sheet.svg) ölçüsü.

## 1) Elektronik / kontrol — ~2.270 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| Kontrol kartı PCB+SMT | Rev-B, 5 adet | 1 | JLCPCB/PCBWay | 1.600 | 1.600 |
| ESP32-DevKitC | WROOM-32 (ön-sertifikalı) | 1 | Robotistan/Motorobit | 170 | 170 |
| TMC2209 sürücü | StepStick, UART | 2 | Robotistan/Motorobit | 125 | 250 |
| Buck 12→5V | ≥5A | 1 | Robotistan | 90 | 90 |
| Klemens/header/sarf | 2.54mm + 5mm | 1 | Direnç.net | 160 | 160 |

## 2) Motor & hareket — ~1.805 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| NEMA17 step motor | 1.8°, ~0.4 N·m | 2 | Robotistan | 260 | 520 |
| MGN12 ray + araba | ~300mm + MGN12H | 1 | lineer hareket satıcı | 470 | 470 |
| Lazy-susan rulman | Ø100–150 | 1 | yatak/robotik | 160 | 160 |
| GT2 kayış+kasnak seti | 6mm 2m + 20T×2 + 60T + idler | 1 | Robotistan | 260 | 260 |
| **Kapsül slip ring** | Ø12.5 · 8–12 yol · ≥2A | 1 | otomasyon/Aliexpress | 360 | 360 |
| Endstop | mekanik/opto | 1 | Robotistan | 35 | 35 |

## 3) Mıknatıs & bilye — ~403 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| N52 taşıyıcı mıknatıs | Ø20×10 | 3 | yurtiçi neodyum | 45 | 135 |
| N52 üst modül mıknatıs | Ø20×3 | 8 | yurtiçi neodyum | 26 | 208 |
| Krom çelik bilye | Ø12 | 5 | rulman/bilye satıcı | 12 | 60 |

## 4) Güç + LED — ~590 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| 12V SMPS (CE'li) | ≥6A kapalı kasa | 1 | Samm/Robotistan | 320 | 320 |
| Güç kablosu + fiş | topraklı IEC | 1 | elektrik malz. | 60 | 60 |
| WS2812B LED | 60 LED halka/şerit | 1 | Samm/LED Pazarı | 210 | 210 |

## 5) Gövde & yapı — ~5.850 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| Ceviz kaplama gövde (CNC) | drum Ø600 (prototip tek) | 1 | yerel CNC ahşap atölyesi | 3.200 | 3.200 |
| Masif ceviz ayak (torna) | 8°, L320 | 4 | ahşap torna/mobilya | 200 | 800 |
| Lake/finiş | mat koruyucu | 1 | boya malz. | 300 | 300 |
| Temperli cam Ø552×6 | low-iron, rodajlı | 1 | yerel temperli cam | 800 | 800 |
| Al lazer kesim (DXF) | şasi + kol + 4 ayak plakası | 1 | sac/Al lazer atölyesi | 750 | 750 |

## 6) Bağlantı / sarf — ~640 TL
| Parça | Spec | Ad | Tedarikçi | Birim | Toplam |
|---|---|--:|---|--:|--:|
| Vida/somun/standoff/insert | M3/M4/M5/M6 + gömme dişli | 1 | hırdavat/Robotistan | 260 | 260 |
| Kablo yönetimi | kanal/spiral/ferrül/etiket | 1 | elektrik malz. | 150 | 150 |
| İnce kuvars kum | ~1.5 kg | 1 | hobi/akvaryum | 80 | 80 |

## Tedarikçi rehberi (TR)
- **Elektronik/motor/ray/GT2/endstop:** Robotistan, Motorobit, Direnç.net
- **LED / güç:** Samm Teknoloji, LED Pazarı · toplu: LCSC / AliExpress
- **N52 mıknatıs:** yurtiçi neodyum satıcıları (arama: "N52 Ø20")
- **Slip ring:** otomasyon/robotik (arama: "kapsül slip ring 12mm 12 yol")
- **Ahşap gövde/ayak:** yerel CNC ahşap / mobilya atölyesi (DXF + ölçü ver)
- **Temperli cam:** yerel temperli cam imalatçısı (Ø552×6, rodaj iste)
- **Alüminyum lazer:** sac/Al lazer atölyesi ([DXF](dxf/) gönder)
- **PCB:** JLCPCB / PCBWay ([paket](../../hardware/pcb/jlcpcb/)) veya yurtiçi PCB

## Sonraki adım
Sipariş → gelince [bring-up testi](QA_kontrol_listesi.md) (önce motorsuz güç) → [montaj](montaj.md) →
[FluidNC kalibrasyon](../../firmware/README.md). Risk kontrolü: [FMEA](fmea.md).
