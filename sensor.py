import os, sys, io
import M5
from M5 import *
from hardware import Pin, I2C
from unit import ENVUnit
import time

# --- Global Variables ---
i2c0 = None
env3_0 = None
temp_val = 0
humi_val = 0

# UI Widgets
label_temp_title = None
label_temp_value = None
label_humi_title = None
label_humi_value = None

def setup():
    global i2c0, env3_0
    global label_temp_title, label_temp_value, label_humi_title, label_humi_value

    # Initialize M5Stack device
    M5.begin()

    # Step 4: Style the Screen
    # Set rotation to 1 for Landscape (Horizontal)
    Widgets.setRotation(1) 
    M5.Display.fillScreen(0x000033) # Dark blue background

    # Step 1: Initialize ENV III (Port A: 32, 33)
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    env3_0 = ENVUnit(i2c=i2c0, type=3)

    # Step 3 & 4: Compact UI Design (Stacked vertically for small screens)
    # Adjusting Y coordinates to fit within ~135px height
    
    # --- Temperature Section ---
    # Title at the very top
    label_temp_title = Widgets.Label("TEMP:", 10, 5, 1.0, 0xBBBBBB, 0x000033, Widgets.FONTS.DejaVu18)
    # Value below the title
    label_temp_value = Widgets.Label("---", 10, 30, 1.0, 0xFFFFFF, 0x000033, Widgets.FONTS.DejaVu24)
    
    # --- Humidity Section ---
    # Title in the middle
    label_humi_title = Widgets.Label("HUMI:", 10, 70, 1.0, 0xBBBBBB, 0x000033, Widgets.FONTS.DejaVu18)
    # Value at the bottom
    label_humi_value = Widgets.Label("---", 10, 95, 1.0, 0x00FF00, 0x000033, Widgets.FONTS.DejaVu24)

def loop():
    global temp_val, humi_val
    M5.update()
    
    try:
        # Step 2: Read data from sensor
        temp_val = env3_0.read_temperature()
        humi_val = env3_0.read_humidity()
        
        # Step 3: Update Screen Labels
        # Using concise format to ensure it fits the small screen
        label_temp_value.setText("{:.1f} C".format(temp_val))
        label_humi_value.setText("{:.1f} %".format(humi_val))
        
        # --- Real-time Plotting to Computer (UIFlow 2.0 Chart) ---
        # Note: Open "Terminal -> Chart" in UIFlow 2.0 on your PC
        print("temp:{:.1f},humi:{:.1f}".format(temp_val, humi_val))
        
    except Exception as e:
        label_temp_value.setText("Error")

    # Step 2: Mandatory 500ms delay for system stability
    time.sleep_ms(500)

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("System Error:", e)