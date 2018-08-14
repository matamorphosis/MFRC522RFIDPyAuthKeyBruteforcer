#!/usr/bin/env python

import RPi.GPIO as GPIO, mfrc522, signal, sys, time, re, argparse

continue_reading = True
allcombos = []

parser = argparse.ArgumentParser(description='Default Key Bruteforcer is a python brute force program for cracking the authentication key for Mifare RC522 compliant RFID tags.')
parser.add_argument('-t', '--type', help='This option is used to specify the type of bruteforce, currently only pure is supported for the option. Pure bruteforce is 100% effective; however, it takes a while. ./Default-Key-Bruteforcer.py -t pure')
parser.add_argument('-f', '--file', help='This option is used to specify a file containing URLs to search. Unless specified the program looks for the file keys.txt. ./Default-Key-Bruteforcer.py -f file.txt')
args = parser.parse_args()

# Capture SIGINT for cleanup when the script is aborted.
def end_read(signal, frame):
    global continue_reading
    print("[!] INTERRUPT [!] - Ctrl+C captured, stopping program and cleaning up.")
    continue_reading = False
    GPIO.cleanup()

def tempcombo(t1, t2, t3, t4, t5, t6):
	tempcombo.temp = []
	tempcombo.temp.append(i1)
	tempcombo.temp.append(i2)
	tempcombo.temp.append(i3)
	tempcombo.temp.append(i4)
	tempcombo.temp.append(i5)
	tempcombo.temp.append(i6)

def Reader(arrayofattempts, ishex):
        # Welcome message.
        print("[i] RFID Key Brute-forcer.")
        print("[i] Written by Matthew Brittain, built on https://github.com/mxgxw/MFRC522-python.")
        print("[i] Press Ctrl-C to stop the program.")
	# Hook the SIGINT.
	signal.signal(signal.SIGINT, end_read)

	# Create an object of the class MFRC522.
	MIFAREReader = mfrc522.MFRC522()
	# This loop keeps checking for chips. If one is near it will get the UID and authenticate.
	while continue_reading:
		
		for newline in arrayofattempts:
			
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

					if (ishex == 1):
						# Strip the imported UID of commas.
						key = [int(byte.strip(), 16) for byte in newline.split(',')]
					else:
						key = newline

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

if args.file:
	file = args.file
	#try:
        with open(file) as lines:
                newlines = lines.read().splitlines()
                for line in newlines:
                        hexregex = re.search(r"[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}", line)
                        if not hexregex:
                                sys.exit("[-] The contents of the file are not in the correct format.")
                ishex = 1
                Reader(newlines, ishex)
        file.close()
	#except:
		#sys.exit("[-] Failed to open file: " + file + ".")

else:
	file = "keys.txt"

if (args.type == "pure"):
	print("[i] Pure brute force option selected... Generating all 274,941,996,890,625 combinations.")
	i1 = 1
	i2 = 1
	i3 = 1
	i4 = 1
	i5 = 1
	i6 = 1

	while (i1 <= 255):
		tempcombo(i1, i2, i3, i4, i5, i6)
		allcombos.append(tempcombo.temp)
		while (i2 <= 254):
			tempcombo(i1, i2, i3, i4, i5, i6)
			allcombos.append(tempcombo.temp)
			while (i3 <= 254):
				tempcombo(i1, i2, i3, i4, i5, i6)
				allcombos.append(tempcombo.temp)
				while (i4 <= 254):
					tempcombo(i1, i2, i3, i4, i5, i6)
					allcombos.append(tempcombo.temp)
					while (i5 <= 254):
						tempcombo(i1, i2, i3, i4, i5, i6)
						allcombos.append(tempcombo.temp)
						while (i6 <= 254):
							tempcombo(i1, i2, i3, i4, i5, i6)
							allcombos.append(tempcombo.temp)
							i6 = i6 + 1
						i6 = 1
						i5 = i5 + 1
					i5 = 1
					i4 = i4 + 1
				i4 = 1
				i3 = i3 + 1
			i3 = 1
			i2 = i2 + 1
		i2 = 1
		i1 = i1 + 1
	i1 = 1
	
	ishex = 0
	Reader(allcombos, ishex)
