# Fotogerçekçi Render Reçetesi (Blender Cycles / KeyShot)

`hardware/sand_table.scad` modelinden STL al → Blender'a import et (veya Fusion
360'ta yeniden modelleyip KeyShot'a gönder). Aşağıdaki reçete tanıtım/ürün
görseli kalitesinde sonuç verir.

## 1) Model hazırlığı
- OpenSCAD'de `EXPLODE=0`, `SHOW_GLASS=true`, `SHOW_SAND=true` → Export STL.
- Blender: Import STL → ölçek mm→m (0.001) kontrol et → `Shade Smooth` gövde.
- Kum yüzeyine **gerçek desen** için: Sandify'dan bir `.thr`/SVG yörüngesini
  curve olarak import et, ince oluk (displacement) olarak kuma uygula.

## 2) Malzemeler (Principled BSDF)
| Parça | Ayar |
|---|---|
| Ahşap gövde | Base color koyu ceviz doku (Roughness 0.4, hafif clearcoat) |
| Cam üst | Transmission 1.0, Roughness 0.02, IOR 1.5, ince kalınlık |
| Kum | Base color #DBC79E, Roughness 0.9 + **Displacement** (noise + desen yörüngesi) |
| Çelik bilye | Metallic 1.0, Roughness 0.08 |
| Metal mekanizma | Metallic 1.0, Roughness 0.3 |
| LED halka | Emission, renk seçilebilir (örn. mavi/turkuaz), Strength 4–8 |

## 3) Aydınlatma
- **HDRI** stüdyo ortamı (Poly Haven `studio_small_*`) — yumuşak yansıma.
- 1 ana softbox (area light, üstten 45°), 1 dolgu, 1 arka kenar ışığı.
- LED halkanın emission'ı sahneye renk sızdırsın (karanlık çekim için ortam ışığını kıs).

## 4) Kamera & kompozisyon
- 35–50mm lens, hafif üstten 3/4 açı (deseni gösterir).
- İkinci kare: tam tepeden (top-down) sadece kum deseni + LED parıltısı.
- DOF: f/4 civarı, bilyeye odak.

## 5) Render ayarları (Cycles)
- 1024–2048 sample + OpenImageDenoise.
- Film transparent (PNG, sonradan zemin) veya stüdyo zemini (soft gradient).
- Çözünürlük 2000×2000+ (ürün sayfası/e-ticaret için kare).

## 6) İki ortam çekimi
1. **Aydınlık ürün shot'u** — ahşap+cam dokusu, premium his.
2. **Karanlık ortam shot'u** — LED halka parlıyor, kum deseni ışıkla vurgulu.

## Alternatif hızlı yol
Fusion 360'ta modelle → yerleşik **Render** çalışma alanı veya KeyShot'a köprü →
hazır malzeme kütüphanesiyle dakikalar içinde fotogerçekçi çıktı.

> Not: Bu reçeteden çıkan görseller e-ticaret ürün sayfası ve reklam için yeterli
> kalitededir. İstersen Blender için hazır `.blend` sahne kurulum scriptini de
> (Python) yazabilirim.
