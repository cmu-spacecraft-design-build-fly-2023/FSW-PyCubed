# Core modules containing the framework of the flight software

from core.state_manager import StateManager
from core.template_task import TemplateTask

# expose the Singleton state manager
state_manager = StateManager()
