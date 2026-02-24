# Copyright (c) 2026 Remzican Onur Altunbaş
# Non-Commercial License
# Commercial use prohibited without permission

import json
import os
import random
import pyttsx3
import serial
import time
import speech_recognition as sr
import warnings


warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- ÇEVRİMDİŞİ SES MOTORUNU BAŞLAT ---
engine = pyttsx3.init()
engine.setProperty('rate', 140) 

# --- ARDUINO BAĞLANTISI ---
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2) 
    print("Arduino bağlantısı başarılı!")
except Exception as e:
    arduino = None
    print("Arduino bulunamadı, donanım kontrolleri devre dışı bırakıldı.")

def konus(metin):
    print("Asistan:", metin)
    engine.say(metin)
    engine.runAndWait()

def dinle():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Seni dinliyorum (TR/EN)...")
        r.adjust_for_ambient_noise(source, duration=0.5) 
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5) 
            print("Ses işleniyor... (İnternetsiz Mod)")
            
            metin = r.recognize_whisper(audio, model="base")
            
            print(f"Sen söyledin: {metin}")
            return metin.lower().strip()
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Ses algılama hatası: {e}")
            return ""

def cevapla(komut, komutlar):
    komut = komut.lower()

    for kategori, veri in komutlar.items():
        for anahtar in veri.get("anahtarlar", []):
            if anahtar in komut:
                
                # Arduino Komutları
                if kategori == "led_1_ac":
                    if arduino: arduino.write(b'1')
                    else: return "Donanım bağlantısı yok."
                elif kategori == "led_1_kapat":
                    if arduino: arduino.write(b'2')
                    else: return "Donanım bağlantısı yok."
                elif kategori == "led_2_ac":
                    if arduino: arduino.write(b'3')
                    else: return "Donanım bağlantısı yok."
                elif kategori == "led_2_kapat":
                    if arduino: arduino.write(b'4')
                    else: return "Donanım bağlantısı yok."
                elif kategori == "led_3_ac":
                    if arduino: arduino.write(b'5')
                    else: return "Donanım bağlantısı yok."
                elif kategori == "led_3_kapat":
                    if arduino: arduino.write(b'6')
                    else: return "Donanım bağlantısı yok."

                
                cevap = random.choice(veri["cevap"]) if isinstance(veri["cevap"], list) else veri["cevap"]
                return cevap

    return ""

def asistan_calistir():
    if os.path.exists('komutlar.json'):
        with open('komutlar.json', 'r', encoding='utf-8') as f:
            komutlar = json.load(f)
    else:
        komutlar = {}

    konus("Sistemler çevrimdışı modda aktif. Systems are online and offline mode activated.")

    while True:
        try:
            komut = dinle()
            
            if not komut: 
                continue 
            
            
            if any(x in komut for x in ["kapat", "görüşürüz", "shut down", "goodbye", "exit"]):
                konus("Görüşürüz, sistemleri kapatıyorum. Shutting down.")
                break
            
            yanit = cevapla(komut, komutlar)
            if yanit: 
                konus(yanit)
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    asistan_calistir()