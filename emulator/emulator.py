from typing import List, Optional

from hal.cubesat import CubeSat
from hal.drivers.burnwire import BurnWires
from hal.drivers.imu import IMU
from hal.drivers.light_sensor import LightSensor
from hal.drivers.payload import Payload
from hal.drivers.power_monitor import PowerMonitor
from hal.drivers.radio import Radio
from hal.drivers.sd import SD
from numpy import array


class device:
    """
    Based on the code from: https://docs.python.org/3/howto/descriptor.html#properties
    Attempts to return the appropriate hardware device.
    If this fails, it will attempt to reinitialize the hardware.
    If this fails again, it will raise an exception.
    """

    def __init__(self, fget=None):
        self.fget = fget
        self._device = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError(f"unreadable attribute {self._name}")

        if self._device is not None:
            return self._device
        else:
            self._device = self.fget(instance)
            return self._device


class satellite(CubeSat):
    def __init__(self, enable_middleware, debug) -> None:
        self.__middleware_enabled = enable_middleware
        self.__debug = debug

        super().__init__()

        self._burnwires = BurnWires()
        self._radio = Radio()
        self._sd_card = SD()
        self._payload_uart = Payload()

        self._vfs = None
        self._gps = None
        self._charger = None

        self._light_sensor_xp = LightSensor(900)
        self._light_sensor_xm = LightSensor(48000)
        self._light_sensor_yp = LightSensor(85000)
        self._light_sensor_ym = LightSensor(200)
        self._light_sensor_zp = LightSensor(12000)

        self._torque_x = None
        self._torque_y = None
        self._torque_z = None

        accel = array([1.0, 2.0, 3.0])
        mag = array([4.0, 3.0, 1.0])
        gyro = array([0.0, 0.0, 0.0])
        self._imu = IMU(accel=accel, mag=mag, gyro=gyro, temp=20)
        self._imu.enable()

        self._jetson_monitor = PowerMonitor(4, 0.05)
        self._battery_monitor = PowerMonitor(4.2, 0.04)

    def boot_sequence(self) -> List[int]:
        pass

    def run_system_diagnostics(self) -> Optional[List[int]]:
        pass
