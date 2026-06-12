# FMEA + Gereksinim & Test İzlenebilirliği

Hata Modu ve Etkileri Analizi (FMEA) + ürün gereksinim spesifikasyonu (PRD) ve
gereksinim→test izleme matrisi. Global donanım geliştirmede standart mühendislik rigoru.

---

## 1) Ürün gereksinimleri (PRD — özet)
| ID | Gereksinim | Doğrulama (test) |
|---|---|---|
| **R1** | Desen çözünürlüğü ≥ sub-mm (kenar) | T-MECH-1 |
| **R2** | θ sürekli dönme, ρ 0–250 mm, homing | T-MOT-2/3 |
| **R3** | Bilye kaçırmadan sürüklenir (≤ hedef hız) | T-FUNC-1 |
| **R4** | Gürültü ≤ ~35 dBA (oturma odası) | T-NOISE |
| **R5** | 5V/12V raylar tolerans içinde, LED kararlı | T-PWR-1/2, T-LED |
| **R6** | 7/24 çalışmada atlama/ısınma yok (ömür) | T-BURN (≥24h, hedef ≥1000h) |
| **R7** | Üst modül emniyetli tutma (SF ≥ 3) | hesap: SF 5.2× ✓ |
| **R8** | Ağ güvenliği: yetkisiz erişim yok | T-SEC |
| **R9** | Devrilme stabilitesi (mobilya std) | T-STAB |
| **R10** | EMC/emniyet uyumlu | [sertifikasyon](sertifikasyon.md) |

## 2) FMEA (S=şiddet, O=olasılık, D=tespit; RPN=S×O×D, 1–10)
| # | Öğe / fonksiyon | Hata modu | Etki | S | O | D | RPN | Önlem |
|---|---|---|---|--:|--:|--:|--:|---|
|F1| 12V giriş | ters polarite | kart hasarı | 7 | 3 | 2 | 42 | P-FET + sigorta (Rev-B) ✓ |
|F2| WS2812 data | 3.3V seviye yetersiz | LED titrer/yanmaz | 4 | 6 | 3 | 72 | level-shifter (Rev-B) ✓ |
|F3| TMC2209 UART | adres çakışması | sürücü ayarlanamaz | 6 | 5 | 3 | 90 | ayrı MS adres (Rev-B) ✓ |
|F4| Slip ring | kontak gürültü/aşınma | ρ motor kesilir | 7 | 4 | 4 | 112 | ≥2A kaliteli kapsül, akım düşük; periyodik bakım |
|F5| Manyetik kuplaj | hızda bilye kaçar | desen bozulur | 5 | 5 | 2 | 50 | hız limiti + aralık ≤10mm + mıknatıs büyüt |
|F6| θ yatak | boşluk/salınım | desen kayması | 6 | 4 | 5 | 120 | kaliteli ince-kesit rulman + kayış gerginliği |
|F7| ρ kayış | atlama (skip) | konum kayması | 6 | 4 | 5 | 120 | doğru gerginlik + akım; homing referansı |
|F8| Motor/sürücü | aşırı ısınma | kapanma/ömür | 6 | 3 | 4 | 72 | akım 0.6–0.9A, havalandırma, burn-in |
|F9| Temperli cam | kırılma | yaralanma | 9 | 2 | 2 | 36 | temperli + rodaj + yük testi |
|F10| Üst mıknatıs modül | parmak sıkışması | yaralanma | 7 | 3 | 3 | 63 | ikaz + kaldırma tasarımı |
|F11| Firmware | güç kesintisi sonrası kayıp | yeniden home gerek | 4 | 5 | 3 | 60 | açılışta auto-home + durum kaydı |
|F12| Ağ | yetkisiz erişim | kontrol ele geçer | 7 | 3 | 5 | 105 | AP şifre, yerel ağ, OTA imzalama, port kısıtla |
|F13| Wi-Fi/EMC | parazit/uyumsuzluk | sertifika kalır | 6 | 4 | 4 | 96 | ön-sertifikalı modül + EMC pre-scan |

**En yüksek RPN'ler (öncelik):** F6/F7 (mekanik boşluk/atlama, 120), F4 (slip ring, 112), F12 (güvenlik, 105),
F13 (EMC, 96), F3 (90). Bunlar **prototip/bring-up testinde** özellikle doğrulanmalı.

## 3) Gereksinim → Test izleme matrisi
| Gereksinim | Test (QA fişi / plan) | Durum |
|---|---|---|
| R1 | T-MECH-1 (çözünürlük) | hesap ✓ · donanım ⏳ |
| R2 | [QA](QA_kontrol_listesi.md) §4.2–4.4 | ⏳ prototip |
| R3 | QA §6.1 | ⏳ |
| R4 | T-NOISE (dBA ölçüm) | ⏳ |
| R5 | QA §2.1–2.3, §5 | ⏳ |
| R6 | QA §7.1 burn-in | ⏳ |
| R7 | mıknatıs hesabı (SF 5.2×) | ✓ |
| R8 | T-SEC (penetrasyon) | ⏳ |
| R9 | T-STAB (devrilme) | ⏳ |
| R10 | [sertifikasyon](sertifikasyon.md) | ⏳ |

> "⏳" kalemler **fiziksel prototip** gerektirir — yazılımda kapatılamaz. FMEA, bring-up ve
> DVT test planının girdisidir ([üretim dosyası §5](URETIM_DOSYASI.md)).

## 4) Süreç (global pro)
Tasarım → **FMEA** (bu) → risk azaltma → prototip → **bring-up + DVT testleri** (gereksinime bağlı) →
ECO ile düzeltme → PVT → üretim. Her revizyonda FMEA güncellenir ([CHANGELOG](../../CHANGELOG.md)).
