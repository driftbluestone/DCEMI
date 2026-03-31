import json
from PIL import Image, ImageChops
from pathlib import Path
DIR = Path(__file__).resolve().parent.parent.parent
pattern = "mod_data/gtceu*/assets/gtceu/textures"
DIR = str(next(DIR.glob(pattern)))

def material_renderer(material_name: str, material_type: str) -> Image.Image:
    with open(f"{DIR}/../../../../../materialdata/{material_name}.json", "r") as file:
        material_info = json.load(file)
    try:
        material_set = material_info["icon_set"]
        
    except KeyError:
        material_set = "dull"
    if material_type in ["gem_exquisite", "gem_flawless"]:
        material_set = "dull"
    rgb1 = tuple(material_info["color"])
    try:
        rgb2 = tuple(material_info["secondary_color"])
    except:
        rgb2 = None

    if material_set in ["fluid", "gas", "molten"]:
        if material_set == "fluid": material_set = "liquid"
        try:
            with Image.open(f"{DIR}/block/fluids/fluid.{material_name}.png") as im: return _tint_rgb(im, rgb1).crop((0, 0, 16, 16))
        except FileNotFoundError:
            with Image.open(f"{DIR}/block/material_sets/dull/{material_set}.png") as im: return _tint_rgb(im, rgb1).crop((0, 0, 16, 16))

    with Image.open(f"{DIR}/item/material_sets/{material_set}/{material_type}.png") as im:
        base = _tint_rgb(im, rgb1)

    if rgb2:
        with Image.open(f"{DIR}/item/material_sets/{material_set}/{material_type}_secondary.png") as im:
            top = _tint_rgb(im, rgb2)
            base = Image.alpha_composite(base, top)
    with Image.open(f"{DIR}/item/material_sets/{material_set}/{material_type}_overlay.png") as im:
        im_mask = im.convert("RGBA")
        im = im.convert("RGB")
        
        base.paste(im, mask=im_mask)
    base = base.crop((0, 0, 16, 16))
    image = base
    return image

def _tint_rgb(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    tint_layer = Image.new("RGB", rgb_img.size, rgb)
    tinted = ImageChops.multiply(rgb_img, tint_layer)
    return Image.merge("RGBA", (*tinted.split(), a))

def get_material(material: str) -> tuple[str, str]:
    with open(f"{DIR}/../../../../../materialdata/_materials.json", "r") as file:
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

# image = material_renderer(*get_material("naquadah_alloy_plate"))
# image = image.resize((8*image.width, 8*image.height), resample= Image.BOX)
# image.show()
def render(material: str) -> Image.Image:
    return material_renderer(*get_material(material))