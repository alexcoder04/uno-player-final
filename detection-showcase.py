#!/usr/bin/env python3

from dl import RCamDataloader, COLOR_MAP, NUMBER_MAP

dataloader = RCamDataloader()

print("CARD DETECTION SHOWCASE")

while True:
    (c, n) = dataloader.read_card("")
    print(f"Detected {COLOR_MAP[c]} {NUMBER_MAP[n]}!")
