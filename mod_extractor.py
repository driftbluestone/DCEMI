import os, shutil
from pathlib import Path
DIR = Path(__file__).resolve().parent

for file in os.listdir(f"{DIR}/mods"):
    os.rename(f"{DIR}/mods/{file}", f"{DIR}/mods/{file[:-4]}.zip")
for file in os.listdir(f"{DIR}/mods"):
    shutil.unpack_archive(f"{DIR}/mods/{file}", f"{DIR}/mod_data/{file[:-4]}")