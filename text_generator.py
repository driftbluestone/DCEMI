import re
from PIL import Image
from pathlib import Path
DIR = Path(__file__).resolve().parent

text_replace = {
    "/":"slash",
    ".":"period",
    "-":"dash",
    ",":"comma",
    "+":"plus",
    "*":"star",
    ")":"close_paren",
    "(":"open_paren",
    "'":"apostrophe",
    "&":"and",
    "%":"percent",
    "$":"dollar",
    "#":"hashtag",
    "\"":"quote",
    "!":"exclamation",
    "~":"tilde",
    "}":"close_curly",
    "{":"open_curly",
    "`":"backtick",
    "_":"underscore",
    "^":"carat",
    "]":"close_square",
    "[":"open_square",
    "\\":"backslash",
    "@":"at",
    "?":"question",
    ">":"greater_than",
    "=":"equal",
    "<":"less_than",
    ";":"semicolon",
    ":":"colon"
}

def generate_text(text: str) -> Image.Image:
    text = list(text)
    text_array = []
    for i in text:

        i= re.sub(r"([a-z])", r"\g<1>2", i)
        for k, v in text_replace.items():
            i = i.replace(k, v)
        text_array.append(i)
    horizontal = 0
    vertical = 10
    text_image = Image.new("RGBA", (1, vertical), (0, 0, 0, 0))
    for i in text_array:
        if i == "\n" or i == "backslashn2":
            horizontal = 0
            vertical += 10
            continue
        with Image.open(f"{DIR}/gui/font/{i}.png") as im:
            bbox = im.getbbox()
            im = im.crop((bbox[0], 0, bbox[2], im.height))
            im_width = im.width + text_image.width + 1
            new_text_image = Image.new('RGBA', (im_width, vertical), (0, 0, 0, 0))
            new_text_image.paste(text_image, (0, 0))
            text_image = new_text_image
            text_image.paste(im, (horizontal, vertical-10))
            horizontal += im.width + 1
    return text_image

text = "w awa\n123\newe we\nw ewe123123"
im = generate_text(text)
im = im.resize((8*im.width, 8*im.height), resample= Image.BOX)
im.show()