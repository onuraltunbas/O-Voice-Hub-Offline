# O-Voice-Hub-Offline — Çevrimdışı Sesli Kontrol & Otomasyon Asistanı

Bu proje, Ubuntu ve Linux tabanlı sistemler üzerinde çalışmak üzere tasarlanmış, **tamamen çevrimdışı (offline)** çalışan ve fiziksel donanımları kontrol edebilen bir yapay zeka sesli asistanıdır.

Bulut tabanlı standart asistanların aksine, ses verilerinizi hiçbir uzak sunucuya göndermez; tüm dinleme, anlama ve konuşma süreçlerini bilgisayarınızın yerel donanım gücünü kullanarak gerçekleştirir. Asistanın ses işleme motoru olarak OpenAI'ın *Whisper* modeli, donanım kontrolcüsü olarak ise seri port üzerinden haberleştiği bir *Arduino* kullanılmıştır.

---

## 🌟 Özellikler

* **Tamamen İnternetsiz Çalışma:** Kurulum aşamasından sonra hiçbir Wi-Fi veya ağ bağlantısına ihtiyaç duymaz.
* **Çift Dilli (Bilingual) Ses Tanıma:** Hem Türkçe hem de İngilizceyi otomatik olarak algılar.
* **Fiziksel Donanım Kontrolü (Arduino Entegrasyonu):** USB üzerinden Arduino'ya sinyaller göndererek röleleri, aydınlatma sistemlerini veya motorları kontrol eder.
* **Sesli Geri Bildirim:** `pyttsx3` aracılığıyla kullanıcıya sesli durum bildirimi yapar.
* **Dinamik Komut Yönetimi:** `komutlar.json` dosyasını düzenleyerek sınırsız yeni komut eklenebilir.

---

## ⚙️ Kurulum

### 1. Sistemi Güncelleme ve Gereksinimleri Yükleme

```bash
sudo apt update && sudo apt upgrade -y
sudo apt-get install portaudio19-dev python3-pyaudio espeak ffmpeg -y
```

### 2. Python Kütüphanelerini Yükleme

```bash
pip install -r requirements.txt
```

### 3. Donanım Bağlantısı (Arduino)

1. `main.ino` dosyasını Arduino IDE ile kartınıza yükleyin.
2. Kontrol etmek istediğiniz donanımı (röle, LED vb.) ilgili pinlere bağlayın.
3. Arduino port iznini aşağıdaki komutla ayarlayın:

```bash
sudo usermod -a -G dialout $USER
```

> **Not:** Bu komutu çalıştırdıktan sonra iznin sisteminize tam olarak işlemesi için bilgisayarınızı yeniden başlatmanız gerekmektedir.

4. `komutlar.json` dosyasındaki `ARDUINO_PORT` değerini kendi Arduino portunuza göre güncelleyin.
   - Linux: `/dev/ttyUSB0` veya `/dev/ttyACM0`

### 4. Whisper Yapay Zeka Modelini İndirme

```bash
python3 -c 'import whisper; print("Model indiriliyor, lutfen bekleyin..."); whisper.load_model("base"); print("Indirme tamamlandi, sistem tamamen cevrimdisi calismaya hazir.")'
```

### 5. Asistanı Çalıştırma

```bash
python3 main.py
```

---

## 🎙️ Örnek Komutlar

Sistem çalıştıktan sonra mikrofonunuzdan şu tarz komutlar verebilirsiniz:

| Komut | Açıklama |
|---|---|
| "Işıkları aç" / "Işıkları kapat" | Aydınlatma rölesini kontrol eder |
| "Motoru çalıştır" / "Motoru durdur" | Motor kontrolü yapar |
| "Sistemleri kapat" | Programdan güvenli çıkış yapar |



---

## 📁 Dosya Yapısı

```
├── main.py            # Ana Python asistan uygulaması
├── komutlar.json      # Sesli komut anahtarları ve sistem cevapları
├── main.ino           # Arduino donanım kontrol kodları
└── requirements.txt   # Gerekli Python kütüphaneleri listesi
```

---

## 📄 License

This project is licensed under a **Non-Commercial License**.

You may use, modify, and share this project for **personal, educational, and non-commercial purposes only**.

🚫 **Commercial use is strictly prohibited** without prior written permission from the author.

For commercial licensing inquiries, please contact the author.
See the LICENSE file for full details.