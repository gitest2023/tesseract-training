# use this script to rename all the image files before generating boxfiles.
# Language and font should not have spaces and preferable an abbreviated name should be used.

import glob
import os
import shutil

dir = 'data/images'
targetDir = "data/prepared"
images = [f for f in os.listdir(dir)[:2] if f.endswith(('.jpg', '.jpeg', '.png', '.tif', '.bmp'))]

print(f"{len(images)} number of images found")

lang = input('Enter The language without spaces\n')
font = input('Enter font without spaces\n')

part1 = f"{lang}.{font}.exp"

# Create target folder (/prepared) if not exists
if (not os.path.exists(targetDir)):
    os.mkdir(targetDir)
# Remove all files in /prepared if found
for f in glob.glob(os.path.join(targetDir, "*")):
    os.remove(f)

# Rename files with standard format:
# [language name].[font name].exp[number].[file extension]
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    shutil.copyfile(os.path.join(dir, image), os.path.join(targetDir, filename))
    # os.rename(os.path.join(dir, image), os.path.join("data", filename))
