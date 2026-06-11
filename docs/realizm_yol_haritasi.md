# Gerçeklik Yol Haritası — sonraki aşamalar

Mevcut durum: kod-tabanlı Blender/Cycles render (stüdyo HDRI + gerçek PBR doku) + WebGL simülasyon.
"Gerçekten gerçek" hisse ulaşmak için aşamalar (etkili → maliyetli sırayla):

## 1) Kum oluğu = gerçek geometri (en yüksek etki)
Şu an desen, kumun üstünde ince bir **çizgi/tüp**. Gerçekte bilye kumda **oluk açar**:
çukur + iki yanda kabarma (berm) + grenli gölge.
- **Render:** kumu yüksek alt-bölmeli mesh yap; `.thr` yolundan bir **yükseklik haritası (heightmap)**
  üret (yol boyunca Gauss çukur + kenar kabarma) → **displacement** modifier. Cycles adaptive subdiv.
  Bilye geçtikçe gerçek gölge/AO oluşur → fotoğraf gibi.
- **Sim (WebGL):** aynı heightmap'i bir doku olarak kuma uygula (normal/parallax); bilye ilerledikçe
  heightmap'e çukur "boya" (render-to-texture) → canlı oyulan kum.

## 2) Mekanizmanın görünür çalışması
Bilye tek başına yörünge izliyor; gerçekte **dönen kol + taşıyıcı + mıknatıs** kumun altında hareket eder.
- θ-ρ kinematiğini hesapla: her kare bilyenin (theta,rho)'suna göre kolu döndür, taşıyıcıyı kaydır,
  mıknatısı bilyenin tam altına koy. Hem sim hem video bunu göstersin → mekanizma inandırıcı olur.

## 3) Render kalitesi (foto-kalibrasyon)
- **Sample** 384 → 1024+, **DOF/bokeh**, hafif **film grain + kromatik** (gerçek lens hissi).
- **Kostik:** cam → kum ışık kırılması (Cycles caustics / MNEE) → cam gerçekçiliği büyük sıçrar.
- **Gerçek referans:** benzer ürün fotoğraflarıyla ışık/poz eşle.

## 4) Malzeme doğrulama (ölçülü PBR)
- Gerçek **ceviz, kum, cam** örneklerini tarayıp (polarized foto / fotogrametri) doğru
  albedo–roughness–normal çıkar. Tahmini değerler yerine ölçülmüş → "CG kokusu" gider.
- Kum: gerçek granül boyutu/rengi (kuvars vs silis), nemli/kuru sheen.

## 5) WebGL simülasyon gerçekçiliği
- Gerçek **HDRI environment** (zaten studio.hdr) + **SSAO** + **yumuşak gölge** + **DOF**.
- Kum **parallax/normal** shader; oluk için (1)'deki heightmap.
- Alternatif: gerçekçilik kritikse, sim yerine **pre-rendered döngü video** (Cycles) göster;
  etkileşim için ayrı basit sim. (Gerçek zamanlı asla TV-reklam fotoğraf-gerçekçiliğinde olmaz.)

## 6) Fiziksel prototip → gerçek foto/video (altın standart)
CAD render hiçbir zaman %100 değil. **Gerçek prototip** üretip (BOM + montaj hazır) gerçek
fotoğraf/video çekmek, en inandırıcı "reklam" malzemesidir. Render'lar ön-görselleştirme;
satış görseli için fiziksel ürün şart.

## Öncelik önerisi
1 (oluk geometrisi) + 2 (mekanizma hareketi) → görselin "gerçek cihaz" hissini en çok artıran ikisi.
Sonra 3–4 (render/materyal kalibrasyonu). Nihai: 6 (gerçek prototip).
