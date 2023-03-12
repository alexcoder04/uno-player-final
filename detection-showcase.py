#!/usr/bin/env python3

from dl import RCam2Dataloader, COLOR_MAP, NUMBER_MAP

dataloader = RCam2Dataloader()

print("CARD DETECTION SHOWCASE")

while True:
    (c, n, _) = dataloader.read_card("", correct=False)
    print(f"Detected {COLOR_MAP[c]} {NUMBER_MAP[n]}!")
