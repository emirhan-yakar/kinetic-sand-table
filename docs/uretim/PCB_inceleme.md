# PCB Elektriksel İnceleme — dürüst değerlendirme

**Kart:** ESP32 + 2× TMC2209 + WS2812 + güç (`hardware/pcb/controller.kicad_pcb`)

## Durum (net)
- ✅ KiCad'de tasarlandı, Freerouting ile tam yönlendirildi, **DRC temiz** (0 short, 0 ratsnest, 0 bakır clearance).
- ✅ Final Gerber + STEP + Excellon üretildi (fab formatında).
- ❌ **Fiziksel olarak ÜRETİLMEDİ, lehimlenmedi, ölçülmedi, test edilmedi.**
- ⚠️ Aşağıdaki **elektriksel inceleme bulguları üretimden önce düzeltilmelidir** (Rev-B).

> DRC "geometri/clearance" kontrolüdür — **devrenin doğru çalışacağını garanti etmez.**
> Aşağıdakiler ancak gözden geçirme ile yakalanır.

---

## Bulgular ve düzeltmeler (üretim öncesi ZORUNLU)

| # | Bulgu | Risk | Düzeltme (Rev-B) |
|---|---|---|---|
| 1 | **TMC2209 UART adres çakışması** — A1 ve A2'nin MS1/MS2 pinleri aynı nete (N_MS1/N_MS2) bağlı → iki sürücü **aynı UART adresi** → ayrı ayrı adreslenemez | Yüksek (UART config çalışmaz) | Her sürücüye **ayrı adres**: A1 MS1=GND,MS2=GND (adr 0); A2 MS1=VIO,MS2=GND (adr 1). MS pinlerini ayır. |
| 2 | **WS2812 data seviye uyumu** — DIN 3.3V (GPIO4 üzerinden 330Ω); 5V WS2812 HIGH eşiği ~3.5V > 3.3V | Orta (kararsız LED) | **Level shifter** (74AHCT125) 3.3→5V, veya ilk pikseli ~4.3V besle, ya da 3.3V toleranslı SK6812. |
| 3 | **Yarım-çift UART eksik bağlantı** — sürücü PDN_UART tek hat; ESP32 TX→1k→PDN ve RX←PDN gerekir; mevcut tasarımda 1k yok, RX hattı sürücülere bağlı değil | Orta (UART iletişim) | TX'e **1kΩ** seri + RX'i PDN hattına bağla (tek-hat half-duplex). |
| 4 | **VM (12V) bulk kondansatör yok** — sürücü yanında 12V tampon eksik (datasheet ≥100µF önerir) | Orta (motor gürültü/reset) | Her sürücü VM'ine yakın **100µF/25V** + 100nF. |
| 5 | **Giriş koruması yok** — 12V girişte ters polarite koruması ve sigorta yok | Orta (yanlış bağlantıda hasar) | **P-MOSFET ters polarite** + **sigorta/PTC** (örn. 5A). |
| 6 | **EN boot durumu** — sürücü EN (active-low) boot anında belirsiz → motor istem dışı sürülebilir | Düşük/Orta | **10kΩ pull-up** (EN→VIO) → boot'ta sürücüler pasif. |
| 7 | **GPIO5 strapping** — ρ DIR = GPIO5 (strapping pin) | Düşük | TMC DIR yüksek-Z giriş olduğu için kabul edilebilir; istenirse non-strapping GPIO (33) kullan. |

## Basitleştirme önerisi (EVT için risk azaltıcı)
İlk prototipte **UART'ı atla, sürücüleri standalone modda** kullan (MS1/MS2/SPREAD pinleriyle
mikro-adım + akım onboard ayar). FluidNC STEP/DIR ile çalışır; #1 ve #3 bulguları **ortadan kalkar.**
UART'ı (runtime akım/mikroadım) DVT'de ekle. → daha az arıza noktası, daha hızlı bring-up.

## Üretim öncesi adım sırası
1. Rev-B: bulguları KiCad'de uygula (build_kicad.py'de net/komponent ekle), DRC + **göz incelemesi**.
2. (Önerilir) hızlı **breadboard doğrulaması**: ESP32 + 2 TMC2209 modül + 1 LED → FluidNC bring-up,
   hat/pin doğrula → ardından PCB'ye geç.
3. PCB'yi **5 adet** bastır+dizgi (yedekli), `bring-up` testi (`URETIM_DOSYASI.md` §5.1).
4. Firmware entegrasyon testi → DVT.

## Güç bütçesi (kontrol)
- 5V: ESP32 ~0.25A + sürücü VIO ~0.05A + **WS2812 60 LED × ~60mA(max) = 3.6A** → buck **≥4–5A** şart (BOM'da var). İdle/tipik çok düşük; max tam-beyaz tasarım sınırı.
- 12V: 2× NEMA17 ~0.6–0.9A/faz → ~2–3A tepe → 12V 6A SMPS yeterli.
