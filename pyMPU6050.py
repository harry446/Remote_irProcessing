import smbus


class pyMPU6050:
    def __init__(self):
        self.sensorAddress = 0x68
        self.device = smbus.SMBus(1)
        self.accerelations = [0, 0, 0]
        # Initialization of the sensor
        self.device.write_byte_data(self.sensorAddress, 0x6b, 0)

    def read_byte(self, adr):
        return self.device.read_byte_data(self.sensorAddress, adr)

    def read_word(self, adr):
        high = self.device.read_byte_data(self.sensorAddress, adr)
        low = self.device.read_byte_data(self.sensorAddress, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def getAccel(self):
        self.accerelations[0] = self.read_word_2c(0x3b)
        self.accerelations[1] = self.read_word_2c(0x3d)
        self.accerelations[2] = self.read_word_2c(0x3f)
