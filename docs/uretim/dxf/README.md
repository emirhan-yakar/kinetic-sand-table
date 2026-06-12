# CNC / Lazer Kesim DXF Dosyaları

Alüminyum şasi, ayak plakası ve dönen kol için 2D kesim dosyaları (mm, DXF R2010).
Lazer / CNC router / su jeti atölyesine doğrudan gönderilebilir.

| Dosya | Parça | Malzeme / kalınlık | Adet |
|---|---|---|---|
| `sasi.dxf` | Mekanizma şasi diski Ø520 | Alüminyum **6082 / 5754, 4 mm** | 1 |
| `ayak_plakasi.dxf` | Ayak bağlantı plakası 60×60 | Alüminyum 4 mm veya çelik 3 mm | **4** |
| `kol.dxf` | Dönen kol (θ) 320×40 | Alüminyum 5 mm | 1 |

Her `.dxf` yanında `*_preview.png` (görsel kontrol).

## 3D STEP (mekanik CAD doğrulama)
Aynı parçalar **3D katı** olarak da var (`*.step`) — Fusion 360 / FreeCAD / SolidWorks'te
açıp montaj/fitment doğrulamasına başlamak için (`make_step.py`, cadquery ile üretildi):
`sasi.step` (Ø520×4, 820 cm³) · `ayak_plakasi.step` (60×60×4) · `kol.step` (320×40×5).
> Bunlar **kesim parçalarının** katılarıdır; tam fitment için satın alınan COTS parçaları
> (MGN12 ray, lazy-susan, slip ring, NEMA17) CAD'e ekleyip doğrula.

## Delik şeması (özet)
- **Şasi:** dış Ø520 · drum bağlantı 4× M4 @ Ø500 PCD · merkez Ø90 (slip ring + kayış boşluğu) ·
  turntable 4× M4 @ Ø120 · θ motor NEMA17 (Ø22 + 4× M3 @ 31×31, offset) · PCB 4× M3 (92×67) · kablo yuvası.
- **Ayak plakası:** 60×60 · 4× M5 @ 36×36 · merkez Ø20 (ayak tenon). **8° splay açısı plakada değil,
  eğimli ayak/braket veya ara takozda** verilir (DXF düz kesimdir).
- **Kol:** pivot ucu 4× M3 @ Ø30 + merkez Ø8 · MGN12 ray M3 @ 20 mm · ρ motor NEMA17 ucu.

## ⚠️ Üretim öncesi doğrulama (ZORUNLU)
Delik konumları **temsilidir** — atölyeye göndermeden önce **gerçek parçalarla** doğrula:
- **MGN12 ray** delik pitch'i (20 vs 25 mm) → satın alınan raya göre.
- **Lazy-susan / turntable** civata dairesi → satın alınan rulmana göre.
- **Slip ring** gövde/bore çapı → seçilen modele göre (merkez Ø90 boşluk).
- **NEMA17** = standart (31×31 M3, Ø22 pilot) ✓.
- Toleranslar: gecme delikler (M3=3.2, M4=4.5, M5=5.5); sıkı geçme gerekiyorsa düşür.

> Bunlar 2D **kesim** dosyalarıdır; 3D montaj/açı için `montaj.md`, `montaj_sheet.svg`,
> `montaj_patlatma.png`. Nihai mekanik CAD (Fusion 360 / SolidWorks) ile son kontrol önerilir.

## Yeniden üretmek
```
python3 make_dxf.py    # ezdxf gerekir:  pip install ezdxf
```
Ölçüler `make_dxf.py` başındaki sabitlerden (montaj_hesap.py ile tutarlı) gelir.
