from machine import I2C
import utime

class PAJ7620():
    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr #设置需要通信的从机地址
        self.i2c.write(self.addr, b'\xEF')  # 唤醒命令
        utime.sleep(0.01)
        initial_value = self.i2c.readfrom_mem(self.addr, 0x00, 1)

        if initial_value == [32]:
            print("wake-up successful!")
            i2c.write(addr, b'\xEF\x01')  #进入BANK1
            i2c.write(addr, b'\x72\x01')  #使能工作
        else:
            print("wake-up failed!")

    def set_gesture(self, reg, data):
        self.i2c.write(self.addr, b'\xEF\x00')  #进入BANK0

        if reg == 1:
            self.i2c.write(self.addr, bytes([0x41, data]))
        elif reg == 2:
            self.i2c.write(self.addr, bytes([0x42, data]))


        print(self.i2c.readfrom_mem(self.addr, 0x41, 1))   #获取当前哪些手势可以被识别
        print(self.i2c.readfrom_mem(self.addr, 0x42, 1)) 

    def get_gesture(self,reg):
        self.i2c.write(self.addr, b'\xEF\x00')  #进入BANK0
        if reg == 1:
            ges1 = self.i2c.readfrom_mem(self.addr, 0x43, 1)
            return ges1
        if reg == 2:
            ges2 = self.i2c.readfrom_mem(self.addr, 0x44, 1)
            return ges2
