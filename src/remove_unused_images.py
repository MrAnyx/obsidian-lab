import json
import os
from pathlib import Path
import re
import progressbar
from utils.files import get_files_by_extension

from utils.progress_bar import get_progress_bar

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH")
ATTACHMENT = os.environ.get("OBSIDIAN_ATTACHMENT_PATH")
REGEX = r"!\[\[(.*?)\]\]"
EXTENSIONS = [
    "jpg",
    "png",
    "jpeg",
    "webp",
    "mp4",
    "gif",
    "pdf",
    "ico",
    "afdesign",
    "svg",
]

# Check if location exist
if not os.path.isdir(VAULT) or not os.path.isdir(ATTACHMENT):
    raise Exception(f"Path {VAULT} or {ATTACHMENT} doesn't exist")

image_list = []
images_deleted = []

# Retrieve all images
files = get_files_by_extension(VAULT, "md")
progress_bar = get_progress_bar("Preprocessing markdown files: ", files, "files")
for file_path in progress_bar(files):
    if file_path.is_file():

        # Get file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Check if file contains images
        contains_images = re.search(REGEX, content)

        if bool(contains_images):
            images = re.compile(REGEX).findall(content)

            for image in images:
                if image not in image_list:
                    image_list.append(image)


for ext in EXTENSIONS:
    files = get_files_by_extension(ATTACHMENT, ext)
    progress_bar = get_progress_bar(f"Processing {ext} images: ", files, "images")
    for file_path in progress_bar(files):
        if file_path.is_file():

            source_full_path = str(file_path)
            source_filename_with_ext = file_path.name

            contains_images = False

            # Check if file contains images
            for image in image_list:
                if source_filename_with_ext in image:
                    contains_images = True
                    break

            if not contains_images:
                # Remove original image
                os.remove(source_full_path)
                images_deleted.append(source_full_path)

# with open("../.output/images_deleted.json", "w", encoding="utf-8") as file:
#     file.write(json.dumps(images_deleted, indent=4))
