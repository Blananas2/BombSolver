from sys import argv
from os import unlink
from glob import glob
import cv2
from features import (serial_number, indicator, button, symbols, password, memory, whos_first)
from debug import log
import config

config.VERBOSITY = 1

FEATURE_EXTRACTORS = {
    "serial_number" : serial_number,
    "indicator" : indicator,
    "button" : button,
    "symbols" : symbols,
    "password" : password,
    "memory_game" : memory,
    "whos_on_first" : whos_first
}

if len(argv) == 1 or argv[1] in "-h, -help":
    print(f"Usage: python generate_character_data.py [type ({'|'.join(FEATURE_EXTRACTORS.keys())})] [delete_images]")
    exit(0)

DATA_TYPE = argv[1]
DEL_IMAGES = True
if len(argv) > 2:
    DEL_IMAGES = int(argv[2]) == 1

TYPES = FEATURE_EXTRACTORS.keys() if DATA_TYPE == "all" else [DATA_TYPE]
for data_type in TYPES:
    INPUT_PATH = "../resources/training_images/" + data_type
    OUTPUT_PATH = f"{INPUT_PATH}/generated_data/"

    NUM_IMAGES = len(glob(OUTPUT_PATH + "*.png"))
    INDEX = NUM_IMAGES

    FILES = glob(INPUT_PATH + "/*.png")
    for file in FILES:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        data = FEATURE_EXTRACTORS[data_type].get_characters(img)
        masks = data[0] if type(data) is tuple else data
        for mask in masks:
            if mask is None:
                print("MASK IS NONE :(")
                exit(0)
            cv2.imwrite(f"{OUTPUT_PATH}{INDEX:03d}.png", mask)
            INDEX += 1
        if DEL_IMAGES:
            unlink(file)

    log(f"Captured {INDEX-NUM_IMAGES} images. Total images: {INDEX}")
