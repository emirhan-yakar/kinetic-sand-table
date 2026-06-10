# Blender Fotogerçekçi Render

Kinetik kum sanatı masasının (Ø60cm) prosedürel Blender sahnesi ve Cycles render'ı.
Geometri `hardware/sand_table.scad` ölçüleriyle kod içinde kurulur — harici STL/model gerekmez.

## Çalıştırma
```
BL=~/Applications/Blender.app/Contents/MacOS/Blender
"$BL" --background --python render_table.py -- hero    # aydınlık ürün çekimi
"$BL" --background --python render_table.py -- dark    # koyu LED parıltılı çekim
```
Çıktı: `table_hero.png`, `table_dark.png` (1600×1200, Cycles, Metal GPU + OpenImageDenoise).

## Çıktılar
| Dosya | Açıklama |
|---|---|
| `table_hero.png` | Aydınlık stüdyo: mat ceviz gövde + taranmış konsantrik kum deseni + çelik bilye + LED halka |
| `table_dark.png` | Koyu stüdyo: cam görünür, mavi LED halka kumu/camı aydınlatır (ambiyans) |

## Sahne özeti (`render_table.py`)
- **Geometri:** ahşap gövde (üst kısma boolean ile kum havuzu oyulur), kum diski,
  cam üst (hero'da kameradan gizli → desen net), çelik bilye, LED torus halka, ahşap çerçeve.
- **Malzemeler (Principled BSDF):** ceviz (prosedürel Wave damar, mat), cam (transmission 1,
  roughness 0.02, IOR 1.5), kum (Wave RINGS `Z` → konsantrik oluk bump + ince gren noise),
  çelik (metallic), LED (Emission).
- **Işık:** 4 area light (key/fill/rim/top) düşük `specular_factor` (cam/bilye ışık aynalamasın),
  yumuşak stüdyo dünyası. Dark modda key+rim azaltılıp LED gücü artırılır.
- **Kamera:** 50mm, 3/4 yüksek açı, DOF f/5.6.
- **Ton eşleme:** Filmic Medium Contrast.

## Ayar ipuçları
- Kum deseni belirginliği: `wring` Scale/Distortion + `bumpS` Strength.
- Pozlama: area light `energy` ve world `Strength`; oluk gölgesi için Top ışığı kıs, Key (yan) koru.
- Kalite: `scene.cycles.samples` (220 → 300+).
- Ayrıntılı malzeme/ışık reçetesi: `../docs/render-recipe.md`.
