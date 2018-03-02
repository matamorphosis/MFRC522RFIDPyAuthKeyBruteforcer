#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import spi

  
class MFRC522:
    NRSTPD = 22

    MAX_LEN = 16

    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03

    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SElECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ = 0x30
    PICC_WRITE = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE = 0xC2
    PICC_TRANSFER = 0xB0
    PICC_HALT = 0x50

    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2

    Reserved00 = 0x00
    CommandReg = 0x01
    CommIEnReg = 0x02
    DivlEnReg = 0x03
    CommIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E
    Reserved01 = 0x0F

    Reserved10 = 0x10
    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxAutoReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19
    Reserved11 = 0x1A
    Reserved12 = 0x1B
    MifareReg = 0x1C
    Reserved13 = 0x1D
    Reserved14 = 0x1E
    SerialSpeedReg = 0x1F

    Reserved20 = 0x20
    CRCResultRegM = 0x21
    CRCResultRegL = 0x22
    Reserved21 = 0x23
    ModWidthReg = 0x24
    Reserved22 = 0x25
    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    TCounterValueRegH = 0x2E
    TCounterValueRegL = 0x2F

    Reserved30 = 0x30
    TestSel1Reg = 0x31
    TestSel2Reg = 0x32
    TestPinEnReg = 0x33
    TestPinValueReg = 0x34
    TestBusReg = 0x35
    AutoTestReg = 0x36
    VersionReg = 0x37
    AnalogTestReg = 0x38
    TestDAC1Reg = 0x39
    TestDAC2Reg = 0x3A
    TestADCReg = 0x3B
    Reserved31 = 0x3C
    Reserved32 = 0x3D
    Reserved33 = 0x3E
    Reserved34 = 0x3F

    serNum = []

    def __init__(self, dev='/dev/spidev0.0', spd=1000000):
        spi.openSPI(device=dev, speed=spd)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(self.NRSTPD, 1)
        self.mfrc522_init()

    def mfrc522_reset(self):
        self.write_mfrc522(self.CommandReg, self.PCD_RESETPHASE)

    @staticmethod
    def write_mfrc522(addr, val):
        spi.transfer(((addr << 1) & 0x7E, val))

    @staticmethod
    def read_mfrc522(addr):
        val = spi.transfer((((addr << 1) & 0x7E) | 0x80, 0))
        return val[1]

    def set_bit_mask(self, reg, mask):
        tmp = self.read_mfrc522(reg)
        self.write_mfrc522(reg, tmp | mask)

    def clear_bit_mask(self, reg, mask):
        tmp = self.read_mfrc522(reg)
        self.write_mfrc522(reg, tmp & (~mask))

    def antenna_on(self):
        temp = self.read_mfrc522(self.TxControlReg)
        if ~(temp & 0x03):
            self.set_bit_mask(self.TxControlReg, 0x03)

    def antenna_off(self):
        self.clear_bit_mask(self.TxControlReg, 0x03)

    def mfrc522_to_card(self, command, send_data):
        back_data = []
        back_len = 0
        status = self.MI_ERR
        irq_end = 0x00
        wait_irq = 0x00
        i = 0

        if command == self.PCD_AUTHENT:
            irq_end = 0x12
            wait_irq = 0x10
        if command == self.PCD_TRANSCEIVE:
            irq_end = 0x77
            wait_irq = 0x30

        self.write_mfrc522(self.CommIEnReg, irq_end | 0x80)
        self.clear_bit_mask(self.CommIrqReg, 0x80)
        self.set_bit_mask(self.FIFOLevelReg, 0x80)

        self.write_mfrc522(self.CommandReg, self.PCD_IDLE)

        while i < len(send_data):
            self.write_mfrc522(self.FIFODataReg, send_data[i])
            i = i+1

        self.write_mfrc522(self.CommandReg, command)

        if command == self.PCD_TRANSCEIVE:
            self.set_bit_mask(self.BitFramingReg, 0x80)

        i = 2000
        while True:
            n = self.read_mfrc522(self.CommIrqReg)
            i = i - 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break

        self.clear_bit_mask(self.BitFramingReg, 0x80)

        if i != 0:
            if (self.read_mfrc522(self.ErrorReg) & 0x1B) == 0x00:
                status = self.MI_OK

                if n & irq_end & 0x01:
                    status = self.MI_NOTAGERR

                if command == self.PCD_TRANSCEIVE:
                    n = self.read_mfrc522(self.FIFOLevelReg)
                    last_bits = self.read_mfrc522(self.ControlReg) & 0x07
                    if last_bits != 0:
                        back_len = (n-1)*8 + last_bits
                    else:
                        back_len = n*8

                    if n == 0:
                        n = 1
                    if n > self.MAX_LEN:
                        n = self.MAX_LEN

                    i = 0
                    while i < n:
                        back_data.append(self.read_mfrc522(self.FIFODataReg))
                        i = i + 1
            else:
                status = self.MI_ERR

        return status, back_data, back_len

    def mfrc522_request(self, req_mode):
        tag_type = []

        self.write_mfrc522(self.BitFramingReg, 0x07)

        tag_type.append(req_mode)
        (status, backData, back_bits) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, tag_type)

        if (status != self.MI_OK) | (back_bits != 0x10):
            status = self.MI_ERR

        return status, back_bits

    def mfrc522_anticoll(self):
        ser_num_check = 0

        ser_num = []

        self.write_mfrc522(self.BitFramingReg, 0x00)

        ser_num.append(self.PICC_ANTICOLL)
        ser_num.append(0x20)

        (status, back_data, back_bits) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, ser_num)

        if status == self.MI_OK:
            i = 0
            if len(back_data) == 5:
                while i < 4:
                    ser_num_check = ser_num_check ^ back_data[i]
                    i = i + 1
                if ser_num_check != back_data[i]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR

        return status, back_data

    def calulate_crc(self, p_indata):
        self.clear_bit_mask(self.DivIrqReg, 0x04)
        self.set_bit_mask(self.FIFOLevelReg, 0x80)
        i = 0
        while i < len(p_indata):
            self.write_mfrc522(self.FIFODataReg, p_indata[i])
            i = i + 1
        self.write_mfrc522(self.CommandReg, self.PCD_CALCCRC)
        i = 0xFF
        while True:
            n = self.read_mfrc522(self.DivIrqReg)
            i = i - 1
            if not ((i != 0) and not (n & 0x04)):
                break
        p_out_data = list()
        p_out_data.append(self.read_mfrc522(self.CRCResultRegL))
        p_out_data.append(self.read_mfrc522(self.CRCResultRegM))
        return p_out_data

    def mfrc522_select_tag(self, ser_num):
        buf = list()
        buf.append(self.PICC_SElECTTAG)
        buf.append(0x70)
        i = 0
        while i < 5:
            buf.append(ser_num[i])
            i = i + 1
        p_out = self.calulate_crc(buf)
        buf.append(p_out[0])
        buf.append(p_out[1])
        (status, back_data, back_len) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, buf)

        if (status == self.MI_OK) and (back_len == 0x18):
            print("Size: " + str(back_data[0]))
            return back_data[0]
        else:
            return 0

    def mfrc522_auth(self, auth_mode, block_addr, sector_key, ser_num):
        buff = list()

        # First byte should be the authMode (A or B)
        buff.append(auth_mode)

        # Second byte is the trailerBlock (usually 7)
        buff.append(block_addr)

        # Now we need to append the authKey which usually is 6 bytes of 0xFF
        i = 0
        while i < len(sector_key):
            buff.append(sector_key[i])
            i = i + 1
        i = 0

        # Next we append the first 4 bytes of the UID
        while i < 4:
            buff.append(ser_num[i])
            i = i + 1

        # Now we start the authentication itself
        (status, backData, backLen) = self.mfrc522_to_card(self.PCD_AUTHENT, buff)

        # Check if an error occurred
        if not(status == self.MI_OK):
            print("AUTH ERROR!!")
        if not (self.read_mfrc522(self.Status2Reg) & 0x08) != 0:
            print("AUTH ERROR(status2reg & 0x08) != 0")

        # Return the status
        return status

    def mfrc522_stop_crypto1(self):
        self.clear_bit_mask(self.Status2Reg, 0x08)

    def mfrc522_read(self, block_addr):
        recv_data = list()
        recv_data.append(self.PICC_READ)
        recv_data.append(block_addr)
        p_out = self.calulate_crc(recv_data)
        recv_data.append(p_out[0])
        recv_data.append(p_out[1])
        (status, back_data, back_len) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, recv_data)
        if not(status == self.MI_OK):
            print("Error while reading!")
        if len(back_data) == 16:
            print("Sector "+str(block_addr)+" "+str(back_data))

    def mfrc522_write(self, block_addr, write_data):
        buff = list()
        buff.append(self.PICC_WRITE)
        buff.append(block_addr)
        crc = self.calulate_crc(buff)
        buff.append(crc[0])
        buff.append(crc[1])
        (status, back_data, back_len) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, buff)
        if not(status == self.MI_OK) or not(back_len == 4) or not((back_data[0] & 0x0F) == 0x0A):
            status = self.MI_ERR

        print(str(back_len)+" backdata &0x0F == 0x0A "+str(back_data[0] & 0x0F))
        if status == self.MI_OK:
            i = 0
            buf = []
            while i < 16:
                buf.append(write_data[i])
                i = i + 1
            crc = self.calulate_crc(buf)
            buf.append(crc[0])
            buf.append(crc[1])
            (status, back_data, back_len) = self.mfrc522_to_card(self.PCD_TRANSCEIVE, buf)
            if (
                not(status == self.MI_OK) or not(back_len == 4) or
                not((back_data[0] & 0x0F) == 0x0A)
            ):
                print("Error while writing")
            if status == self.MI_OK:
                print("Data written")

    def mfrc522_dump_classic1k(self, key, uid):
        i = 0
        while i < 64:
            status = self.mfrc522_auth(self.PICC_AUTHENT1A, i, key, uid)
            # Check if authenticated
            if status == self.MI_OK:
                self.mfrc522_read(i)
            else:
                print("Authentication error")
            i = i+1

    def mfrc522_init(self):
        GPIO.output(self.NRSTPD, 1)

        self.mfrc522_reset()

        self.write_mfrc522(self.TModeReg, 0x8D)
        self.write_mfrc522(self.TPrescalerReg, 0x3E)
        self.write_mfrc522(self.TReloadRegL, 30)
        self.write_mfrc522(self.TReloadRegH, 0)

        self.write_mfrc522(self.TxAutoReg, 0x40)
        self.write_mfrc522(self.ModeReg, 0x3D)
        self.antenna_on()
