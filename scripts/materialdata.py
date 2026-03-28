import os, json, re
from pathlib import Path
DIR = Path(__file__).resolve().parent

with open(f"{DIR}/temp/materials.json", "r") as file:
    data = json.load(file)
materials = {}
for d in data:
    k, v = list(d.items())[0]
    materials[k] = {}
    color = tuple(int((hex(v["color"]).removeprefix("0x").zfill(6))[i : i + 2], 16) for i in (0, 2, 4))
    materials[k]["color"] = color
    if v["secondary_color"] != -1:
        secondary_color = tuple(int((hex(v["secondary_color"]).removeprefix("0x").zfill(6))[i : i + 2], 16) for i in (0, 2, 4))
        materials[k]["secondary_color"] = secondary_color
    materials[k]["icon_set"] = v["icon_set"]

for k, v in materials.items():
    with open(f"{DIR}/../materialdata/{k}.json", "w") as file:
        json.dump(v, file, indent=2)
materials = []
for file in os.listdir(f"{DIR}/../materialdata"):
    materials.append(file[:-5])
with open(f"{DIR}/../materialdata/_materials.json", "w") as file:
    json.dump(materials, file, indent=2)