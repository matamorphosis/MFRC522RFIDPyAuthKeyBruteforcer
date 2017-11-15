# MFRC522PythonAuthKeyBruteforcer
Just a simple RFID authentication key brute-force program written in python, as all the ones I found were written in C. This is much more user friendly

Usage:

Add desired keys to keys.txt must be in the following format:
a0,a1,a2,a3,a4,a5

So get rid of 0x, if your key looks like:
0xa0,0xa1,0xa2,0xa3,0xa4,0xa5

Make sure to have an Mifare RC522 RFID Reader setup and running in order to use this software.
This software is built on top of https://github.com/mxgxw/MFRC522-python.
