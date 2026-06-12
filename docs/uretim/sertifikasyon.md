# Sertifikasyon & Uyumluluk Yol Haritası

Premium, **şebeke beslemeli (adaptörlü), ağ bağlantılı, ağır cam + güçlü mıknatıs** içeren bir
mobilya-elektronik ürünü global satmak için gerekenler. Bunlar **pazarlık dışı** — yoksa yasal satılamaz.

> Strateji: ürün **SELV (≤24V DC)** tarafında kalsın; şebeke gerilimi **harici, zaten sertifikalı
> bir adaptörde** olsun → ürünün kendi sertifikasyon yükü ciddi azalır (en kritik tasarım kararı).

## 1) Hedef pazara göre zorunlu işaretler
| Pazar | İşaret / standart | Kapsam |
|---|---|---|
| **AB** | **CE** — EMC 2014/30, LVD/(adaptör), **EN 62368-1** (AV/BT emniyet), **RoHS** 2011/65, **REACH**, WEEE | emniyet + EMC + kimyasal + e-atık |
| **AB radyo** | **RED 2014/53** (Wi-Fi/BT) | telsiz modülü (ESP32) — **ön-sertifikalı modül kullan** |
| **ABD** | **FCC Part 15B** (+15C telsiz) | EMC / radyo |
| **İngiltere** | **UKCA** | CE muadili |
| **Kanada** | ISED | radyo |
| **Genel** | **EN 60335** (ev aletleri) *veya* 62368-1 + mobilya **devrilme/stabilite** | mekanik emniyet |

## 2) Ürün-özel emniyet riskleri (test edilmeli)
- **Güçlü mıknatıs (N52):** sıkışma/yutma; çocuk erişimi; manyetik alan (kalp pili uyarısı, ambalaj ikazı).
- **Temperli cam:** kırılma davranışı (temperli zorunlu), kenar emniyeti, yük dayanımı.
- **Devrilme/stabilite:** sehpa standardı (örn. ağırlık + ayak açısı; biz 8° splay + SF 5.2× ile tasarladık).
- **Isınma:** motor/sürücü yüzey sıcaklığı sınırları; uzun çalışmada.
- **Sıkışma:** mıknatıslı üst modül (≈21.6 kgf) — parmak ikazı + tasarımsal emniyet.

## 3) Akış ve tahmini bütçe (TR'den global)
| Adım | Ne | Tahmini maliyet | Süre |
|---|---|---|---|
| Ön-uyumluluk (pre-scan) | EMC ön-tarama (akredite lab) — erken hata yakala | 15–40k ₺ | 1–2 hafta |
| Tasarım düzeltme | filtre, kılıflama, topraklama | mühendislik | — |
| **CE dosyası** | EMC + 62368 emniyet testi + teknik dosya + DoF (Declaration of Conformity) | 80–200k ₺ | 4–8 hafta |
| **FCC** | Part 15B (ABD hedefliyse) | 60–150k ₺ | 3–6 hafta |
| RoHS/REACH | malzeme beyanı + (gerekirse) test | 10–30k ₺ | 1–3 hafta |
| Telsiz | **ön-sertifikalı ESP32 modülü** → modül sertifikası devral (büyük tasarruf) | düşük | — |

> Rakamlar TR akredite lab (TÜRKAK) / TÜV SÜD / Intertek / SGS / Eurofins seviyesi tahminidir;
> kapsam ve adetle değişir. **Modül sertifikası devralma** ve **harici adaptör** en büyük iki tasarruf.

## 4) Akredite test lab seçenekleri (TR / global)
TÜV SÜD · TÜV Rheinland · Intertek · SGS · Eurofins · UL · (TR akredite EMC labları).
Erken aşamada **bir labla ön-görüşme** → kapsam/maliyet netleşir.

## 5) Tasarım tarafında şimdi yapılabilecekler (pre-compliance)
- **Ön-sertifikalı ESP32 modülü** (FCC/CE/RED ID'li) seç → telsiz testini büyük oranda atla.
- **Harici CE'li adaptör** (12V DC) → şebeke emniyeti adaptörde.
- **EMC için PCB'de:** giriş filtresi, ferrit, düzgün GND, ekranlı motor kablosu (Rev-C'de eklenebilir).
- **Topraklama / SELV ayrımı**, sigorta (zaten Rev-B'de).
- Kullanım kılavuzunda **mıknatıs/cam/çocuk** ikazları + ambalaj sembolleri.

## 6) Belgeler (teknik dosya içeriği)
Teknik dosya, DoF, test raporları, risk analizi ([FMEA](fmea.md)), şema/PCB, BOM, kullanım kılavuzu,
etiket/işaretleme. Üretim sürekliliği için **üretim kontrolü** (FAI/QA — [QA fişi](QA_kontrol_listesi.md)).

> **Önce hangi pazar?** AB+TR ile başla (CE+UKCA yoksa bile AB), ABD'yi (FCC) ölçeklerken ekle.
> İlk hedef tek pazar → maliyet/odak.
