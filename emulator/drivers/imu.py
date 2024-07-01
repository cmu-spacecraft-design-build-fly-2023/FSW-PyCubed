class IMU:
    def __init__(self, accel, mag, gyro, temp) -> None:
        self.__accel = accel
        self.__mag = mag
        self.__gyro = gyro
        self.__temp = temp
        self.__enable = False

    def accel(self):
        return self.__accel if self.__enable else None

    def mag(self):
        return self.__mag if self.__enable else None

    def gyro(self):
        return self.__gyro if self.__enable else None

    def temp(self):
        return self.__temp if self.__enable else None

    def enable(self):
        self.__enable = True

    def disable(self):
        self.__enable = False
