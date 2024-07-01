"""
jetson_comms.py
================
Task to interact with Jetson over UART
"""

from apps.jetson_comms.argus_comm import ArgusComm

# State manager and OBDH
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH
from hal.configuration import SATELLITE


class Task(TemplateTask):

    name = "JETSON"
    ID = 0x13

    argus_comms = ArgusComm(SATELLITE.PAYLOADUART)

    data_keys = [
        "ram",
        "disk",
        "cpu_temp",
        "gpu_temp",
    ]

    async def main_task(self):
        # Only communicate if SAT in NOMINAL state
        if SM.current_state == "NOMINAL":
            if not DH.data_process_exists("jetson"):
                DH.register_data_process("jetson", self.data_keys, "ffff", True, line_limit=40)

            # Register image process
            if not DH.data_process_exists("img"):
                DH.register_image_process()

            # Ask Jetson for image
            print(f"[{self.ID}][{self.name}] Requesting Jetson for image")
            # msg = Message(TRANSMIT_IMAGE, struct.pack(b, 0))

            # Wait for Jetson comms for 0.1s
            if not self.argus_comms.receive_message():
                # No message received
                print(f"[{self.ID}][{self.name}] No message received from Jetson")

            # Image received successfully
            else:
                DH.image_completed()
                print(f"[{self.ID}][{self.name}] Image successfully received from Jetson")
