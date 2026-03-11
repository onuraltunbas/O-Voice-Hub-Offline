# Copyright (c) 2026 Remzican Onur Altunbaş
# Non-Commercial License
# Commercial use prohibited without permission

import json
import os
import random
import serial
import time
import speech_recognition as sr
import warnings
from ctypes import *

# --- XTTS v2 (COQUI) KÜTÜPHANELERİ ---
import sounddevice as sd
import numpy as np
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

# --- PYTORCH 2.6+ UYUMLULUK YAMASI ---
_original_load = torch.load
def patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = patched_load
# -------------------------------------

# --- ALSA (LINUX SES) UYARILARINI GİZLEME ---
try:
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    pass

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- YAPAY ZEKA SES MOTORUNU (XTTS v2) BAŞLAT ---
os.environ["COQUI_TOS_AGREED"] = "1"
print("Initializing local AI Voice (XTTS v2)...")

config = XttsConfig()
config.load_json("xtts_v2_local/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="xtts_v2_local", eval=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"Voice model activated on {device.upper()}!")

print("Analyzing voice clone (benim_sesim.wav)...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["jarvis.wav"])
print("Voice systems fully operational!")


# --- ARDUINO BAĞLANTISI ---
try:
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2) 
    print("Arduino connection successful!")
except Exception as e:
    arduino = None
    print("Arduino not found, hardware controls are disabled.")


def konus(metin):
    print("Assistant:", metin)
    
    out = model.inference(
        text=metin,
        language="en", 
        gpt_cond_latent=gpt_cond_latent,
        speaker_embedding=speaker_embedding,
        temperature=0.7,
    )
    
    audio_data = np.array(out["wav"])
    sd.play(audio_data, samplerate=24000)
    sd.wait() 

def dinle():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Listening to you...")
        r.adjust_for_ambient_noise(source, duration=0.5) 
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5) 
            print("Processing audio...")
            
            metin = r.recognize_whisper(audio, model="base", language="en")
            
            print(f"You said: {metin}")
            return metin.lower().strip()
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Audio recognition error: {e}")
            return ""

def cevapla(komut, komutlar):
    komut = komut.lower()

    for kategori, veri in komutlar.items():
        for anahtar in veri.get("anahtarlar", []):
            if anahtar in komut:
                
                # --- DONANIM KONTROLLERİ ---
                if kategori == "led_1_ac":
                    if arduino: arduino.write(b'1')
                    else: return "No hardware connection."
                elif kategori == "led_1_kapat":
                    if arduino: arduino.write(b'2')
                    else: return "No hardware connection."
                elif kategori == "led_2_ac":
                    if arduino: arduino.write(b'3')
                    else: return "No hardware connection."
                elif kategori == "led_2_kapat":
                    if arduino: arduino.write(b'4')
                    else: return "No hardware connection."
                elif kategori == "led_3_ac":
                    if arduino: arduino.write(b'5')
                    else: return "No hardware connection."
                elif kategori == "led_3_kapat":
                    if arduino: arduino.write(b'6')
                    else: return "No hardware connection."
                elif kategori == "gösteri":
                    if arduino: arduino.write(b'7')
                    else: return "No hardware connection."

                
                cevap = random.choice(veri["cevap"]) if isinstance(veri["cevap"], list) else veri["cevap"]
                return cevap

    return ""

def asistan_calistir():
    if os.path.exists('komutlar.json'):
        with open('komutlar.json', 'r', encoding='utf-8') as f:
            komutlar = json.load(f)
    else:
        komutlar = {}

    konus("welcome home, sir. How can I assist you today?")

    while True:
        try:
            komut = dinle()
            
            if not komut: 
                continue 

            # UYANDIRMA KİLİDİ
            if "hey car" not in komut:
                continue
            
            if any(x in komut for x in ["shut down", "goodbye", "exit"]):
                konus("Goodbye.")
                break
            
            yanit = cevapla(komut, komutlar)
            if yanit: 
                konus(yanit)
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    asistan_calistir()