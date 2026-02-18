# IoT Pulse Oximeter with Cloud Visualization

This project is a Python-based monitoring system that reads SpO2 data from an Arduino-connected MAX30102 sensor and visualizes it both locally and in the cloud.

## Features
* **Real-time Data Processing**: Automatically filters raw sensor input to extract clean SpO2 percentages.
* **Local Logging**: Saves every reading with a timestamp to `sensor_data.csv`.
* **Cloud Graphing**: Integrates with **ThingSpeak** to provide a live web-based dashboard for remote monitoring.

## Hardware Components
* **Arduino Uno** (Connected to COM4)
* **MAX30102** Pulse Oximeter Sensor

## Installation & Setup
1. **Libraries**: Install the required Python libraries:
   ```bash
   pip install pyserial requests
