import time
import datetime
import csv
import requests
import serial

# --- CONFIGURATION ---
THINGSPEAK_API_KEY = "Insert API KEY" # <--- Paste your Write API Key here
THINGSPEAK_URL = "https://api.thingspeak.com/update"
CSV_FILENAME = "sensor_data.csv"

# --- ARDUINO SETUP ---
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
    print("Connected to Arduino on COM4")
    time.sleep(2) 
except Exception as e:
    print(f"Error: Could not connect to COM4. {e}")
    exit()

# --- SETUP CSV FILE ---
try:
    with open(CSV_FILENAME, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "SpO2"])
except FileExistsError:
    pass

print("System Started... Place your finger on the sensor.")

# --- MAIN LOOP ---
while True:
    try:
        current_spo2 = 0
        
        if ser.in_waiting > 0:
            # --- PASTE FIX #1 HERE ---
            ser.reset_input_buffer() 
            # -------------------------
            
            # # 1. Read the line (e.g., "127209, 98")
            raw_data = ser.readline().decode('utf-8').strip()
            
            # 2. Split by comma to get the SpO2 value
            parts = raw_data.split(',')
            if len(parts) >= 2:
                try:
                    # Taking the second part (the 98)
                    current_spo2 = int(parts[1].strip())
                except ValueError:
                    current_spo2 = 0
            
        # Only upload if a real reading is found
        if current_spo2 > 0:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to CSV
            with open(CSV_FILENAME, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([now, current_spo2])
                
            # Send to ThingSpeak
            payload = {'api_key': THINGSPEAK_API_KEY, 'field1': current_spo2}
            try:
                r = requests.get(THINGSPEAK_URL, params=payload)
                status = "Uploaded" if r.status_code == 200 else "Failed"
            except:
                status = "Offline"

            print(f"Saved: {now} | SpO2: {current_spo2}% | {status}")
            
            # Wait 16 seconds for ThingSpeak Free Tier
            time.sleep(0.1)
        else:
            # Keep checking quickly if no finger is detected
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping... Data is safe in 'sensor_data.csv'")
        break