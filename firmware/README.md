# Firmware & Desen Yazılımı

Yuvarlak (polar) kum masası için iki olgun yol var. **Dune Weaver** yeni başlayan
için en pratiği — ESP32 üzerinde çalışır, dahili Wi-Fi web arayüzü, `.thr`
oynatma kuyruğu ve LED kontrolü hazır gelir.

## Seçenek A — Dune Weaver (ÖNERİLEN)
Açık kaynak, polar kum masaları için yazılmış. Web arayüzünden desen yükle,
sıraya al, hız/parlaklık ayarla.

Repo: https://github.com/tuanchris/dune-weaver

Kurulum (özet):
1. ESP32'ye firmware'i yükle (PlatformIO veya hazır `.bin`).
2. `config.h` içinde:
   - `THETA_STEPS_PER_REV` ve `RHO_STEPS_PER_MM` değerlerini mekaniğine göre kalibre et
     (pulley diş sayısı, mikro-adım, kayış adımı, MGN12 menzili).
   - Pinleri `hardware/pcb/README.md`'deki haritaya göre ayarla.
   - `LED_PIN`, `LED_COUNT` (WS2812B sayısı) gir.
3. İlk açılışta ESP32 bir Wi-Fi AP açar → bağlan → ev Wi-Fi'ına ekle.
4. Tarayıcıdan `http://duneweaver.local` → desen kütüphanesi.

Kalibrasyon ipucu: ρ ekseni "home" konumunda merkez (ρ=0), dış kenar ρ=max.
θ home için bir opto/mikro switch ile sıfır açıyı sabitle.

## Seçenek B — FluidNC (GRBL, ESP32) + polar kinematik
Daha çok kontrol istersen FluidNC kullan ve `.thr` dosyalarını G-code'a çevir.
- FluidNC: https://github.com/bdring/FluidNC
- Polar masada genelde gönderici tarafında theta-rho → XY/G-code dönüşümü yapılır.
  `sandify` doğrudan polar (.thr) ve G-code çıktısı verebilir.

## Desen üretimi — Sandify (her iki seçenekte de)
Tarayıcıda çalışır, kurulum yok: https://sandify.org
- Şekiller, spiraller, yıldız/çiçek desenleri, kendi yörüngeni çiz.
- **Export → Theta Rho (.thr)** Dune Weaver için, veya **G-code** FluidNC için.
- Üretilen `.thr` dosyalarını Dune Weaver web arayüzüne yükle → hazır
  desen kütüphanen oluşur (ürünün satış değerinin bir kısmı budur).

## Kalibrasyon checklist
- [ ] Mikro-adım (TMC2209 örn. 1/16) firmware ile uyumlu
- [ ] θ tam tur = doğru adım sayısı (görsel: 1 tur dön, kayma yok)
- [ ] ρ home (merkez) ve ρ max (kenar) sınırları doğru, bilye cama değmiyor
- [ ] Mıknatıs gücü bilyeyi kaybetmeden sürüklüyor (hız vs. kuvvet dengesi)
- [ ] LED parlaklığı 5V akım bütçesini aşmıyor (60 LED ≈ 3.6A tepe @ tam beyaz)
