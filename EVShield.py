# main.py -- put your code here!

from pyb import I2C

BANKA = 0x34 >> 1
BANKB = 0x36 >> 1
Device_ADDRESS = 0x34 >> 1

Device_WHO_AM_I = 0x10
Device_VERSION = 0x00
Device_VENDOR = 0x08
Device_FEATURES = 0x18
Servo_Base = 0x42
Led_Base = 0xD7
SA1_base = 0x48
SA2_base = 0x5E
SA3_base = 0x74
SD1_base = 0x8A
SD2_base = 0xA0
KeyPress = 0xDA
LeftKeyCount = 0xDB
GoKeyCount = 0xDC
RightKeyCount = 0xDD

Contntrol_reg = 0x41

I2C(1, I2C.MASTER, baudrate=20000).deinit()
pyb.delay(1000)
i2c = I2C(1, I2C.MASTER, baudrate=20000)

def read_who_am_I(Dev_ADDRESS):
    list = i2c.mem_read(8,Dev_ADDRESS, Device_WHO_AM_I, timeout=1000)
    print(list.decode("utf-8") )

def read_features(Dev_ADDRESS):
    list = i2c.mem_read(8,Dev_ADDRESS, Device_FEATURES, timeout=1000)
    print(list.decode("utf-8"))

def read_vendor(Dev_ADDRESS):
    name =""
    list = i2c.mem_read(8,Dev_ADDRESS, Device_VENDOR, timeout=1000)
    print(list.decode("utf-8"))

def read_version(Dev_ADDRESS):
    list = i2c.mem_read(5,Dev_ADDRESS, Device_VERSION, timeout=1000)
    print(list.decode("utf-8"))

def read_info(Dev_ADDRESS = BANKA):
    list = i2c.mem_read(32,Dev_ADDRESS, Device_VERSION, timeout=1000)
    print(list.decode("utf-8"))

def set_RGB(R,G,B,Dev_ADDRESS= BANKA):
    data = bytearray(3)
    data[0] = R
    data[1] = G
    data[2] = B
    i2c.mem_write(data, Dev_ADDRESS, Led_Base, timeout=1000)

def get_RGB(Dev_ADDRESS= BANKA):
    list = i2c.mem_read(3,Dev_ADDRESS, Led_Base, timeout=1000)
    return list[0],list[1],list[2],

def set_Servo(device,value):
    data = bytearray(2)
    data[1] = int(value/256)
    data[0] = int(value)
    i2c.mem_write(data, Device_ADDRESS, Servo_Base +2*int(device),timeout=1000)

def read_SD1():
    if int(i2c.mem_read(1,Device_ADDRESS, SD1_base+3)[0]) == 0:
        list = i2c.mem_read(14,Device_ADDRESS, SD1_base+4)
        return(list)

def read_Key(reg =GoKeyCount):
    list = i2c.mem_read(1,Device_ADDRESS, reg)
    return(list[0])

def read_analog(port):
    list = i2c.mem_read(6,Device_ADDRESS, SA1_base +port*22)
    if list[0] == 1 : return(list[4] +list[5]*256) 
    else: return 0

def Set_type(port ,type):
    data = bytearray(1)
    data[0] = int(type)
    i2c.mem_write(data, Device_ADDRESS, SA1_base +2+port*22,timeout=1000)

def Set_mode(port ,mode,type =0):
    data = bytearray(2)
    data[0] = int(mode)
    data[1] = int(type)
    i2c.mem_write(data, Device_ADDRESS, SA1_base +port*22,timeout=1000)

def Set_pin(port ,mode):
    data = bytearray(1)
    data[0] = int(mode)
    i2c.mem_write(data, Device_ADDRESS, SA1_base+4 +port*22,timeout=1000)

read_info(BANKA)
read_info(BANKB)
print(get_RGB())
while True:
    print(read_Key(KeyPress),read_Key(GoKeyCount),read_Key(LeftKeyCount),read_Key(RightKeyCount))
    set_RGB(0,100,0,BANKA)
    set_RGB(100,0,0,BANKB)
    pyb.delay(200)
    set_RGB(100,0,0,BANKA)
    set_RGB(0,100,0,BANKB)
    pyb.delay(200)