import sys
from sm_configuration import SM_CONFIGURATION, TASK_REGISTRY
import flight.core.state_manager as state_manager

sys.path.append(".")
print("sys.path", sys.path)

# import flight.core.scheduler as scheduler
# scheduler.enable_debug_logging()

state_manager.start("STARTUP", SM_CONFIGURATION, TASK_REGISTRY)