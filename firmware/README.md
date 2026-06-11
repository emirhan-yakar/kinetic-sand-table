# Firmware & Yazılım — gerçek mimari

> **Durum:** Mimari + config **hazır**; cihaza yüklenip **doğrulanmadı** (PCB henüz üretilmedi).
> Hazır açık kaynak yazılım kullanılır — sıfırdan firmware yazmaya gerek yok.

## Mimari
Kinetik kum masaları iki katmanlı çalışır:

1. **Hareket: ESP32 + FluidNC** — G-code yorumlar, TMC2209 sürücülerle θ/ρ motorlarını sürer.
   - Pinler kontrol kartıyla eşleşir: **`fluidnc_config.yaml`** (bu klasörde).
   - FluidNC'nin kendi **WebUI**'si var; SD karttan G-code oynatabilir.
2. **Desen/UX: Dune Weaver (opsiyonel, Raspberry Pi)** — `.thr` desen kütüphanesi, canlı
   önizleme, **LED senkron (WLED)**, zamanlama. `.thr`'yi G-code'a çevirip FluidNC'ye gönderir.

```
.thr (Sandify/Dune Weaver) --(theta-rho -> G-code)--> FluidNC (ESP32) --> TMC2209 --> motorlar
                                                          └ WebUI / SD
LED: WS2812B  <-- WLED veya Dune Weaver LED modulu (idle/playing/scheduled)
```

**İki seçenek:**
- **A (sade, EVT):** Sadece FluidNC. Desenler offline `.thr→G-code` çevrilip SD'ye/WebUI'a.
- **B (tam UX, ürün):** A + Raspberry Pi Zero 2 W'de Dune Weaver app (+~500 ₺).

## Kurulum
1. **FluidNC yükle** (ESP32): https://github.com/bdring/FluidNC — web installer (`http://install.fluidnc.com`) veya esptool.
2. `fluidnc_config.yaml`'i karta yükle (FluidNC WebUI → Files veya SD). Pinler PCB ile eşleşir.
3. **Kalibrasyon (donanımda, ZORUNLU):**
   - `steps_per_mm` (X=ρ ve A=θ) gerçek dişli/mikroadıma göre ayarla (config'deki değerler tahmini).
   - ρ home (endstop) yönü/menzili; θ tam tur = doğru derece.
   - TMC2209 akımı ~0.6–0.9A (standalone'da pot/UART'da config).
4. **Desen akışı:** `firmware/patterns/*.thr` (Atatürk imza, spiral, klasik) → Sandify/Dune Weaver
   ile G-code'a çevir → oynat. (Üretici: `firmware/patterns/*.py`.)
5. **Dune Weaver (opsiyonel):** Raspberry Pi'ye kur (https://github.com/tuanchris/dune-weaver),
   FluidNC'yi seri/USB ile bağla, `.thr` kütüphanesi + LED + zamanlama.

## LED (WS2812B)
- **WLED** (ESP ayrı veya aynı) ya da Dune Weaver LED modülü ile sürülür — idle/playing/scheduled modları.
- Donanım notu: 3.3V→5V **level shifter** gerekir (bkz. `docs/uretim/PCB_inceleme.md` #2).

## Önemli — dürüst notlar
- Bu config **donanımda doğrulanmadı**; ilk bring-up'ta pin/yön/akım testleri gerekir
  (`docs/uretim/URETIM_DOSYASI.md` §5).
- İlk prototipte **standalone TMC** (UART yok) önerilir — daha az risk; UART'ı DVT'de ekle.
- Polar kinematik: θ = sürekli dönme (A ekseni), ρ = lineer (X ekseni). `.thr` (theta rad, rho 0..1)
  → G-code (A derece, X = rho×max_yarıçap). Çevrim Sandify/Dune Weaver tarafında.

## Dosyalar
- `fluidnc_config.yaml` — FluidNC pin/eksen config (PCB ile eşleşir)
- `patterns/` — `.thr` desenleri + üreteçler (imza izi, spiral, görüntü→theta-rho)
