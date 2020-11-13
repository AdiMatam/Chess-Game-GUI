from PIL import Image
import os


def resize(size):
    img = Image.open(r"images\bbishop.png")
    if img.size[0] == size:
        return
    for file in os.listdir("images"):
        img = Image.open(fr"images\{file}").resize((size, size))
        img.save(fr"images\{file}")
