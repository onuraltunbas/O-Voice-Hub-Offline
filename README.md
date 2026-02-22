# Çevrimdışı (Offline) Yapay Zeka & Donanım Asistanı

Bu proje, Ubuntu ve Linux tabanlı sistemler üzerinde çalışmak üzere tasarlanmış, **tamamen çevrimdışı (offline)** çalışan ve fiziksel donanımları kontrol edebilen bir yapay zeka sesli asistanıdır.

Bulut tabanlı standart asistanların aksine, ses verilerinizi hiçbir uzak sunucuya göndermez; tüm dinleme, anlama ve konuşma süreçlerini bilgisayarınızın yerel donanım gücünü kullanarak gerçekleştirir. Asistanın ses işleme motoru olarak OpenAI'ın *Whisper* modeli, donanım kontrolcüsü olarak ise seri port üzerinden haberleştiği bir *Arduino* kullanılmıştır.

### 🌟 Asistanın Temel Yetenekleri

* **Tamamen İnternetsiz Çalışma:** Kurulum aşamasından sonra hiçbir Wi-Fi veya ağ bağlantısına ihtiyaç duymaz.
* **Çift Dilli (Bilingual) Ses Tanıma:** Hem Türkçe hem de İngilizceyi otomatik olarak algılar.
* **Fiziksel Donanım Kontrolü (Arduino Entegrasyonu):** USB üzerinden Arduino'ya sinyaller göndererek röleleri, aydınlatma sistemlerini veya motorları kontrol eder.
* **Sesli Geri Bildirim:** `pyttsx3` aracılığıyla kullanıcıya sesli durum bildirimi yapar.
* **Dinamik Komut Yönetimi:** `komutlar.json` dosyasını düzenleyerek sınırsız yeni komut eklenebilir.

---

### ⚙️ Kurulum Adımları

### 1. Sistemi Güncelleme ve Gereksinimleri Yükleme
```bash
sudo apt update && sudo apt upgrade -y
sudo apt-get install portaudio19-dev python3-pyaudio espeak ffmpeg -y
```

### 2. Python Kütüphanelerini Yükleme
```bash
pip install -r requirements.txt
```

### 3. Arduino Port İzinlerini Ayarlama
```bash
sudo usermod -a -G dialout $USER
```

> **Not:** Bu komutu çalıştırdıktan sonra iznin sisteminize tam olarak işlemesi için bilgisayarınızı yeniden başlatmanız gerekmektedir.

### 4. Whisper Yapay Zeka Modelini İndirme
```bash
python3 -c 'import whisper; print("Model indiriliyor, lutfen bekleyin..."); whisper.load_model("base"); print("Indirme tamamlandi, sistem tamamen cevrimdisi calismaya hazir.")'
```

### 5. Asistanı Çalıştırma
```bash
python3 main.py
```