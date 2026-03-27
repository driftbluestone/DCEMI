import json
from PIL import Image, ImageChops
from pathlib import Path
DIR = Path(__file__).resolve().parent

material_name = input("Name: ")
material_type = input("Type: ")

def material_renderer(material_name: str, material_type: str) -> Image.Image:
    with open(f"{DIR}/materialdata/{material_name}.json", "r") as file:
        material_info = json.load(file)
    try:
        material_set = material_info["icon_set"]
    except KeyError:
        material_set = "dull"
    rgb1 = tuple(int(material_info["color"].removeprefix("0x")[-6:][i : i + 2], 16) for i in (0, 2, 4))
    try:
        rgb2 = tuple(int(material_info["secondary_color"].removeprefix("0x")[-6:][i : i + 2], 16) for i in (0, 2, 4))
    except:
        rgb2 = None

    def tint_rgb(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
        img = img.convert("RGBA")
        r, g, b, a = img.split()
        rgb_img = Image.merge("RGB", (r, g, b))
        tint_layer = Image.new("RGB", rgb_img.size, rgb)
        tinted = ImageChops.multiply(rgb_img, tint_layer)
        return Image.merge("RGBA", (*tinted.split(), a))

    with Image.open(f"{DIR}/gui/gtceu/item/material_sets/{material_set}/{material_type}.png") as im:
        base = tint_rgb(im, rgb1)

    if rgb2:
        with Image.open(f"{DIR}/gui/gtceu/item/material_sets/{material_set}/{material_type}_secondary.png") as im:
            top = tint_rgb(im, rgb2)
            base = Image.alpha_composite(base, top)

    with Image.open(f"{DIR}/gui/gtceu/item/material_sets/{material_set}/{material_type}_overlay.png") as im:
        im_mask = im.convert("RGBA")
        im = im.convert("RGB")
        
        base.paste(im, mask=im_mask)
    image = base
    return image
base = material_renderer(material_name, material_type)
base.save(f"{DIR}/image.png")