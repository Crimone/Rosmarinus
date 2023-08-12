import os
import shutil

folder = r'I:\Soulseek Downloads\Soulseek Shared Folder\Bandari - 12CD' 

files = os.listdir(folder)
duplicates = {}

for file in files:
    name, ext = os.path.splitext(file)
    if name in duplicates:
        duplicates[name].append(file) 
    else:
        duplicates[name] = [file]

for name, filenames in duplicates.items():
    if len(filenames) > 1:
        new_folder = os.path.join(folder, name)
        os.mkdir(new_folder)
        for filename in filenames:
            shutil.move(os.path.join(folder, filename), new_folder)