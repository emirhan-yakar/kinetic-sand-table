# QA / Bring-up & Fonksiyonel Test Fişi (FCT)

**Ünite seri no:** ____________  **Tarih:** __________  **Operatör:** ____________
**Rev:** PCB Rev-B · FluidNC ____  **Sonuç:** ☐ GEÇTİ  ☐ KALDI  **İmza:** __________

> Sırayı atlamayın. Her adımda **ölç → yaz → işaretle**. Bir KALDI varsa durun, kök neden bulun.

---

## 1) Gelen muayene + emniyet (güç YOK)
| # | Kontrol | Beklenen | Ölçüm | ✓/✗ |
|---|---|---|---|---|
|1.1| Görsel: lehim/komponent/yön (U2,Q1,D1 polarite) | kusursuz | — | ☐ |
|1.2| 12V–GND kısa devre (ohm) | yüksek (>1kΩ) | _____ Ω | ☐ |
|1.3| 5V–GND kısa devre | yüksek | _____ Ω | ☐ |
|1.4| 3V3–GND kısa devre | yüksek | _____ Ω | ☐ |
|1.5| PE topraklama sürekliliği (gövde) | <0.1 Ω | _____ Ω | ☐ |

## 2) Güç verme (motor BAĞLI DEĞİL)
| # | Test noktası | Beklenen | Ölçüm | ✓/✗ |
|---|---|---|---|---|
|2.1| J1 giriş | 11.4–12.6 V | _____ V | ☐ |
|2.2| 5V rayı (buck çıkışı) | 4.90–5.10 V | _____ V | ☐ |
|2.3| 3V3 rayı (ESP32) | 3.25–3.35 V | _____ V | ☐ |
|2.4| Boşta akım (12V) | < 0.30 A | _____ A | ☐ |
|2.5| ESP32/sürücü ısınma (1 dk) | el ile ılık-altı | — | ☐ |
|2.6| Ters polarite testi (kısa, bilerek ters) | hasar yok (Q1 keser) | — | ☐ |

## 3) Haberleşme / firmware
| # | Kontrol | Beklenen | ✓/✗ |
|---|---|---|---|
|3.1| FluidNC açılıyor (seri/WebUI) | versiyon banner | ☐ |
|3.2| `$Stepper` / config okunuyor | hata yok | ☐ |
|3.3| (UART modu) iki sürücü ayrı adres yanıtı | addr 0 ve 1 | ☐ |

## 4) Hareket (motorlar bağlı, mekanizma serbest)
| # | Test | Beklenen | Ölçüm | ✓/✗ |
|---|---|---|---|---|
|4.1| TMC akım ayarı | 0.6–0.9 A/faz | _____ A | ☐ |
|4.2| θ tam tur (A 360°) | kayma/atlama yok | — | ☐ |
|4.3| ρ ileri/geri (X 0→250→0) | düzgün, ses az | — | ☐ |
|4.4| ρ homing (endstop) | tetikler, durur | — | ☐ |
|4.5| θ yön / ρ yön doğru | desenle uyumlu | — | ☐ |

## 5) LED
| # | Test | Beklenen | ✓/✗ |
|---|---|---|---|
|5.1| Tüm LED yanıyor (test deseni) | eksik/yanlış renk yok | ☐ |
|5.2| Level-shifter (DIN 5V) kararlı | titreme yok | ☐ |

## 6) Fonksiyonel (sistem, kum+bilye)
| # | Test | Beklenen | ✓/✗ |
|---|---|---|---|
|6.1| Mıknatıs bilyeyi sürüklüyor | kaçırma yok (orta hız) | ☐ |
|6.2| Tam desen (Atatürk imza / spiral) | temiz oluk, merkezde | ☐ |
|6.3| Kuplaj max hız (kalibrasyon) | _____ mm/s’de stabil | ☐ |

## 7) Dayanıklılık
| # | Test | Beklenen | ✓/✗ |
|---|---|---|---|
|7.1| 24h burn-in (sürekli desen) | hata/ısınma/atlama yok | ☐ |
|7.2| Gürültü seviyesi | kabul (≤ ____ dBA) | ☐ |

## 8) Final QA
| # | Kontrol | ✓/✗ |
|---|---|---|
|8.1| Cam/üst modül mıknatıs oturuyor, boşluk yok | ☐ |
|8.2| Ayak stabilite (sallanma yok) | ☐ |
|8.3| Etiket / seri no / kullanım kılavuzu | ☐ |
|8.4| Ambalaj uygun | ☐ |

**Notlar:** ____________________________________________________________________

> Test noktaları: 12V=J1, 5V=C1/BK1 çıkışı, 3V3=ESP32 3V3 pini, akım=seri ampermetre.
> Akış: `elektrik_montaj.md` → bu fiş → `URETIM_DOSYASI.md §5`.
