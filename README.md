# Kinetik Kum Sanatı Masası — Üretim Projesi (Polar / Theta-Rho, Ø60+ cm)

Nikolatoy "Home Art Sand Painting Coffee Table" benzeri bir ürünün Türkiye'de
üretilebilir, açık tasarımlı versiyonu. Yuvarlak büyük masa için **polar
(theta-rho)** mekanik mimari kullanılır — gerçek Sisyphus masalarının çalışma
prensibi budur.

## Nasıl çalışır?
Cam yüzeyin altında dönen bir kol (θ ekseni) ve kol üzerinde içeri/dışarı kayan
bir taşıyıcı (ρ ekseni) bir **neodyum mıknatısı** taşır. Mıknatıs, üstteki ince
kum tabakasındaki **çelik bilyeyi** sürükleyerek sonsuz desenler çizer. Kenardaki
**WS2812B RGB LED halka** sahneyi aydınlatır. Beyin bir **ESP32**'dir ve
`.thr` (theta-rho) desen dosyalarını oynatır.

```
        ┌──────────────────────────────┐  ← Temperli cam + ince kum + çelik bilye
        │   ●  ←bilye                    │
        ├──────────────────────────────┤
        │  [mıknatıs]→ taşıyıcı (ρ)      │  ← dönen kol (θ)
        │  ════════ GT2 kayış ═══════    │
        │      ◎ lazy-susan rulman       │
        │  θ motor   ρ motor + slip ring │  ← taban (sabit)
        └──────────────────────────────┘
   Kenarda: WS2812B LED halka  |  Beyin: ESP32 (Dune Weaver firmware)
```

## Proje içeriği
| Dosya | İçerik |
|---|---|
| `BOM.md` | Tam malzeme listesi + Türkiye tedarik linkleri + maliyet (prototip & seri) |
| `hardware/sand_table.scad` | Parametrik 3D model (OpenSCAD) — gövde, kol, cam, LED halka |
| `hardware/pcb/` | Kontrol kartı: `pcb_gen.py` üreteci, **hazır Gerber + Excellon** (`gerbers/`), katman çizimleri (`plots/`), `controller.net` netlist, `board3d.scad` 3D model. Detay: `hardware/pcb/README.md` |
| `firmware/README.md` | Dune Weaver / FluidNC kurulumu + Sandify ile desen üretimi |
| `render/` | **Blender fotogerçekçi render** — `render_table.py` (prosedürel sahne, Cycles), `table_hero.png` (aydınlık) + `table_dark.png` (LED parıltılı). Bkz. `render/README.md` |
| `docs/render-recipe.md` | Render reçetesi (malzeme + ışık), `render/`'ın temeli |

## Hızlı başlangıç
1. `BOM.md` → parçaları sipariş et.
2. `hardware/sand_table.scad` → OpenSCAD'de aç, `TABLE_DIAMETER` vb. ayarla, STL al → 3D bas / lazer kestir.
3. `hardware/pcb/` → prototipte hazır kontrol kartı; seride özel PCB bastır.
4. `firmware/` → ESP32'ye Dune Weaver yükle, Wi-Fi web arayüzünden desen oynat.
5. `docs/render-recipe.md` → fotogerçekçi tanıtım görselleri.

## Referans açık kaynak projeler
- Dune Weaver (polar sand table, ESP32, web UI): https://github.com/tuanchris/dune-weaver
- Sandify (desen/theta-rho üreteci): https://sandify.org
- ZenXY / rdudhagra Sand-Table: https://github.com/rdudhagra/Sand-Table
- DIY Machines kinetik kum masası: https://www.diymachines.co.uk/kinetic-sand-art-coffee-table-self-drawing
