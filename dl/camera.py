"""
Default Camera Interface for entering the cards and other data
"""

import json
import numpy as np
import os
import requests
import tempfile
import tensorflow as tf

from .generic import get_players_number, _input, clear, get_how_many_to_pull, COLOR_MAP, NUMBER_MAP


class CameraDataloader:
    def __init__(self, dev_mode: bool = True, models_path: str = "./nn/tensorflow") -> None:
        self.TMPFILE = f"{tempfile.gettempdir()}/uno-player-card.jpeg"
        self.RASPI_IP = CameraDataloader.getenv("RASPI_IP", "192.168.178.32")
        self.DEV_MODE = dev_mode
        print("Loading models...")

        self.c_model = tf.keras.models.load_model(f"{models_path}/colors/model.h5")
        self.c_model.load_weights(f"{models_path}/colors/model_weights")
        with open(f"{models_path}/colors/classes.json") as f:
            self.c_classes = json.load(f)

        self.n_model = tf.keras.models.load_model(f"{models_path}/numbers/model.h5")
        self.n_model.load_weights(f"{models_path}/numbers/model_weights")
        with open(f"{models_path}/numbers/classes.json") as f:
            self.n_classes = json.load(f)

    def get_players_number(self) -> int:
        return get_players_number()

    def _download_image(self) -> None:
        while True:
            try:
                resp = requests.get(f"http://{self.RASPI_IP}:8000/image.jpeg")
                break
            except requests.exceptions.ConnectionError:
                print("Connection to Raspberry Pi failed. Is the server running?")
                _input("Press <enter> to retry...")
        with open(self.TMPFILE, "wb") as f:
            f.write(resp.content)

    def _load_image(self):
        img = tf.keras.preprocessing.image.load_img(self.TMPFILE, target_size=(32, 32))
        X = tf.keras.preprocessing.image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        return np.vstack([X])

    def _correct(self, c_res, n_res, c_val, n_val) -> tuple:
        if self.DEV_MODE:
            print(f"=> {self.c_classes[c_res]}")
            for i, v in enumerate(c_val[0]):
                print(f"{self.c_classes[i]} = {v}")
            print(f"=> {self.n_classes[n_res]}")
            for i, v in enumerate(n_val[0]):
                print(f"{self.n_classes[i]} = {v}")
        else:
            print(
                f"Detected {COLOR_MAP[self.c_classes[c_res]]} {NUMBER_MAP[self.n_classes[n_res]]}"
            )
        inp = _input("Correct card (enter if ok): ")
        if inp == "":
            color = self.c_classes[c_res]
            number = self.n_classes[n_res]
        else:
            while True:
                try:
                    [color, number] = inp.split(",")
                    break
                except ValueError:
                    print("Sorry, cannot read your input")
                    inp = _input("Correct card (enter if ok): ")
            color, number = color.strip(), number.strip()
            print(f"Corrected to {COLOR_MAP[color]} {NUMBER_MAP[number]}")
        return color, number

    def read_card(self, prompt: str) -> tuple:
        print(prompt)
        _input("Hold the card in front of camera and press enter...")
        self._download_image()
        images = self._load_image()
        c_val = self.c_model.predict(images)
        n_val = self.n_model.predict(images)
        c_res = CameraDataloader.get_max(c_val)
        n_res = CameraDataloader.get_max(n_val)
        while True:
            color, number = self._correct(c_res, n_res, c_val, n_val)
            if color not in ("r", "g", "b", "y", "j"):
                print("Sorry, invalid color, use (r,g,b,y,j)")
                continue
            if color != "s" and number not in (
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "r",
                "n",
                "+2",
                "j",
                "+4",
            ):
                print("Sorry, invalid number, use (0,1,2,3,4,5,6,7,8,9,r,n,+2,j,+4)")
                continue
            # if color == "j" and number not in ("j","+4"):
            #    print("Sorry, invalid number, use (j,+4)")
            #    continue
            if color == "j":
                color = "s"
            special = True if color == "s" else False
            return color, number, special

    def get_how_many_to_pull(self) -> int:
        return get_how_many_to_pull()

    def clear(self) -> None:
        clear()

    @staticmethod
    def get_max(val):
        max_val = -1000
        res = 1000
        for i, v in enumerate(val[0]):
            if v >= max_val:
                max_val = v
                res = i
        return res

    @staticmethod
    def getenv(key: str, default: str = "") -> str:
        try:
            return os.environ[key]
        except KeyError:
            return default
