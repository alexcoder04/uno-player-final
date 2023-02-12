
from .cmdline import CmdLineDataloader
from .generic import COLOR_MAP, NUMBER_MAP

# importing tensorflow will fail on the raspberry pi
try:
    from .camera import CameraDataloader
except ModuleNotFoundError:
    print("Failed to import Tensorflow-based neural network.")
    print("If you are running on the Raspberry Pi, you can ignore this message, as you are supposed to use TFLite.")
    print("Otherwise make sure that Tensorflow is installed correctly.\n")

from .rcam import RCamDataloader
