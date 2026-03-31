import render_item
from PIL import Image
render_item.render("exquisite_aluminium_gem").resize((8*render_item.render("exquisite_aluminium_gem").width, 8*render_item.render("exquisite_aluminium_gem").height), resample= Image.BOX).show()