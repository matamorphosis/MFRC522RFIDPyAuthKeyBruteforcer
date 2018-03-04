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

# Welcome message
print("RFID Key Bruteforcer")
print("Written by Matthew Brittain, Built on https://github.com/mxgxw/MFRC522-python")
print("Press Ctrl-C to stop.")

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
            # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            # print (key)

            lines = [line.rstrip('\n') for line in open('keys.txt')]

            for l in lines:
                key = [int(byte.strip(), 16) for byte in l.split(',')]
                print("Trying the following key:")
                print(key)

                # Select the scanned tag
                mifare_reader.mfrc522_select_tag(uid)

                # Authenticate
                status = mifare_reader.mfrc522_auth(mifare_reader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == mifare_reader.MI_OK:
                    mifare_reader.mfrc522_read(8)
                    mifare_reader.mfrc522_stop_crypto1()
                    print("The correct key is " + key)

                else:
                    print("Authentication error")
