import os
import subprocess

image = 'datasets/test/test1.JPG'
lang = 'vie'
tessdata_dir = 'runs/train4'

# Ref: https://www.systutorials.com/docs/linux/man/1-tesseract/
os.system(f"tesseract {image} stdout --tessdata-dir {tessdata_dir} -l {lang} --psm 6")