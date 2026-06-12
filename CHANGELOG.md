# Değişiklik Geçmişi — DEVRAN

[Keep a Changelog](https://keepachangelog.com/tr/) biçimine yakın. Tarihler yaklaşık.

## [Devam ediyor]
- Fusion'da COTS (MGN12, lazy-susan, slip ring) fit doğrulama
- PCB Rev-B fiziksel prototip + bring-up testi
- Gerçek prototip fotoğraf/video (satış görseli)
- CE / elektrik güvenlik belgelendirme

## Marka & sunum
- **Marka kimliği:** DEVRAN adı + polar-spiral logo/favicon, tüm site + dokümanlara uygulandı
- **Profesyonel datasheet** (D60 spec sheet) + **iş/yatırım pitch** PDF
- **Modern web sitesi** baştan: premium dark tema, her doküman ayrı sayfa (MD→HTML), hub
- **Teknik çizim montaj** PDF (2D ölçülü, antet bloğu) — 3D render kılavuzuna ek
- Profesyonel README + bu CHANGELOG

## Üretim paketi
- **PCB Rev-B:** UART adresleme, WS2812 level-shifter, giriş koruması, bulk cap, EN pull-up
  → yeniden route (196 iz, 0 short); **JLCPCB paketi** (Gerber+BOM+CPL)
- **Mekanizma tasarımı:** θ/ρ kinematik + kesit + çözünürlük hesabı + slip ring
- **Mekanik DXF + STEP** (şasi/ayak/kol) · **IKEA tarzı montaj kılavuzu** (PDF)
- **Elektrik:** harness şeması + pinout + slip ring haritası + **QA/FCT test fişi**
- **Üretim gerçekleme dosyası** (NPI/EVT-DVT-PVT, test planı, COGS, risk)
- **BOM + maliyet** (TR tedarik) + hedef MSRP · **FluidNC config** (PCB pinmap ile eşleşir)
- **Gerçek oluk** (heightmap displacement): bilye kumu gerçekten oyar

## Görsel & simülasyon
- **AgX** tone mapping + sığ DOF + 512 spp fotogerçekçi render'lar
- **Reklam videosu:** ilerleyen ışıklı oluk → Atatürk imzası net çiziliyor
- **İnteraktif 3D sim** (Three.js): desen seç → çiz, parçalara ayır; ayna/cam/kontrol düzeltmeleri
- Atatürk imzası `.thr` deseni (skeletonize + NN path)

## Temel
- KiCad PCB (ESP32 + 2× TMC2209 + WS2812 + güç), Freerouting tam routing
- Blender prosedürel sahne (`scene.py`), `.thr` desen üreteçleri
- Proje kurulumu, GitHub repo
