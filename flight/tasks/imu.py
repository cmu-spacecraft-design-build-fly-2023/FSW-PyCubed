# from hal.pycubed import hardware
import time

from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH
from hal.configuration import SATELLITE


class Task(TemplateTask):

    name = "IMU"
    ID = 0x03

    data_keys = [
        "time",
        "accel_x",
        "accel_y",
        "accel_z",
        "mag_x",
        "mag_y",
        "mag_z",
        "gyro_x",
        "gyro_y",
        "gyro_z",
    ]

    # Temporary fake time
    curr_time = time.monotonic_ns()

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if not DH.data_process_exists("imu"):
                DH.register_data_process("imu", self.data_keys, "ffffffffff", True, line_limit=40)

            # print(f"[{self.ID}][{self.name}] Reading BMX160.")

            # SATELLITE.IMU.enable()

            readings = {
                "accel": SATELLITE.IMU.accel(),
                "mag": SATELLITE.IMU.mag(),
                "gyro": SATELLITE.IMU.gyro(),
            }

            # SATELLITE.IMU.disable()

            log_data = {
                "time": time.time(),
                "accel_x": readings["accel"][0],
                "accel_y": readings["accel"][1],
                "accel_z": readings["accel"][2],
                "mag_x": readings["mag"][0],
                "mag_y": readings["mag"][1],
                "mag_z": readings["mag"][2],
                "gyro_x": readings["gyro"][0],
                "gyro_y": readings["gyro"][1],
                "gyro_z": readings["gyro"][2],
            }

            DH.log_data("imu", log_data)

            print(f"[{self.ID}][{self.name}] Data: {readings}")
