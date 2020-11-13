from PIL import Image
import os
from const import IMGSIZE


def resize():
    for file in os.listdir("images"):
        img = Image.open(fr"images\{file}")
        if img.size[0] == IMGSIZE:
            break
        img.resize((IMGSIZE, IMGSIZE))
        img.save(fr"images\{file}")
