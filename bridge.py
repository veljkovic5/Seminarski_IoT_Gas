import serial
import requests
import time

SERIAL_PORT = 'COM3'  # Promeni u svoj COM port na kome je Arduino
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Most izmedju Arduina i Flask-a je pokrenut...")

    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if "Vrednost gasa:" in line:
                try:
                    val = int(line.split(":")[1].strip())
                    # Slanje na Flask REST API
                    response = requests.post('http://127.0.0.1:5000/api/readings', json={'value': val})
                    print(f"Očitano sa Arduina: {val} | Server odgovorio: {response.status_code}")
                except ValueError:
                    continue
except serial.SerialException:
    print(f"Greška pri povezivanju na port {SERIAL_PORT}. Proveri da li je Arduino priključen.")
except KeyboardInterrupt:
    print("\nPrekinuto od strane korisnika.")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()