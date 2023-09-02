from igen import adresKodKontrol
import time
import sys
from datetime import datetime

dosya_yolu = "kodlar.txt"

def tarihzaman():
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime_string

def dosyayaYaz(yazi):
    with open(yazilacak_dosya, "a") as file:
        file.write(yazi)

if len(sys.argv) > 1:
    tekurlmi = True
    url = sys.argv[1]
else:
    tekurlmi = False

if len(sys.argv) > 2:
    dosyaya_yaz = True
    yazilacak_dosya = sys.argv[2]
    if yazilacak_dosya == dosya_yolu:
        print("dikkat et lan")
        quit()

    dosyayaYaz(f"{tarihzaman()} {url}\n")
else:
    dosyaya_yaz = False

with open(dosya_yolu, "r") as file:
    for index, line in enumerate(file):
        # Split the line into a list of space-separated values
        values = line.split()
        # Check if the line has at least five values
        if len(values) >= 5:
            kod = values[2]  # Third ID (index 2)
            adres = values[4]  # Fifth ID (index 4)
            
            if tekurlmi:
                if not adres == url:
                    continue

            print(f"[{index}]{kod} - {adres} test...     ", end="")
            if adresKodKontrol(adres, kod):
                print(f"kod çalışıyor")
                if dosyaya_yaz:
                    dosyayaYaz(f"{kod} ")
            else:
                print(f"kod bozuk")
            time.sleep(1)

