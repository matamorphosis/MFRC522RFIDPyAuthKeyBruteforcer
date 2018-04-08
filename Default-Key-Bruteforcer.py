#!/bin/python

import RPi.GPIO as GPIO
import MFRC522
import signal
import ast
import sys

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("[i] RFID Key Bruteforcer.")
print ("[i] Written by Matthew Brittain, Built on https://github.com/mxgxw/MFRC522-python.")
print ("[i] Press Ctrl-C to stop the program.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("[+] Card detected")
    
    	# Get the UID of the card
    	(status,uid) = MIFAREReader.MFRC522_Anticoll()

    	# If we have the UID, continue
    	if status == MIFAREReader.MI_OK:

        	# Print UID
        	print ("[+] Card read UID: " + ",".join(uid))
    
        	# This is the default key for authentication
        	# key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            try:
                # Import UIDs from text file
        	    lines = [line.rstrip('\n') for line in open('keys.txt')]
            except:
                sys.exit("[-] Failed to open file.")
                
            for l in lines:
                # Strip the imported UID of commas
                keya = [ byte.strip() for byte in l.split(',') ]
            	    key = [int(byte,16) for byte in keya]
            	    print ("[i] Trying the key: " + key)

            	    # Select the scanned tag
            	    MIFAREReader.MFRC522_SelectTag(uid)

            	    # Authenticate
            	    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            	    # Check if authenticated
            	    if status == MIFAREReader.MI_OK:
                    	MIFAREReader.MFRC522_Read(8)
                    	MIFAREReader.MFRC522_StopCrypto1()
                    	print ("[+] The correct key is " + key)
                
                    else:
               	    	print ("[-] Authentication error")
