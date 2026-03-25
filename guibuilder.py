from pathlib import Path
from PIL import Image
DIR = Path(__file__).resolve().parent

width = int(input("Gui Width: "))
height = int(input("Gui Height: "))
# base gui colors
# border = (0, 0, 0)
# background = (198, 198, 198)
# top_left = (255, 255, 255)
# bottom_right = (85, 85, 85)
async def create_base_gui(width: int, height: int) -> Image.Image:
    """Creates an empty minecraft GUI"""
    basegui = Image.new('RGBA', (width+8, height+8))
    with Image.open(f"{DIR}/gui/corner_top_left.png") as img:
        basegui.paste(im=img, box=(0, 0))
    with Image.open(f"{DIR}/gui/corner_bottom_left.png") as img:
        basegui.paste(im=img, box=(0, width+4))
    with Image.open(f"{DIR}/gui/corner_top_right.png") as img:
        basegui.paste(im=img, box=(height+4, 0))
    with Image.open(f"{DIR}/gui/corner_bottom_right.png") as img:
        basegui.paste(im=img, box=(height+4, width+4))

    with Image.open(f"{DIR}/gui/border_top.png") as img:
        border_top = img.resize((width, 4))
        basegui.paste(im=border_top, box=(4, 0))
    with Image.open(f"{DIR}/gui/border_bottom.png") as img:
        border_bottom = img.resize((width, 4))
        basegui.paste(im=border_bottom, box=(4, height+4))
    with Image.open(f"{DIR}/gui/border_left.png") as img:
        border_left = img.resize((4, height))
        basegui.paste(im=border_left, box=(0, 4))
    with Image.open(f"{DIR}/gui/border_right.png") as img:
        border_right = img.resize((4, height))
        basegui.paste(im=border_right, box=(width+4, 4))
    with Image.open(f"{DIR}/gui/center.png") as img:
        center = img.resize((width, height))
        basegui.paste(im=center, box=(4, 4))
    return basegui
basegui: Image.Image = create_base_gui(width, height)
basegui.show()