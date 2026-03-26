import math
from pathlib import Path
from PIL import Image
DIR = Path(__file__).resolve().parent
with Image.open(f"{DIR}/gui/temp/widgets.png") as img:
    img = img.crop((44,0,68,17))
    img.save(f"{DIR}/gui/arrow.png")

# width = int(input("Gui Width: "))
# height = int(input("Gui Height: "))
input_slots = int(input("Input Slots: "))
output_slots = int(input("Output Slots: "))
# base gui colors
# border = (0, 0, 0)
# background = (198, 198, 198)
# top_left = (255, 255, 255)
# bottom_right = (85, 85, 85)
def create_base_gui(width: int, height: int) -> Image.Image:
    """Creates an empty minecraft GUI"""
    basegui = Image.new('RGBA', (width+8, height+8))
    with Image.open(f"{DIR}/gui/corner_top_left.png") as img:
        basegui.paste(im=img, box=(0, 0))
    with Image.open(f"{DIR}/gui/corner_bottom_left.png") as img:
        basegui.paste(im=img, box=(0, height+4))
    with Image.open(f"{DIR}/gui/corner_top_right.png") as img:
        basegui.paste(im=img, box=(width+4, 0))
    with Image.open(f"{DIR}/gui/corner_bottom_right.png") as img:
        basegui.paste(im=img, box=(width+4, height+4))

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

def add_slots(gui: Image.Image, in_slots: int, out_slots: int) -> Image.Image:
    vertical = 8
    horizontal = 8
    height = max([math.ceil(input_slots / 3), math.ceil(output_slots / 3)])
    gui.__setattr__("input_slots", in_slots)
    gui.__setattr__("output_slots", out_slots)

    with Image.open(f"{DIR}/gui/slot.png") as img:
        for i in range(in_slots):
            i += 1
            gui.paste(im=img, box=(horizontal, vertical))
            horizontal+=18
            if i % 3 == 0:
                horizontal = 8
                vertical += 18
    
    arrow_distance = 54 + 20
    if input_slots < 3:
        arrow_distance = input_slots*18 + 20
    arrow_height = height * 9
    with Image.open(f"{DIR}/gui/arrow.png") as img:
        gui.paste(im=img, box=(arrow_distance, arrow_height))
    
    vertical = 8
    horizontal = arrow_distance + 24 + 12
    with Image.open(f"{DIR}/gui/slot.png") as img:
        for i in range(out_slots):
            i += 1
            gui.paste(im=img, box=(horizontal, vertical))
            horizontal+=18
            if i % 3 == 0:
                horizontal = arrow_distance + 24 + 12
                vertical += 18
    return gui

def create_gui(input_slots: int, output_slots: int) -> Image.Image:
    width = 56
    height = (max([math.ceil(input_slots / 3), math.ceil(output_slots / 3)])) * 18 + 8
    if input_slots >= 3:
        width += 54
    else:
        width += 18*input_slots
    if output_slots >= 3:
        width += 54
    else:
        width += 18*output_slots

    gui = create_base_gui(width, height)
    gui = add_slots(gui, input_slots, output_slots)
    return gui

basegui = create_gui(input_slots, output_slots)
basegui = basegui.resize((8*basegui.width, 8*basegui.height), resample= Image.BOX)
basegui.save(f"{DIR}/gui.png")


basegui.show()