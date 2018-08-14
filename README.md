# MFRC522PythonAuthKeyBruteforcer
Just a simple RFID authentication key brute-force program written in python, as all the ones I found were written in C. This is much more user friendly

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
- Install with the following command:
- root@linux:/Downloads/SPI-Py# python setup.py install

As can be seen in the latest commit of the main program, a pure brute-force option is now available which runs through all 274,941,996,890,625, calculated by (255^6), possibililities. This option is not recommended for just one device such as a raspberry pi, as it will take years to crack. However, a more powerful computer may be able to run through these options much quicker.
