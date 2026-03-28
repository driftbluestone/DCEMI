import guibuilder, itemrenderer, json
from pathlib import Path
from PIL import Image
DIR = Path(__file__).resolve().parent

recipe = {"gtceu__bender": [
      {
        "id": "gtceu:bender/bend_aluminium_to_plate",
        "category": "gtceu:bender",
        "width": 150,
        "height": 61,
        "catalysts": [
          {
            "id": "gtceu:programmed_circuit",
            "chance": 0.0,
            "nbt": "{Configuration:1}"
          }
        ],
        "inputs": [
          {
            "id": "gtceu:polytetrafluoroethylene_gear"
          },
          {
            "id": "gtceu:polytetrafluoroethylene_spring"
          },
          {
            "id": "gtceu:ethylene"
          }
        ],
        "outputs": [
          {
            "id": "gtceu:exquisite_polyethylene_gem"
          },
          {
            "id": "gtceu:exquisite_neutronium_gem"
          },
          {
            "id": "gtceu:exquisite_americium_gem"
          }
        ],
        "workstations": [
          "gtceu:lv_bender",
          "gtceu:mv_bender",
          "gtceu:hv_bender",
          "gtceu:ev_bender",
          "gtceu:iv_bender",
          "gtceu:luv_bender",
          "gtceu:zpm_bender",
          "gtceu:uv_bender",
          "gtceu:uhv_bender",
          "gtceu:uev_bender",
          "gtceu:uiv_bender",
          "gtceu:uxv_bender",
          "gtceu:opv_bender",
          "gtceu:large_material_press"
        ]
    }]}

input_count = len(recipe["gtceu__bender"][0]["inputs"])
try:
    input_count += len(recipe["gtceu__bender"][0]["catalysts"])
except ValueError:
    pass

output_count = len(recipe["gtceu__bender"][0]["outputs"])
gui = guibuilder.create_gui(input_count, output_count, "bending")
def fill_slots(gui: Image.Image, inputs: dict, outputs: dict) -> Image.Image:
    horizontal = 9
    vertical = 9
    for i in inputs:
        item = i["id"]
        if item != "gtceu:programmed_circuit":
            material = item.split(":")[1]
            material, material_type = get_material(material)
            material_image = itemrenderer.material_renderer(material, material_type)
            material_image = material_image.convert("RGBA")
            gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
            horizontal += 18
            if horizontal > 60: horizontal, vertical = 9, vertical +18
            continue

        circ_num = int(i["nbt"][15:-1])+1
        with Image.open(f"{DIR}/gui/gtceu/item/programmed_circuit/{circ_num}.png") as material_image:
            material_image = material_image.convert("RGBA")
            gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
            horizontal += 18
            if horizontal > 60: horizontal, vertical = 9, vertical +18

    horizontal = gui.output_slot_distance
    vertical = 9
    for i in outputs:
        i = list(i.values())[0]
        material = i.split(":")[1]
        material, material_type = get_material(material)
        material_image = itemrenderer.material_renderer(material, material_type)
        material_image = material_image.convert("RGBA")
        gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
        horizontal += 18
        if horizontal > (60+ gui.output_slot_distance): horizontal, vertical = gui.output_slot_distance, 9

    return gui

def get_material(material):
    with open(f"{DIR}/materialdata/_materials.json", "r") as file:
        materials = json.load(file)
    material_name_candidates = []
    for i in materials:
        if i in material:
            material_name_candidates.append(i)
    
    
    material_name = sorted(material_name_candidates, key=len)[-1]

    material_type = material.replace(f"{material_name}_", "")
    if material_type == "exquisite_gem": material_type = "gem_exquisite"
    if material_type == "flawless_gem": material_type = "gem_flawless"
    return material_name, material_type

inputs = recipe["gtceu__bender"][0]["inputs"]
try:
    inputs += recipe["gtceu__bender"][0]["catalysts"]
except ValueError:
    pass
gui = fill_slots(gui, recipe["gtceu__bender"][0]["inputs"], recipe["gtceu__bender"][0]["outputs"]) 

gui = gui.resize((8*gui.width, 8*gui.height), resample= Image.BOX)
gui.save(f"{DIR}/gui.png")
gui.show()
