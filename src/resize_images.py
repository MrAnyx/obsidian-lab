from PIL import Image
import os
from pathlib import Path
import math
import glob

ATTACHMENTS = os.environ.get("OBSIDIAN_ATTACHMENT_PATH")
EXTENSIONS = ["png", "jpg", "jpeg"]
MAX_PIXELS = 2_000_000

if not os.path.isdir(ATTACHMENTS):
    raise Exception(f"Path {ATTACHMENTS} doesn't exist")

total = 0
i = 1

for ext in EXTENSIONS:
    total += len(glob.glob1(ATTACHMENTS, f"*.{ext}"))

    for file in Path(ATTACHMENTS).glob(f"*.{ext}"):
        print(f"{i}/{total} -> {file}")
        image = Image.open(file)
        nb_pixels = image.width * image.height

        if nb_pixels >= MAX_PIXELS:
            factor = math.sqrt(MAX_PIXELS / nb_pixels)
            new_width = math.floor(factor * image.width)
            new_height = math.floor(factor * image.height)
            image = image.resize((new_width, new_height))
            image.save(file, quality=75, optimize=True)

        i += 1
