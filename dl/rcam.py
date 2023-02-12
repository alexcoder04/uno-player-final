"""
Camera Interface for running directly on the Raspberry Pi
"""

import tempfile
import tflite_runtime.interpreter as tflite
from PIL import Image
import numpy as np
import os

from .generic import _input, card_valid


COLORS = ["b", "g", "j", "r", "y"]
NUMBERS = ["+2", "+4", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "j", "n", "r"]


class RCamDataloader:
    def __init__(self, dev_mode: bool = True, models_path: str = "./nn/tflite") -> None:
        self.TMPFILE = f"{tempfile.gettempdir()}/uno-player-card.jpg"
        self.DEV_MODE = dev_mode
        print("Loading models...")

        self.ci = tflite.Interpreter(f"{models_path}/colors/model.tflite")
        self.ci.allocate_tensors()
        self.cid = self.ci.get_input_details()

        self.ni = tflite.Interpreter(f"{models_path}/numbers/model.tflite")
        self.ni.allocate_tensors()
        self.nid = self.ni.get_input_details()

        if self.DEV_MODE:
            print("Finished loading models")

    def get_players_number(self) -> int:
        return get_players_number()

    def set_input_tensor(self, interpreter: tflite.Interpreter, image: Image) -> None:
        input_tensor = interpreter.tensor(0)()[0]
        input_tensor[:, :] = image

    def classify(self, interpreter: tflite.Interpreter, image: Image, classes: list[str]) -> int:
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        scores = interpreter.get_tensor(output_details["index"])[0]
        #print(np.max(np.unique(scores)))

        scale, zero_point = output_details["quantization"]
        scores_dequan = scale * (scores - zero_point)

        dequan_max_score = np.max(np.unique(scores_dequan))
        #print(dequan_max_score)

        max_score_index = np.where(scores_dequan == np.max(np.unique(scores_dequan)))[0][0]

        #print(max_score_index, dequan_max_score)
        return max_score_index
        #print(classes[max_score_index])

    def read_card(self, prompt: str) -> tuple:
        print(prompt)
        valid = False
        while not valid:
            _input("Hold the card in front of camera and press enter...")
            os.system(f"raspistill -t 10000 -o {tempfile.gettempdir()}/uno-player-card.jpeg -w 224 -h 224")
            image = Image.open(f"{tempfile.gettempdir()}/uno-player-card.jpeg").resize((224, 224))
            self.set_input_tensor(self.ci, image)
            c = COLORS[self.classify(self.ci, image, COLORS)]
            self.set_input_tensor(self.ni, image)
            n = NUMBERS[self.classify(self.ni, image, NUMBERS)]
            if card_valid(c, n):
                break
            print("There was an error while trying to detect card, please try again.\n")
        return (c, n)
