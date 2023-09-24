import os
import shutil
import subprocess
from datetime import datetime

train_with_exist_box_files = True
lang = ''
font = ''
ALLOWED_IMAGES = ('.jpg', '.png', '.tif', '.bmp')
IMAGES_DIR = 'datasets/vie/fonts/arial'
TR_DIR = f'{IMAGES_DIR}/tr'
OUT_DIR = f'{IMAGES_DIR}/.out'
BACKUP_DIR = f'{IMAGES_DIR}/.backup'

# Create `tr`, `.out` and `.backup` directories if not exists
if not os.path.exists(TR_DIR):
    os.makedirs(TR_DIR, exist_ok=True)
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR, exist_ok=True)
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR, exist_ok=True)

# Remove the previous trained files berfore traning
for image_file in os.listdir(TR_DIR):
    try: os.remove(f'{TR_DIR}/{image_file}')
    except: pass
for image_file in os.listdir(OUT_DIR):
    try: os.remove(f'{OUT_DIR}/{image_file}')
    except: pass

# 1 - Create box files (*.box) and tr files (*.tr)
unicharset_args = ''
tr_files = ''
timestamp = str(datetime.now().timestamp())
temp_backup_dir = os.path.join(BACKUP_DIR, timestamp)
for image_file in os.listdir(IMAGES_DIR):
    # Backup *.box files before creating
    if train_with_exist_box_files == False and image_file.endswith('.box'):
        if not os.path.exists(temp_backup_dir):
            os.makedirs(temp_backup_dir, True)
        # shutil.copyfile(f'{IMAGES_DIR}/{image_file}', f'{temp_backup_dir}/{image_file}')
        shutil.move(f'{IMAGES_DIR}/{image_file}', f'{temp_backup_dir}/{image_file}')

    if image_file.endswith(ALLOWED_IMAGES):
        if lang == '':
            lang = image_file.split('.')[0]
        if font == '':
            font = image_file.split('.')[1]
        expi = image_file.split('.')[2]

        # 1.1 - Create *box files if not exists
        if train_with_exist_box_files:
            print(f'{image_file} => existed')
        else:
            # Delete previous box files if found
            if os.path.exists(f'{IMAGES_DIR}/{lang}.{font}.{expi}.box'):
                os.remove(f'{IMAGES_DIR}/{lang}.{font}.{expi}.box')
            # Create new *.box files
            os.system(f"tesseract {IMAGES_DIR}/{image_file} {IMAGES_DIR}/{lang}.{font}.{expi} batch.nochop makebox")
            print(f'{lang}.{font}.{expi} => created')

        # 1.2 - Create *.tr files
        os.system(f"tesseract {IMAGES_DIR}/{image_file} {TR_DIR}/{image_file[:-4]} nobatch box.train")

        unicharset_args += f'{IMAGES_DIR}/{lang}.{font}.{expi}.box '
        tr_files += f'{TR_DIR}/{lang}.{font}.{expi}.tr '

# 2 - Create unicharset file
subprocess.run(f'unicharset_extractor --output_unicharset {OUT_DIR}/unicharset {unicharset_args}')

# 3 - Creating font properties file (font_properties)
with open(f'{OUT_DIR}/font_properties', 'w') as f:
    f.write(f"{font} 0 0 0 0 0\n")
    f.write(f"{font}b 0 1 0 0 0\n")
    f.write(f"{font}bi 1 1 0 0 0\n")
    f.write(f"{font}i 1 0 0 0 0")

# 4 - Clustering
# 4.1 - Create two other data files (inttemp, pffmtable) via `mftraining` command
# - inttemp (the shape prototypes)
# - pffmtable (the number of expected features for each character)
# NOTE: mftraining will produce a shapetable file if you didn’t run shapeclustering
# Ref: https://www.systutorials.com/docs/linux/man/1-mftraining/
mftraining = f'mftraining -F {OUT_DIR}/font_properties \
                          -U {OUT_DIR}/unicharset \
                          -O {OUT_DIR}/{lang}.unicharset \
                          -D {OUT_DIR} {tr_files}'
subprocess.run(mftraining, check=True)

# 4.2 - Create normproto data file (the character normalization sensitivity prototypes) via `cntraining` command
cntraining = f'cntraining -D {OUT_DIR} {tr_files}'
subprocess.run(cntraining, check=True)

# 4.3 - Rename files after clustered into standard names
os.rename(f'{OUT_DIR}/inttemp', f'{OUT_DIR}/{lang}.inttemp')
os.rename(f'{OUT_DIR}/normproto', f'{OUT_DIR}/{lang}.normproto')
os.rename(f'{OUT_DIR}/pffmtable', f'{OUT_DIR}/{lang}.pffmtable')
os.rename(f'{OUT_DIR}/shapetable', f'{OUT_DIR}/{lang}.shapetable')

# 5 - Combine together all files (shapetable, normproto, inttemp, pffmtable, unicharset) to signle file (*.traineddata file)
os.system(f'combine_tessdata {OUT_DIR}/{lang}.')

# 6 - Clone *.traineddata file (<lang>.traineddata) into new file with standard name (<lang>-<font>.traineddata)
root_dir = os.getcwd()
shutil.copyfile(
    os.path.join(root_dir, OUT_DIR, f'{lang}.traineddata'),
    os.path.join(root_dir, OUT_DIR, f'{lang}-{font}.traineddata')
)
