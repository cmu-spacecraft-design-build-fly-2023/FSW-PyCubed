# Onboard Data Handling (OBDH) Task

from tasks.template_task import DebugTask
from apps.data_handler import DataHandler

class Task(DebugTask):

    name = 'OBDH'
    ID = 0x02
    

    async def main_task(self):






        print(f'[{self.ID}][{self.name}] Temp.')
