# O-Voice-Hub-Offline

Tamamen çevrimdışı çalışan, ses klonlama ve Arduino donanım kontrolü destekli yapay zeka sesli asistan.

**Ses Tanıma:** OpenAI Whisper (base) — **TTS:** Coqui XTTS v2 — **Donanım:** Arduino (Seri Port)

---

## Gereksinimler

- Ubuntu / Debian tabanlı Linux
- Python 3.10+
- Arduino (isteğe bağlı)
- GPU önerilir (CPU ile de çalışır)

---

## Kurulum

### 1. Sistem bağımlılıkları

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install portaudio19-dev python3-pyaudio ffmpeg -y
```

### 2. Python kütüphaneleri

```bash
pip install -r requirements.txt
```

### 3. XTTS v2 modelini indir

(internet bağlantısı gerekir, ~2GB — yalnızca bir kez yapılır):

```bash
python3 download_model.py
```

> İndirme tamamlandıktan sonra sistem tamamen çevrimdışı çalışır.

### 4. Ses klonu referans dosyası

Proje dizinine `benim_sesim.wav` adında **en az 6–10 saniyelik**, net ve gürültüsüz bir ses kaydı koy.

### 5. Arduino kurulumu (isteğe bağlı)

1. `main.ino` dosyasını Arduino IDE ile kartına yükle.
2. LED bağlantıları:

   | LED | Pin |
   |-----|-----|
   | Sol Sinyal | 11 |
   | Farlar | 12 |
   | Sağ Sinyal | 13 |

3. Port iznini ver:

```bash
sudo usermod -a -G dialout $USER
# Ardından bilgisayarı yeniden başlat
```

4. `main.py` içindeki `ARDUINO_PORT` değerini kendi portuna göre güncelle:
   - `/dev/ttyUSB0` veya `/dev/ttyACM0`

> Arduino bağlı değilse sistem yine çalışır; donanım komutları devre dışı kalır.

---

## Çalıştırma

```bash
python3 main.py
```

---

## Kullanım

Asistanı aktive etmek için önce **"Hey Car"** de, ardından komutunu ver.

| Komut | İşlev |
|-------|-------|
| `hello` / `hi` / `greetings` | Selamlama |
| `what time is it` | Saati söyler |
| `what is today` | Tarihi söyler |
| `turn on headlights` | Farları açar (Pin 12) |
| `turn off headlights` | Farları kapatır |
| `turn on left blinker` | Sol sinyali açar (Pin 11) |
| `turn off left blinker` | Sol sinyali kapatır |
| `turn on right blinker` | Sağ sinyali açar (Pin 13) |
| `turn off right blinker` | Sağ sinyali kapatır |
| `shut down` / `goodbye` / `exit` | Programdan çıkar |

Yeni komut eklemek için `komutlar.json` dosyasını düzenle.

---

## Dosya Yapısı

```
├── main.py            # Ana uygulama
├── main.ino           # Arduino LED kontrol kodu
├── komutlar.json      # Komut tanımları ve yanıtlar
├── download_model.py  # XTTS v2 model indirme betiği
├── requirements.txt   # Python bağımlılıkları
├── benim_sesim.wav    # Ses klonu referans dosyası (kendin ekle)
└── xtts_v2_local/     # XTTS v2 model dosyaları (kendin indir)
```

---

## Lisans

**Non-Commercial License** — Kişisel ve eğitim amaçlı kullanım serbesttir.  
Ticari kullanım yazılı izin gerektirmektedir.