# Use this script to rename all the image files before generating boxfiles.
# Language and font should not have spaces and preferable an abbreviated name should be used.

import glob
import os
import shutil

IMAGES_DIR = 'datasets/images/raw'
PROCESSED_DIR = "datasets/images/processed"
ALLOWED_IMAGES = ('.jpg', '.png', '.tif', '.bmp')

images = [f for f in os.listdir(IMAGES_DIR) if f.endswith(ALLOWED_IMAGES)]

print(f"Number of images found: {len(images)}")

lang = input('Enter your language (without spaces)\n')
font = input('Enter your font (without spaces)\n')

part1 = f"{lang}.{font}.exp"

# Create new folder to save after processed if not exists
if (not os.path.exists(PROCESSED_DIR)):
    os.mkdir(PROCESSED_DIR)

# Remove all previous propcessed files if found
for f in glob.glob(os.path.join(PROCESSED_DIR, "*")):
    os.remove(f)

# Rename files with standard format:
# [language_name].[font_name].exp[number].[file_extension]
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    shutil.copyfile(os.path.join(IMAGES_DIR, image), os.path.join(PROCESSED_DIR, filename))
    # os.rename(os.path.join(IMAGES_DIR, image), os.path.join(PROCESSED_DIR, filename))
