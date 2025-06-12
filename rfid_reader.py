import serial
import serial.tools.list_ports
import requests
import time

SERIAL_PORT = 'COM3'  
BAUD_RATE = 9600
FLASK_URL = 'http://127.0.0.1:5000/scan'

USER_MAP = {
    '0009334653': 'Arun',
    '0005823896': 'Thilak',
    '0005823409': 'Hari',
}

def list_available_ports():
    """List all available serial ports"""
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port in ports:
        available_ports.append(port.device)
    return available_ports

def send_scan(unique_id, action):
    name = USER_MAP.get(unique_id, 'Unknown')
    data = {'name': name, 'unique_id': unique_id, 'action': action}
    response = requests.post(FLASK_URL, json=data)
    print(response.json())

def main():
    # List available ports first
    available_ports = list_available_ports()
    print("Available serial ports:")
    for port in available_ports:
        print(f"  {port}")
    
    if not available_ports:
        print("No serial ports found. Please connect your RFID reader.")
        return
    
    # Try to connect to the specified port
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Successfully connected to {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"Failed to connect to {SERIAL_PORT}: {e}")
        print("Please check your RFID reader connection and update SERIAL_PORT in the code.")
        return
    
    print(f"Listening on {SERIAL_PORT}...")
    try:
        while True:
            if ser.in_waiting:
                rfid_data = ser.readline().decode('utf-8').strip()
                if rfid_data:  # Only process non-empty data
                    print(f"Scanned RFID: {rfid_data}")
                    # Ask user for action
                    action = input("Entry or Exit? (entry/exit): ").strip().lower()
                    if action in ['entry', 'exit']:
                        send_scan(rfid_data, action)
                    else:
                        print("Invalid action. Try again.")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == '__main__':
    main()
