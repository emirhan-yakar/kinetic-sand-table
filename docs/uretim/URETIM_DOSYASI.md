# Üretim Gerçekleme Dosyası — Kinetik Kum Masası
### (Manufacturing Readiness / Product Realization Dossier)

Bu belge ürünü **gerçek, satılabilir bir ürüne** dönüştürmek için yol haritasıdır.
Bir deneme değil; profesyonel donanım ürün geliştirme (NPI) disiplinine göre yazılmıştır.
**Dürüstlük ilkesi:** her alt sistemin gerçek olgunluk durumu açıkça belirtilir — "tasarlandı"
ile "doğrulandı" ve "fiziksel test edildi" karıştırılmaz.

---

## 0) DÜRÜST DURUM ÖZETİ (en kritik kısım)

| Alt sistem | Durum | Açıklama |
|---|---|---|
| Mekanik tasarım (Ø600 polar, ayak, mıknatıslı modül) | 🟡 **Tasarlandı** | Parametrik geometri + ölçülü montaj sheet + patlatma çizimi. **Fiziksel prototip yapılmadı.** |
| Kontrol kartı (PCB) | 🟠 **Tasarlandı, DRC temiz — FİZİKSEL ÜRETİLMEDİ/TEST EDİLMEDİ** | KiCad + Freerouting; auto-route. Elektriksel inceleme **düzeltilmesi gereken bulgular** ortaya çıkardı (bkz. `PCB_inceleme.md`). **Hiç lehimlenmedi, ölçülmedi.** |
| Firmware | 🟠 **Yazılmadı — mimari + config taslağı var** | Hazır açık kaynak **FluidNC** (hareket) + **Dune Weaver** (desen/web) kullanılacak. Örnek `firmware/fluidnc_config.yaml` hazırlandı ama **cihaza yüklenip doğrulanmadı.** |
| Görseller/render/video | 🟢 **Hazır** | Reklam kalitesinde (ön-görselleştirme; satış için fiziksel ürün fotosu gerekir). |
| BOM / maliyet / tedarik | 🟢 **Hazır** | Gerçek malzeme + TR tedarik + fiyat. |

> **Net cevap (PCB test edildi mi?):** **Hayır.** Kart yazılımda tasarlandı ve tasarım kuralı
> kontrolünü (DRC) geçti, ancak **fiziksel olarak üretilmedi ve test edilmedi.** Gerçek ürün için
> önce tasarım inceleme bulguları düzeltilmeli, prototip bastırılmalı ve **bring-up testi** yapılmalı.
> Bu dosya tam olarak bu yolu tanımlar.

---

## 1) Sistem mimarisi (gerçek ürün)

```
 [Patternler .thr]  → (Sandify/Dune Weaver: .thr→G-code) →  ┌────────────────────┐
                                                            │ ESP32 + FluidNC    │→ TMC2209 ×2 → NEMA17 θ, ρ
 Web/uygulama (opsiyonel Raspberry Pi Zero 2 W,             │ (hareket, WebUI,   │→ WS2812B LED (WLED/DW)
 Dune Weaver app: desen kütüphanesi, LED senk, zamanlama)   │  SD'den G-code)    │→ endstop (θ home)
                                                            └────────────────────┘
                                                                 12V güç + buck 5V
```

**Mimari kararlar (2 seçenek):**
- **A — Sade (önerilen başlangıç):** ESP32 + **FluidNC** tek başına. Desenler offline `.thr→G-code`
  çevrilir, **SD karta** konur veya WebUI'dan gönderilir. Pi yok → daha ucuz, daha az parça.
- **B — Tam deneyim:** A + **Raspberry Pi Zero 2 W** üzerinde **Dune Weaver** uygulaması
  (.thr kütüphanesi, canlı önizleme, LED modları, zamanlama). +~500 ₺, daha iyi kullanıcı deneyimi.

> Önerimiz: **EVT/DVT'de A** (riski azalt), satışa hazır üründe **B** (UX için).

---

## 2) Entegrasyon haritası — ne nereye, nasıl bağlanır

| Kart konnektörü | Bağlanır | Kablo / not |
|---|---|---|
| **J1 (12V giriş)** | 12V SMPS | Sigorta + ters polarite koruması (bkz. PCB inceleme) |
| **J2 (θ motor, 4p)** | NEMA17 θ (dönen kol tahriki) | gövde içi sabit |
| **J3 (ρ motor, 4p)** | NEMA17 ρ → **slip ring** → dönen koldaki motor | 4 bobin kablosu kapsül slip ring'den |
| **J4 (LED, 3p: 5V/DIN/GND)** | WS2812B halka | DIN'e **level shifter** (3.3→5V) gerekir (inceleme) |
| **J5 (endstop, 3p)** | θ home opto/mikro switch | dönen tablada referans |
| BK1 buck | 12V→5V | ESP32 + LED + sürücü VIO |
| θ motor şasiye, ρ motor kol ucuna | mekanizma (`montaj.md` §4) | M3, slip ring kablolama |

Fiziksel yerleşim: kontrol kartı **drum içi alüminyum şasiye** (4× M3 standoff), 12V SMPS şasi altına,
slip ring şasi merkezine, LED halka rim iç kenarına. (Detay: `montaj.md`, `montaj_patlatma.png`.)

---

## 3) Üretim akışı — kim, neyi, nasıl üretir

| # | Parça | Proses | Üretici (TR) | DFM notu |
|---|---|---|---|---|
| 1 | Drum gövde + rim | CNC kesim + ceviz kaplama + lake | yerel CNC ahşap/mobilya atölyesi | bükme kontrplak veya istif halka; toleranslar montaj sheet'te |
| 2 | Ayaklar (4) | torna + 8° eğimli plaka | ahşap torna / hazır mobilya ayağı | açı plakadan gelir, elde verilmez |
| 3 | Temperli cam Ø552×6 | kesim + temper + rodaj | yerel temperli cam imalatçısı | low-iron opsiyon |
| 4 | Alüminyum şasi + kol | lazer kesim 6082 | sac/alüminyum lazer atölyesi | DXF kesim dosyaları hazırlanmalı (yapılacak) |
| 5 | **Kontrol kartı (PCB)** | PCB üretim + **SMT dizgi** | **JLCPCB/PCBWay** (dizgi dahil) veya yurtiçi | Gerber+BOM+CPL hazır; **önce inceleme düzeltmeleri** |
| 6 | Final montaj + kablolama + kalibrasyon + QA | manuel | kendi montaj hattın | test planı §6 |

---

## 4) NPI aşamaları — ilk satılabilir üniteye yol

| Aşama | Amaç | Çıktı | Süre (tahmini) | Maliyet |
|---|---|---|---|---|
| **0 · Tasarım dondurma** | İnceleme bulgularını düzelt (PCB, mekanik) | Rev-B Gerber, DXF, BOM | 1–2 hafta | düşük (mühendislik) |
| **1 · EVT** (Engineering) | İlk fonksiyon: 1 PCB bastır+dizgi, bread-board mekanizma, FluidNC bring-up | Çalışan 1 ünite (estetik değil) | 3–4 hafta | ~PCB 5'li + parçalar ~15k ₺ |
| **2 · DVT** (Design Verif.) | Estetik gövde + kalibrasyon + 24h burn-in + desen testi | Sunulabilir prototip | 3–4 hafta | ~1 ünite tam BOM |
| **3 · PVT** (Production) | Küçük seri (10–20), montaj talimatı, QA prosedürü | Satılabilir ürün + süreç | 4–6 hafta | seri BOM × adet |
| **4 · Üretim** | Sürekli üretim | — | — | — |

---

## 5) Test ve doğrulama planı

**5.1 PCB bring-up (kart geldiğinde, motor BAĞLAMADAN):**
1. Görsel + kısa devre kontrolü (multimetre: 12V–GND, 5V–GND direnç).
2. Güç ver, **5V rayını ölç** (4.9–5.1V), ESP32 ısınma yok.
3. ESP32 flash (FluidNC), seri konsol açılıyor mu.
4. TMC2209 UART **adres okuma** (FluidNC `$Stepper/...` — her iki sürücü ayrı adres yanıt vermeli).
5. WS2812: tek LED test (level shifter doğrulaması).

**5.2 Hareket:**
6. Motorları bağla, akım ayarı (TMC2209 ~0.6–0.9A), θ tam tur (kayma yok), ρ menzil/endstop.
7. Bilye sürükleme: mıknatıs gücü vs hız (kostik/kayıp testi).

**5.3 Sistem:**
8. Tam desen çiz (Atatürk imza + spiral), 24h **burn-in** (ısınma, gürültü, kaçırma).
9. **Güvenlik:** 12V SMPS CE'li, sigorta, topraklama, sıcaklık < sınır; cam kenar emniyeti.

---

## 6) Maliyet (COGS) ve hedef satış fiyatı

| | Prototip (1 ad) | Seri (50+, parça başı) |
|---|---|---|
| Malzeme (BOM) | ~10.800 ₺ | ~6.100 ₺ |
| İşçilik/montaj | +2.500–4.000 | +1.200 |
| (Tam deneyim) + Raspberry Pi Zero 2 W | — | +500 |
| **COGS** | **~13.500–15.000 ₺** | **~7.800 ₺ (~$230)** |

**Fiyatlandırma (profesyonel marj analizi):**
- Sağlıklı donanım perakende marjı: satış ≈ **2.5–3× COGS** (garanti, iade, pazarlama, kanal payı dahil).
- Seri COGS ~7.800 ₺ → **hedef MSRP ≈ 19.900–23.900 ₺ ($590–700)**.
- **Önerilen liste fiyatı: 21.900 ₺ (~$650)** — benzer ürün ($699) ile rekabetçi, ~%64 brüt marj.
- Lansman/erken kuş: 17.900 ₺; bayi/kanal: liste − %30.

> Not: işçilik + overhead + garanti rezervi (ünite başı ~%8) + iade (~%3) fiyata içkindir.
> Marj, montaj kalitesi/marka/hazır desen kütüphanesinde korunur (donanım kolay kopyalanır).

---

## 7) Risk kaydı (öne çıkanlar)

| Risk | Etki | Önlem |
|---|---|---|
| **PCB ilk dönüşte çalışmaz** | yüksek | inceleme düzeltmeleri + 5'li bastır (yedek), bring-up planı |
| WS2812 3.3V data güvenilmez | orta | level shifter (74AHCT125) — Rev-B |
| TMC2209 UART adres çakışması | orta | MS1/MS2 ayrı adres — Rev-B |
| Slip ring kontak/gürültü | orta | kaliteli kapsül slip ring, ρ akımı düşük tut |
| Mıknatıs bilyeyi kaçırır (hız) | orta | hız limiti + mıknatıs/hava aralığı testi |
| Cam ağırlığı/emniyet | orta | temperli + rodaj + mıknatıslı modül SF 5.2× |
| Tedarik/kur dalgalanması | orta | döviz endeksli kalemler için stok/sözleşme |

---

## 8) İlgili dosyalar
- `PCB_inceleme.md` — dürüst elektriksel inceleme + üretim öncesi düzeltmeler
- `../../firmware/fluidnc_config.yaml` + `../../firmware/README.md` — firmware mimarisi/config
- `BOM_uretim.md` · `montaj.md` · `montaj_sheet.svg` · `montaj_patlatma.png`
- `../../hardware/pcb/` — KiCad tasarımı, Gerber, STEP
