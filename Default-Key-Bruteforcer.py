#!/usr/bin/python

import RPi.GPIO as GPIO, mfrc522, signal, sys, time, re, argparse, threading

continue_reading = True
allcombos = []

parser = argparse.ArgumentParser(description='Default Key Bruteforcer is a python brute force program for cracking the authentication key for Mifare RC522 compliant RFID tags.')
parser.add_argument('-t', '--type', help='This option is used to specify the type of bruteforce, currently only pure is supported for the option. Pure bruteforce is 100% effective; however, it takes a while. ./Default-Key-Bruteforcer.py -t pure')
parser.add_argument('-f', '--file', help='This option is used to specify a file containing URLs to search. Unless specified the program looks for the file keys.txt. ./Default-Key-Bruteforcer.py -f file.txt')
args = parser.parse_args()

# Capture SIGINT for cleanup when the script is aborted.

def welcome():
	# Welcome message.
	print("[i] RFID Key Brute-forcer.")
	print("[i] Written by Matthew Brittain, built on https://github.com/mxgxw/MFRC522-python.")
	print("[i] Press Ctrl-C to stop the program.")
	
def file_open(input_file):
	
	try:
		with open(input_file) as lines:
			newlines = lines.read().splitlines()
			
			for line in newlines:
				hexregex = re.search(r"[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}\,[0-9a-fA-F]{2}", line)
				
				if not hexregex:
					sys.exit("[-] The contents of the file are not in the correct format.")
				
				else:
					Thread = threading.Thread(target=Reader, args=(line, True))
					Thread.start()

	except:
		sys.exit("[-] Failed to open file: " + input_file + ".")

def end_read(signal, frame):
    global continue_reading
    print("[!] INTERRUPT [!] - Ctrl+C captured, stopping program and cleaning up.")
    continue_reading = False
    GPIO.cleanup()

def tempcombo(t1, t2, t3, t4, t5, t6):
	temp_combo = []
	temp_combo.extend([i1, i2, i3, i4, i5, i6])
	return temp_combo

def Reader(attempt, ishex):
	# Hook the SIGINT.
	signal.signal(signal.SIGINT, end_read)
	
	# Create an object of the class MFRC522.
	MIFAREReader = mfrc522.MFRC522()
	
	# This loop keeps checking for chips. If one is near it will get the UID and authenticate.
	
	while continue_reading:
			
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

				if ishex:
					# Strip the imported UID of commas.
					key = [int(byte.strip(), 16) for byte in attempt.split(',')]
				else:
					key = attempt

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
	
	try:
		file = args.file
		welcome()
		file_open(file)
	
	except:
		sys.exit("[-] Failed to load the provided file.")

else:
	
	try:
		file = "keys.txt"
		welcome()
		file_open(file)
	
	except:
		sys.exit("[-] Failed to load keys.txt.")
	
if (args.type == "pure"):
	welcome()
	print("[i] Pure brute force option selected... Generating all 274,941,996,890,625 combinations... Please be patient.")
	i1 = 1
	i2 = 1
	i3 = 1
	i4 = 1
	i5 = 1
	i6 = 1
	
	while (i1 <= 254):
		temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
		Thread_1 = threading.Thread(target=Reader, args=(temp_combo, False))
		Thread_1.start()

		while (i2 <= 254):
			temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
			Thread_2 = threading.Thread(target=Reader, args=(temp_combo, False))
			Thread_2.start()

			while (i3 <= 254):
				temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
				Thread_3 = threading.Thread(target=Reader, args=(temp_combo, False))
				Thread_3.start()

				while (i4 <= 254):
					temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
					Thread_4 = threading.Thread(target=Reader, args=(temp_combo, False))
					Thread_4.start()

					while (i5 <= 254):
						temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
						Thread_5 = threading.Thread(target=Reader, args=(temp_combo, False))
						Thread_5.start()

						while (i6 <= 254):
							temp_combo = tempcombo(i1, i2, i3, i4, i5, i6)
							Thread_6 = threading.Thread(target=Reader, args=(temp_combo, False))
							Thread_6.start()

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
