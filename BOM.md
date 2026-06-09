# Malzeme Listesi (BOM) — Polar Kum Masası Ø60 cm

Fiyatlar Haziran 2026 yaklaşık yurt içi perakende; ₺ kuru oynaktır, USD karşılığı
yön vermek içindir. Linkler kategori/tedarikçi düzeyindedir (model seçimini
ölçüye göre yaparsın).

## 1) Hareket / mekanik
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| NEMA 17 step motor (1.5–1.8A, 42mm) | 2 | θ ve ρ eksenleri | [Robotistan](https://www.robotistan.com), [Motorobit](https://www.motorobit.com) | 500–700 |
| Lazy-susan / turntable rulman (Ø100–150mm) | 1 | dönen kol tablası | rulmancı / Hepsiburada | 150–300 |
| GT2 6mm kayış (5m) + 20T pulley (2) + F623 idler (4) | 1 set | θ büyük pulley + ρ kayış | [Robotistan](https://www.robotistan.com) | 250–400 |
| MGN12 lineer ray + araba (250–300mm) | 1 | ρ ekseni (kol içi) | Robotistan / Aliexpress | 350–600 |
| **6+ kanallı slip ring (kapsül, 12V)** | 1 | dönen kola ρ motor kablosu | [Robotistan](https://www.robotistan.com)/Aliexpress | 250–450 |
| 3D baskı parçalar (PETG): kol, motor yatakları, mıknatıs taşıyıcı | — | `sand_table.scad`'den STL | kendi yazıcın / baskı servisi | 200–400 |

## 2) Mıknatıs & bilye
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| N52 neodyum mıknatıs (Ø15–20mm) | 1–3 | taşıyıcıda | mıknatıs satıcıları | 100–250 |
| Çelik bilye (krom çelik, Ø10–15mm) | 1 | kum üstünde | rulmancı | 30–80 |
| İnce dekoratif/kuvars kum | 1–2 kg | yüzey | hobi/akvaryum | 50–150 |

## 3) Elektronik / beyin
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| ESP32 DevKit (WROOM-32) | 1 | Dune Weaver firmware | [Robotistan](https://www.robotistan.com), [Direnç.net](https://www.direnc.net) | 150–250 |
| TMC2209 step sürücü | 2 | sessiz çalışma için ideal | Robotistan | 300–400 |
| **PROTOTİP alternatifi:** MKS DLC32 / BTT kontrol kartı (ESP32 dahili) | 1 | sürücü yuvalı, kablolama kolay | Robotistan | 700–1200 |

## 4) LED aydınlatma
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| WS2812B / SK6812 adreslenebilir şerit (60 LED/m, ~2m) | 1 | kenar halka | **[Samm Teknoloji](https://www.samm.com)**, **[Direnç.net](https://www.direnc.net)**, **[LED Pazarı](https://www.ledpazari.com)**, Robotistan | 150–350 |
| 1000µF kondansatör + 330Ω direnç (LED hat koruması) | — | std. WS2812 önerisi | Direnç.net | 20 |

> Toptan/seri için: **LCSC** veya **Aliexpress** (WS2812B 5m makara çok daha ucuz).

## 5) Güç
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| 12V 5–10A SMPS / masaüstü adaptör | 1 | motorlar + LED | elektronik tedarikçi | 250–450 |
| Buck konvertör 12V→5V (LED + ESP32) | 1 | 3–5A | Robotistan | 60–120 |

## 6) Gövde / kabin
| Parça | Adet | Not | Tedarik | ~₺ |
|---|---|---|---|---|
| Temperli cam üst (Ø60cm, 5–6mm, kenar rodajlı) | 1 | yüzey | yerel camcı | 600–1200 |
| MDF/kontrplak gövde + alt taban (CNC/lazer kesim) | 1 | kabin | marangoz / lazer atölye | 800–1800 |
| Ahşap kaplama / boya / ayaklar / vida-somun seti | — | bitirme | — | 400–800 |

## Toplam maliyet
| Senaryo | Yaklaşık |
|---|---|
| **Tek-adet prototip** (V-slot yerine MGN12, hazır kart) | **~6.000–10.000 ₺ (≈ $180–300)** |
| **Seri (50+ adet, özel PCB + toplu alım)** | parça başı **~3.500–5.500 ₺** |
| Karşılaştırma: Nikolatoy satış fiyatı | $699 (≈ 22.000+ ₺) |

**Yazılım maliyeti: 0 ₺** — Dune Weaver firmware + Sandify desen üreteci açık kaynak.

> Not: Ø60 yuvarlak + slip ring versiyonu kareye göre biraz daha pahalı ama premium
> segment satış fiyatını fazlasıyla karşılar. Marj asıl olarak montaj kalitesi,
> sessizlik, marka ve hazır desen kütüphanesinde.
