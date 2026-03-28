import pathlib, json
DIR = pathlib.Path(__file__).resolve().parent

items = {}

with open(f"{DIR}/temp/index.json") as file:
    recipes = json.load(file)
length = len(recipes)
for recipe in recipes:
    recipe_data = {}
    recipe_data["id"] = recipe["id"]
    recipe_data["category"] = recipe["category"]
    recipe_data["dimensions"] = [recipe["width"], recipe["height"]]
    try:
        recipe_data["eu_t"] = recipe["euPerTick"]
    except KeyError:
        recipe_data["eu_t"] = 0
    recipe_data["inputs"] = recipe["inputs"]
    recipe_data["outputs"] = recipe["outputs"]
    try:
        recipe_data["catalysts"] = recipe["catalysts"]
    except KeyError:
        recipe_data["catalysts"] = []
    for i in recipe["inputs"]:
        for k, v in i.items():
            if k != "id": continue
            v = v.replace(":", "__")
            items[v] = items.get(v, {})
            items[v]["uses"] = items[v].get("uses", {})
            items[v]["uses"][recipe_data["category"]] = items[v]["uses"].get(recipe_data["category"], [])
            items[v]["uses"][recipe_data["category"]].append(recipe_data)
    for i in recipe["outputs"]:
        for k, v in i.items():
            if k != "id": continue
            v = v.replace(":", "__")
            items[v] = items.get(v, {})
            items[v]["recipes"] = items[v].get("recipes", {})
            items[v]["recipes"][recipe_data["category"]] = items[v]["recipes"].get(recipe_data["category"], [])
            items[v]["recipes"][recipe_data["category"]].append(recipe_data)
 
for k, v in items.items():
    with open(f"{DIR}/../recipedata/{k}.json", "w") as file:
        json.dump(v, file, indent=2)

