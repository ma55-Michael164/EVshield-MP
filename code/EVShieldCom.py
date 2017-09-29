from EVShieldDefines import *
import pyb
import struct


class EVShieldI2C():
    def __init__(self, i2c_address):
        #pyb.I2C(1, I2C.MASTER, baudrate=20000).deinit()
        self.i2c = pyb.I2C(1)
        self.i2c.init(pyb.I2C.MASTER, baudrate=20000)
        self.i2c_address = i2c_address >> 1
        self.timeout = 1000
    
    def readRegisters(self, register, length, timeout = None):
        return self.i2c.mem_read(length, self.i2c_address, register, timeout = timeout or self.timeout)
    
    def readByte(self, register, timeout = None):
        return self.i2c.mem_read(1, self.i2c_address, register, timeout = timeout or self.timeout)[0]
    
    def readInteger(self, register, timeout = None):
        return struct.unpack('h', self.i2c.mem_read(2, self.i2c_address, register, timeout = timeout or self.timeout))[0]
    
    def readLong(self, register, timeout = None):
        return struct.unpack('l', self.i2c.mem_read(4, self.i2c_address, register, timeout = timeout or self.timeout))[0]
    
    def readString(self, register, length, timeout = None):
        return self.i2c.mem_read(length, self.i2c_address, register, timeout = timeout or self.timeout).decode("utf-8")
    
    def writeRegisters(self, register, data, timeout = None):
        self.i2c.mem_write(data, self.i2c_address, register, timeout = timeout or self.timeout)
    
    def writeByte(self, register, dataByte, timeout = None):
        self.i2c.mem_write(bytes([dataByte]), self.i2c_address, register, timeout = timeout or self.timeout)
    
    def writeInteger(self, register, dataInt, timeout = None):
        self.i2c.mem_write(struct.pack('H', dataInt), self.i2c_address, register, timeout = timeout or self.timeout)
    
    def writeLong(self, register, dataLong, timeout = None):
        self.i2c.mem_write(struct.pack('I', dataLong), self.i2c_address, register, timeout = timeout or self.timeout)
    
    def checkAddress(self):
        return self.i2c_address in self.i2c.scan()
    
    def setAddress(self, i2c_address):
        self.i2c_address = i2c_address
    
    def getAddress(self):
        return self.i2c_address
    
    def setTimeout(self, timeout):
        self.timeout = timeout
    
    def getTimeout(self):
        return self.timeout
    
    def getFirmwareVersion(self):
        return self.readString(SH_FIRMWARE_VERSION, 8)
    
    def getVendorID(self):
        return self.readString(SH_VENDOR_ID, 8)
    
    def getDeviceID(self):
        return self.readString(SH_DEVICE_ID, 8)
    
    def getFeatureSet(self):
        return self.readString(SH_FEATURE_SET, 8)
    
    def getInfo(self):
        return self.readString(SH_FIRMWARE_VERSION, 32)

    def issueCommand(self, command):
        self.writeByte(SH_COMMAND, command)


class EVShieldUART():
    def __init__(self, shield, bp, type=SH_Type_EV3):
        if bp not in [SH_BAS1, SH_BAS2, SH_BBS1, SH_BBS2]:
            raise ValueError("Invalid bank port!")
        self.bank = shield.bank_a if bp in [SH_BAS1, SH_BAS2] else shield.bank_b
        self.offset = 0 if bp in [SH_BAS1, SH_BBS1] else 52
        self.setType(type)

    def getMode(self):
        return self.readLocationByte(0x81)

    def setMode(self, newMode):
        self.writeLocation(0x81, newMode)

    def setType(self, type):
        self.bank.writeInteger(SH_S1_MODE if self.offset == 0 else SH_S2_MODE, type)

    def readValue(self):
        return self.readLocationInt(0x83)

    def isDeviceReady(self):
        return self.readLocationByte(0x70) == 1

    def writeLocation(self, loc, data):
        self.bank.writeByte(loc + self.offset, data)

    def readLocationInt(self, loc):
        return self.bank.readInteger(loc + self.offset)

    def readLocationByte(self, loc):
        return self.bank.readByte(loc + self.offset)

    def readAndPrint(self, loc, len):
        result = ""
        for i in range(loc, loc+len):
            result += self.readLocationByte(i)
        print(result)


class EVShieldAnalog():
    def __init__(self, shield, bp, type=SH_Type_ANALOG):
        if bp not in [SH_BAS1, SH_BAS2, SH_BBS1, SH_BBS2]:
            raise ValueError("Invalid bank port!")
        self.bank = shield.bank_a if bp in [SH_BAS1, SH_BAS2] else shield.bank_b
        self.which = 1 if bp in [SH_BAS1, SH_BBS1] else 2
        if type: self.setType(type)
    def setType(self, type):
        self.bank.writeInteger(SH_S1_MODE if self.which==1 else SH_S2_MODE, type)
    def readRaw(self):
        return self.bank.readInteger(SH_S1_ANALOG if self.which==1 else SH_S2_ANALOG)
