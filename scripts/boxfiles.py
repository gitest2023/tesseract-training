# reads all the image files present in data dir and creates corresponding box files.
# Files need to have the correct naming convention.
import os

os.chdir('data/prepared')

number_of_files = len(os.listdir('./'))
lang = input('Enter The language without spaces\n')
font = input('Enter font without spaces\n')

# Create a list of box files with format:
# [language name].[font name].exp[number].box
for i in range(0, number_of_files):
    os.system(f"tesseract {lang}.{font}.exp{i}.jpg {lang}.{font}.exp{i} batch.nochop makebox")