# O-Voice-Hub-Offline — Çevrimdışı Yapay Zeka & Donanım Asistanı

Bu proje, Ubuntu ve Linux tabanlı sistemler üzerinde çalışmak üzere tasarlanmış, **tamamen çevrimdışı (offline)** çalışan ve fiziksel donanımları kontrol edebilen bir yapay zeka sesli asistanıdır.

Bulut tabanlı standart asistanların aksine, ses verilerinizi hiçbir uzak sunucuya göndermez; tüm dinleme, anlama ve konuşma süreçlerini bilgisayarınızın yerel donanım gücünü kullanarak gerçekleştirir. Asistanın ses tanıma motoru olarak OpenAI'ın *Whisper* modeli, ses sentezi motoru olarak ise yerel olarak çalışan *Coqui XTTS v2* ses klonlama modeli kullanılmıştır. Donanım kontrolcüsü olarak seri port üzerinden haberleşilen bir *Arduino* kullanılmıştır.

---

## 🌟 Özellikler

* **Tamamen İnternetsiz Çalışma:** Kurulum aşamasından sonra hiçbir Wi-Fi veya ağ bağlantısına ihtiyaç duymaz.
* **Ses Klonlama (XTTS v2):** Coqui XTTS v2 modeliyle `benim_sesim.wav` referans dosyasından klonlanan sesle konuşur; GPU varsa otomatik olarak CUDA üzerinde çalışır.
* **Wake Word Sistemi:** Yalnızca `"Hey Car"` komutuyla aktive olur, sürekli dinlemez.
* **İngilizce Ses Tanıma:** Whisper modeli (`base`) İngilizce komutları algılar.
* **Fiziksel Donanım Kontrolü (Arduino Entegrasyonu):** USB üzerinden Arduino'ya sinyaller göndererek 3 ayrı LED'i (sol sinyal, farlar, sağ sinyal) bağımsız olarak kontrol eder.
* **Dinamik Komut Yönetimi:** `komutlar.json` dosyasını düzenleyerek sınırsız yeni komut eklenebilir.

---

## ⚙️ Kurulum

### 1. Sistemi Güncelleme ve Gereksinimleri Yükleme

```bash
sudo apt update && sudo apt upgrade -y
sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg -y
```

### 2. Python Kütüphanelerini Yükleme

```bash
pip install -r requirements.txt
```

### 3. XTTS v2 Modelini İndirme

Aşağıdaki betiği çalıştırarak model dosyalarını proje dizinindeki `xtts_v2_local` klasörüne indirin. Bu işlem internet hızına bağlı olarak birkaç dakika sürebilir ve yalnızca bir kez yapılması yeterlidir:

```python
from huggingface_hub import snapshot_download

print("Model dosyaları 'xtts_v2_local' klasörüne indiriliyor. Bu işlem internet hızına bağlı olarak birkaç dakika sürebilir...")

snapshot_download(
    repo_id="coqui/XTTS-v2",
    local_dir="xtts_v2_local",
    local_dir_use_symlinks=False
)

print("İndirme tamamlandı!")
```

> **Not:** İndirme tamamlandıktan sonra sistem tamamen çevrimdışı çalışır. İndirme işlemi için tek seferlik internet bağlantısı gerekmektedir.

### 4. Ses Klonu Oluşturma

XTTS v2, konuşma sesi için bir referans dosyasına ihtiyaç duyar. Proje dizinine `benim_sesim.wav` adında en az 6-10 saniyelik, net ve gürültüsüz bir ses kaydı yerleştirin.

### 5. Donanım Bağlantısı (Arduino)

1. `main.ino` dosyasını Arduino IDE ile kartınıza yükleyin.
2. LED'lerinizi şu pinlere bağlayın:
   - **LED 1 (Sol Sinyal):** Pin 11
   - **LED 2 (Farlar):** Pin 12
   - **LED 3 (Sağ Sinyal):** Pin 13
3. Arduino port iznini aşağıdaki komutla ayarlayın:

```bash
sudo usermod -a -G dialout $USER
```

> **Not:** Bu komutu çalıştırdıktan sonra iznin sisteminize tam olarak işlemesi için bilgisayarınızı yeniden başlatmanız gerekmektedir.

4. `main.py` dosyasındaki `ARDUINO_PORT` değerini kendi Arduino portunuza göre güncelleyin.
   - Linux: `/dev/ttyUSB0` veya `/dev/ttyACM0`

### 6. Asistanı Çalıştırma

```bash
python3 main.py
```

---

## 🎙️ Örnek Komutlar

Sistem çalıştıktan sonra önce **"Hey Car"** diyerek asistanı aktive edin, ardından komutunuzu verin:

| Komut | Açıklama |
|---|---|
| "Hey Car, hello" / "hi" / "greetings" | Asistanı selamlar |
| "Hey Car, what time is it?" | Güncel saati sesli bildirir |
| "Hey Car, what is today?" | Güncel tarihi sesli bildirir |
| "Hey Car, turn on headlights" / "headlights on" | Far LED'ini (Pin 12) açar |
| "Hey Car, turn off headlights" / "headlights off" | Far LED'ini (Pin 12) kapatır |
| "Hey Car, turn on left blinker" / "left blinker on" | Sol sinyal LED'ini (Pin 11) açar |
| "Hey Car, turn off left blinker" / "left blinker off" | Sol sinyal LED'ini (Pin 11) kapatır |
| "Hey Car, turn on right blinker" / "right blinker on" | Sağ sinyal LED'ini (Pin 13) açar |
| "Hey Car, turn off right blinker" / "right blinker off" | Sağ sinyal LED'ini (Pin 13) kapatır |
| "Hey Car, shut down" / "goodbye" / "exit" | Programdan güvenli çıkış yapar |

> **Not:** Tüm komut anahtar kelimeleri ve sistem yanıtları `komutlar.json` dosyasından yönetilmektedir.

---

## 📁 Dosya Yapısı

```
├── main.py            # Ana Python asistan uygulaması
├── komutlar.json      # Sesli komut anahtarları ve sistem cevapları
├── main.ino           # Arduino LED kontrol kodları
├── benim_sesim.wav    # XTTS v2 için ses klonu referans dosyası
├── xtts_v2_local/     # İndirilen Coqui XTTS v2 model dosyaları
└── requirements.txt   # Gerekli Python kütüphaneleri listesi
```

---

## 📄 License

This project is licensed under a **Non-Commercial License**.

You may use, modify, and share this project for **personal, educational, and non-commercial purposes only**.

🚫 **Commercial use is strictly prohibited** without prior written permission from the author.

For commercial licensing inquiries, please contact the author.
See the LICENSE file for full details.