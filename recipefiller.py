import guibuilder, itemrenderer
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
            "chance": 0.0
          }
        ],
        "inputs": [
          {
            "id": "gtceu:wheat_ingot"
          }
        ],
        "outputs": [
          {
            "id": "gtceu:ammonia_plate"
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
        i = list(i.values())[0]
        if i != "gtceu:programmed_circuit":
            material = i.split(":")[1].split("_")
            material_type = material[-1]
            material = "_".join(material[:-1])
            material_image = itemrenderer.material_renderer(material, material_type)
            material_image = material_image.convert("RGBA")
            gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
            horizontal += 18
            if horizontal > 60: horizontal, vertical = 9, 9
            continue
        with Image.open(f"{DIR}/gui/gtceu/item/programmed_circuit/1.png") as material_image:
            material_image = material_image.convert("RGBA")
            gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
            horizontal += 18
            if horizontal > 60: horizontal, vertical = 9, 9

    horizontal = gui.output_slot_distance
    vertical = 9
    for i in outputs:
        i = list(i.values())[0]
        material = i.split(":")[1].split("_")
        material_type = material[-1]
        material = "_".join(material[:-1])
        material_image = itemrenderer.material_renderer(material, material_type)
        material_image = material_image.convert("RGBA")
        gui.paste(im = material_image, mask = material_image, box=(horizontal, vertical))
        horizontal += 18
        if horizontal > 60: horizontal, vertical = gui.output_slot_distance, 9

    return gui
inputs = recipe["gtceu__bender"][0]["inputs"]
try:
    inputs += recipe["gtceu__bender"][0]["catalysts"]
except ValueError:
    pass
gui = fill_slots(gui, recipe["gtceu__bender"][0]["inputs"], recipe["gtceu__bender"][0]["outputs"]) 

gui = gui.resize((8*gui.width, 8*gui.height), resample= Image.BOX)
gui.save(f"{DIR}/gui.png")
gui.show()
