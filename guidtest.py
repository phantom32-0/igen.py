import requests, time, sys, datetime

session = requests.Session()

def tarihzaman():
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime_string

def guidTest(kod, guid):
    try:
        veri = session.get(url + "Home/IndexQr/?formId=0&code=" + guid, allow_redirects=False)
    except:
        print(f"[{tarihzaman()}] sıkıntı çıktı {guid}")
        return
    
    if veri.status_code == 302:
        print(f"[{tarihzaman()}] basarisiz {kod} {guid}")
        return False
    print(f"[{tarihzaman()}] umut var {kod} {guid}")


