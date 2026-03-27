import pathlib, json
DIR = pathlib.Path(__file__).resolve().parent

items = {}

with open(f"{DIR}/temp/index.json") as file:
    recipes = json.load(file)
length = len(recipes)
for recipe in recipes:
    for output in recipe["outputs"]:
        output = list(output.values())[0]
        items[output.replace(":", "__")] = items.get(output.replace(":", "__"), {})
        items[output.replace(":", "__")]["output"] = items[output.replace(":", "__")].get("output", {})
        items[output.replace(":", "__")]["output"][recipe["category"].replace(":", "__")] = items[output.replace(":", "__")]["output"].get(recipe["category"].replace(":", "__"), [])
        items[output.replace(":", "__")]["output"][recipe["category"].replace(":", "__")].append(recipe)
    for input in recipe["inputs"]:
        id, input = list(input.items())[0]
        if id == "id":
            items[input.replace(":", "__")] = items.get(input.replace(":", "__"), {})
            items[input.replace(":", "__")]["input"] = items[input.replace(":", "__")].get("input", {})
            items[input.replace(":", "__")]["input"][recipe["category"].replace(":", "__")] = items[input.replace(":", "__")]["input"].get(recipe["category"].replace(":", "__"), [])
            items[input.replace(":", "__")]["input"][recipe["category"].replace(":", "__")].append(recipe)
        
for k,v in items.items():
    with open(f"{DIR}/../recipedata/{k}.json", "w") as file:
        json.dump(v, file, indent=2)

