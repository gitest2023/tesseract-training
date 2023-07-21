# Run after annotating all the box files generated from boxfiles.py
# https://github.com/nguyenq/jTessBoxEditor/releases/tag/Release-2.3.1 can be used for annotating.

import os
import subprocess
import shutil

lang = input('Enter The language without spaces\n')
font = input('Enter font without spaces\n')

srcdir = 'data/prepared'
destdir = 'trainfiles'

# Removing all previous trained files.
try:
    os.remove(f'tessdata/{lang}.traineddata')
except OSError:
    pass
files = os.listdir(srcdir)
for item in files:
    if not item.endswith(('.jpg', '.box')):
        os.remove(os.path.join(srcdir, item))

# Generating the tuples of filenames
files = os.listdir(srcdir)
jpgs = [x for x in files if x.endswith('.jpg')]
boxes = [x for x in files if x.endswith('.box')]
trainfiles = list(zip(jpgs, boxes))

# generating TR files and unicode charecter extraction
unicharset = f"unicharset_extractor --output_unicharset ../../{destdir}/unicharset "
unicharset_args = f""
errorfiles = []

for image, box in trainfiles:
    unicharset_args += f"{box} "
    if os.path.isfile(f"{destdir}/{image[:-4]}.tr"):
        continue
    try:
        print(image)
        os.system(f"tesseract {srcdir}/{image} {destdir}/{image[:-4]} nobatch box.train")
    except:
        errorfiles.append((image, box))

os.chdir(srcdir)

subprocess.run(unicharset + unicharset_args)

os.chdir('../../')

# Writing log file
if len(errorfiles) == 0:
    errorfiles.append(('no', 'Error'))
with open('scripts/logs.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join('%s %s' % x for x in errorfiles))

# Creating font properties file
with open(f"{destdir}/font_properties", 'w') as f:
    f.write(f"{font} 0 0 0 1 0")

# Getting all .tr files and training
root_dir = os.getcwd()
output = os.path.join(root_dir, 'trainoutput')
trfiles = [f for f in os.listdir(destdir) if f.endswith('.tr')]
os.chdir(destdir)

mftraining = f"mftraining -F font_properties -U unicharset -O {output}/{lang}.unicharset -D {output}"
cntraining = f"cntraining -D {output}"

for file in trfiles:
    mftraining += f" {file}"
    cntraining += f" {file}"

# subprocess.run() method to wait for a process to complete
resultMFTraining = subprocess.run(mftraining, check=True)
resultCNTraining = subprocess.run(cntraining, check=True)


# Renaming training files and merging them
os.chdir(output)
os.rename('inttemp', f'{lang}.inttemp')
os.rename('normproto', f'{lang}.normproto')
os.rename('pffmtable', f'{lang}.pffmtable')
os.rename('shapetable', f'{lang}.shapetable')
os.system(f"combine_tessdata {lang}.")

# Copy {lang}.traineddata file to tessdata folder
if (resultMFTraining.returncode == 0 & resultCNTraining.returncode == 0):
    print('Moving generated traineddata file to tessdata folder')
    shutil.copyfile(os.path.join(root_dir, "trainoutput", f'{lang}.traineddata'), os.path.join(root_dir, 'tessdata', f'{lang}.traineddata'))
    # Remove all files after successful
    os.chdir(root_dir)
    subprocess.run("python scripts/purge.py", check=True)
    print('Training Completed')