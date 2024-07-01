import importlib
import sys

# Add necessary paths
sys.path.append("emulator/cp/")
sys.path.append("flight/")

# Mock other modules
sys.modules["micropython"] = __import__("micropython_mock")
sys.modules["ulab"] = __import__("ulab_mock")

# Alias 'hal' to 'emulator'
sys.modules["hal"] = importlib.import_module("emulator")
