from PIL import Image
import os
from pathlib import Path
import re
import progressbar
from fs import open_fs

from utils.files import get_files_by_extension
from utils.progress_bar import get_progress_bar

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH")
ATTACHMENT = os.environ.get("OBSIDIAN_ATTACHMENT_PATH")
EXTENSIONS = ["jpg", "png", "jpeg"]
REGEX = r"!\[\[.*?\]\]"
FS = open_fs("osfs://" + ATTACHMENT)
QUALITY = 85

# Check if location exist
if not os.path.isdir(VAULT) or not os.path.isdir(ATTACHMENT):
    raise Exception(f"Path {VAULT} or {ATTACHMENT} doesn't exist")

######################################################################
#                         Convert images                             #
######################################################################
for ext in EXTENSIONS:
    files = get_files_by_extension(ATTACHMENT, ext)
    progress_bar = get_progress_bar(f"Processing {ext} images: ", files, "images")
    for file_path in progress_bar(files):
        if file_path.is_file():
            source_path = str(file_path.parent)
            source_full_path = str(file_path)
            source_filename_with_ext = file_path.name
            source_filename = file_path.stem
            source_extension = file_path.suffix

            dest_path = ATTACHMENT
            dest_filename_with_ext = source_filename + ".webp"
            dest_full_path = os.path.join(dest_path, dest_filename_with_ext)
            dest_filename = source_filename
            dest_extension = ".webp"

            # Save new image
            image = Image.open(source_full_path)
            image.save(dest_full_path, "WEBP", quality=QUALITY, optimize=True)

            # Update metadata
            FS.setinfo(
                dest_filename_with_ext,
                {
                    "details": {
                        "created": os.path.getctime(source_full_path),
                        "modified": os.path.getmtime(source_full_path),
                        "accessed": os.path.getatime(source_full_path),
                    }
                },
            )

            # Remove original image
            os.remove(source_full_path)


######################################################################
#                           Update files                             #
######################################################################
files = get_files_by_extension(VAULT, "md")
progress_bar = get_progress_bar("Processing markdown files: ", files, "files")
for file_path in progress_bar(files):
    if file_path.is_file():

        # Get file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Check if file contains images
        contains_images = re.search(REGEX, content)

        if bool(contains_images):
            modified_content = content
            pattern = re.compile(REGEX)

            # Find all images
            matches = pattern.findall(modified_content)

            # For each image found
            for match in matches:
                # Replace the extension to webp
                modified_match = re.sub(
                    r"\.(" + "|".join(EXTENSIONS) + r")", ".webp", match
                )

                # Update the file content
                modified_content = re.sub(
                    re.escape(match), modified_match, modified_content
                )

            # Write the new content to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modified_content)
