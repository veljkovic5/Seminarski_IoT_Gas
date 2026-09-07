import requests
import random
import time

# Adresa tvog Flask API-ja
URL = 'http://127.0.0.1:5000/api/readings'

print("Simulator Arduina je pokrenut...")
print("Šaljem simulirane podatke senzora na Flask server (Pritisni Ctrl+C za prekid)...\n")

try:
    while True:
        # Nasumično generisanje vrednosti senzora:
        # 80% šanse da bude normalna vrednost (100-350)
        # 20% šanse da pređe granicu za ALARM (401-700)
        if random.random() < 0.8:
            gas_value = random.randint(100, 350)
        else:
            gas_value = random.randint(401, 700)

        # Slanje podataka na Flask server preko HTTP POST zahteva
        payload = {'value': gas_value}
        
        try:
            response = requests.post(URL, json=payload)
            if response.status_code == 201:
                status = "ALARM!" if gas_value > 400 else "Normalno"
                print(f"[POSLATO] Vrednost gasa: {gas_value} ppm | Status: {status}")
            else:
                print(f"[GREŠKA] Server je vratio status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("[GREŠKA] Ne mogu se povezati na Flask server. Proveri da li pokrenuta 'python app.py'.")

        # Pauza od 2 sekunde između slanja merenja
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulacija je zaustavljena.")