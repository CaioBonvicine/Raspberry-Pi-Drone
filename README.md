# Project: Autonomous Drone S500 with Raspberry Pi + Pixhawk (PX4)

## 📘 Description
This project aims to control an **S500 drone** autonomously using a **Raspberry Pi** and a **Pixhawk** flight controller running **PX4 firmware**.  
The Raspberry Pi executes **Python** scripts with **MAVSDK** to send flight commands to the Pixhawk through the **MAVLink** protocol.

---

## 🧠 System Architecture
- **Pixhawk:** Main flight controller running PX4 (configured via QGroundControl)
- **Raspberry Pi:** Onboard computer responsible for autonomous logic
- **Communication:** MAVLink via USB or UART serial connection
- **QGroundControl:** Software used for PX4 setup, configuration, and monitoring

---

## 🧩 Dependencies

### Operating System
- Official Raspberry Pi OS (latest version recommended)

### Basic Packages and Tools
Run the following commands on your Raspberry Pi:

### Install MAVSDK (Python)
python3 -m pip install --upgrade pip
python3 -m pip install mavsdk

## 🔌 Connecting the Raspberry Pi to the Pixhawk

1. Connect the Pixhawk to the Raspberry Pi using a USB cable or a UART (serial) interface.  
   - USB usually appears as `/dev/ttyACM0`
   - UART usually appears as `/dev/ttyAMA0` or `/dev/serial0`

2. Check which port the Pixhawk is connected to:
ls /dev/tty*

## 🧭 How to Run on Raspberry Pi

1. Clone this repository:
git clone https://github.com/CaioBonvicine/Raspberry-Pi-Drone.git
cd Raspberry-Pi-Drone

2. Run the script:
python3 "Name of the code you want to run".py

## ⚙️ Common Issues

**Drone not connecting:**  
Ensure the correct serial port (`/dev/ttyACM0`) is being used. Try adjusting the baud rate (e.g., `:921600` or `:115200`).

**Permission denied:**  
Run `sudo usermod -a -G dialout $USER` and reboot.

**Drone fails to arm:**  
Check QGroundControl for safety warnings and confirm that GPS and sensors are properly calibrated.

---