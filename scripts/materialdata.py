import os, json, re
from pathlib import Path
DIR = Path(__file__).resolve().parent

data = ""
for file in os.listdir(f"{DIR}/temp"):
    if not file.endswith(".java"): continue
    with open(f"{DIR}/temp/{file}", "r") as file:
        data += file.read()
data = data.split(";")
new_data = []
for i in data:
    if i.startswith("\n\n"):
        new_data.append(i)
data = []
for i in new_data:
    data.append(i.strip())
materials = {}
for i in data:
    material_name, material_info = i.split(" = ")
    material_data = {}
    if ".color" in material_info: material_data["color"] = re.search(r"\.color\(([^)]+)\)", material_info).group(1)
    if ".secondaryColor" in material_info: material_data["secondary_color"] = re.search(r"\.secondaryColor\(([^)]+)\)", material_info).group(1)
    if ".iconSet" in material_info: material_data["icon_set"] = re.search(r"\.iconSet\(([^)]+)\)", material_info).group(1)
    materials[material_name] = material_data

snake_case_materials = {}
for k, v in materials.items():
    if not v:
        continue
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    s2 = s2.lower()
    snake_case_materials[s2] = v

for k, v in snake_case_materials.items():
    with open(f"{DIR}/../materialdata/{k}.json", "w") as file:
        json.dump(v, file, indent=2)
