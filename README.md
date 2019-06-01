# MFRC522PythonAuthKeyBruteforcer
Just a simple RFID authentication key brute-force program written in python, as all the ones I found were written in C. This is much more user friendly

Required Hardware:
- Mifare RC522 RFID Reader
- Raspberry Pi, or a controller with GPIO pins ideally running some form of debian linux.

Usage:

Add any keys you wish to test to the keys.txt file. They must be in the following format with 6 hex chars, seperated by commas exclusive of any \x or 0x at the front:
ff,ff,ff,ff,ff,ff

Make sure to have an Mifare RC522 RFID Reader setup and running in order to use this software.
This software is built on top of https://github.com/mxgxw/MFRC522-python.

To connect the reader to a  Raspberry Pi, refer to the following wiring diagram:
https://cdn.pimylifeup.com/wp-content/uploads/2017/10/RFID-Diagram.png

In the Raspberry Pi config, make sure to enable the SPI Interface

Lastly, clone SPI-Py from the following repository:
https://github.com/lthiery/SPI-Py
- It is imperative you rollback to the following to the following repository:
- root@linux:/Downloads/SPI-Py# git checkout 8cce26b9ee6e69eb041e9d5665944b88688fca68
- Then Install with the following command:
- root@linux:/Downloads/SPI-Py# python setup.py install

As can be seen in the latest commit of the main program, a pure brute-force option is now available which runs through all 274,941,996,890,625, calculated by (255^6), possibililities. This option is not recommended for just one device such as a raspberry pi, as it will take extremely long to crack. However, a more powerful computer may be able to run through these options much quicker. There are two options within the pure bruteforce option: ascending and descending.
- Ascending: Increases from 0,0,0,0,0,0 to 255,255,255,255,255,255
- Descending: Decreases from 255,255,255,255,255,255 to 0,0,0,0,0,0

!!KNOWN ISSUE!!
There is a strange known issue, when you first run the program, where the program keeps attempting the very first key, for ascending this is 1,1,1,1,1,1 and descending this is 255,255,255,255,255,255. While this bug is being fixed a workaround is to remove the card from the reader, wait a couple of seconds and it will start to increase with each attempt. This is only a requirement once. The following image shows an example of this. Notice the first 6 attempts have the same key, and afterwards is when I removed the card, and then tapped it on again, and the numbers started to increase.

![Alt text](photos/Asc-Err.png?raw=true "Error")

Lastly, if you want proof everything is working correctly, I recommend using a blank card with the default authentication key, which is 255,255,255,255,255,255. Choose the descending pure brute force option, or use the file option and provide a file with the default key. You should get a response like the following:

![Alt text](photos/Desc-Success.png?raw=true "Success")

Feel free to pull this code, and get in running with other RFID reader libraries, I'd love to turn this into an open-source mass-RFID cracker.
