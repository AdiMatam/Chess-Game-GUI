from PIL import Image
import os
from const import IMGSIZE

os.chdir("images")
for file in os.listdir(os.getcwd()):
    img = Image.open(file).resize((IMGSIZE, IMGSIZE))
    img.save(file)
