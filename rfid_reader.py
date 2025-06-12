import serial
import requests
import time

SERIAL_PORT = 'COM4'  
BAUD_RATE = 9600
FLASK_URL = 'http://127.0.0.1:5000/scan'

USER_MAP = {
    '0009334653': 'Arun',
    '0005823896': 'Thilak',
    '0005823409': 'Hari',
}

def send_scan(unique_id, action):
    name = USER_MAP.get(unique_id, 'Unknown')
    data = {'name': name, 'unique_id': unique_id, 'action': action}
    response = requests.post(FLASK_URL, json=data)
    print(response.json())

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT}...")
    while True:
        if ser.in_waiting:
            rfid_data = ser.readline().decode('utf-8').strip()
            print(f"Scanned RFID: {rfid_data}")
            # Ask user for action
            action = input("Entry or Exit? (entry/exit): ").strip().lower()
            if action in ['entry', 'exit']:
                send_scan(rfid_data, action)
            else:
                print("Invalid action. Try again.")
        time.sleep(0.5)

if __name__ == '__main__':
    main()
