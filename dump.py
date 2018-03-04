#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522
import signal

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mifare_reader = mfrc522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status, TagType) = mifare_reader.mfrc522_request(mifare_reader.PICC_REQIDL)

    # If a card is found
    if status == mifare_reader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status, uid) = mifare_reader.mfrc522_anticoll()

    # If we have the UID, continue
    if status == mifare_reader.MI_OK:

        # Print UID
        print("Card read UID: %s" % ','.join([a for a in uid[:3]]))
    
        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        
        # Select the scanned tag
        mifare_reader.mfrc522_select_tag(uid)

        # Dump the data
        mifare_reader.mfrc522_dump_classic1k(key, uid)

        # Stop
        mifare_reader.mfrc522_stop_crypto1()
