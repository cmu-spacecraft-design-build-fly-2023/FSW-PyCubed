# Sun Vector Tasks

import time

from apps.sun import compute_body_sun_vector_from_lux, in_eclipse, read_light_sensors
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH


class Task(TemplateTask):

    name = "SUN"
    ID = 0x11

    data_keys = [
        "time",
        "status",
        "x",
        "y",
        "z",
        "eclipse",
        "xp",
        "xm",
        "yp",
        "ym",
        "zp",
    ]

    THRESHOLD_ILLUMINATION_LUX = 3000

    status = False
    sun_vector = [1, 0, 0]
    eclipse_state = False

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if not DH.data_process_exists("sun"):
                DH.register_data_process("sun", self.data_keys, "fbfffbiiiii", True, line_limit=100)

            # Access Sun Sensor Readings - Satellite must return the array directly
            lux_readings = read_light_sensors()

            self.status, self.sun_vector = compute_body_sun_vector_from_lux(lux_readings)
            self.eclipse_state = in_eclipse(
                lux_readings,
                threshold_lux_illumination=self.THRESHOLD_ILLUMINATION_LUX,
            )

            readings = {
                "time": time.time(),
                "status": self.status,
                "x": self.sun_vector[0],
                "y": self.sun_vector[1],
                "z": self.sun_vector[2],
                "eclipse": self.eclipse_state,
                "xp": lux_readings[0],
                "xm": lux_readings[1],
                "yp": lux_readings[2],
                "ym": lux_readings[3],
                "zp": lux_readings[4],
            }

            DH.log_data("sun", readings)
            print(f"[{self.ID}][{self.name}] Data: {readings}")
