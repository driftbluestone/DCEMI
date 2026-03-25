import discord, pathlib, time, json
import PIL
DIR = pathlib.Path(__file__).resolve().parent

with open(f"{DIR}/../../TOKEN.txt", "r") as file:
    TOKEN = file.read()

bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(f'oh boy {bot.user}!')

items = {}
@tree.command(name="imager",description="imager")
async def imager(interaction:discord.Interaction):
    time1 = int(time.time())
    await interaction.response.send_message("Uploading images...")
    with open(f"{DIR}/temp/index.json") as file:
        recipes = json.load(file)
    length = len(recipes)
    count = 0
    errors = []
    for recipe in recipes:
        count+=1
        try:
            message: discord.Message = await interaction.channel.send(f"{str(count)}/{length}, {(count/length)*100}%" ,file=discord.File(f"{DIR}/temp/{recipe["file"]}"))
            image_url = message.attachments[0].url

            for output in recipe["outputs"]:
                output = list(output.values())[0]
                items[output.split(":")[1]] = items.get(output, {})
                items[output.split(":")[1]]["output"] = items[output.split(":")[1]].get("output", {})
                items[output.split(":")[1]]["output"][recipe["file"][6:]] = image_url
            for input in recipe["inputs"]:
                id, input = list(input.items())[0]
                if id == "id":
                    items[input.split(":")[1]] = items.get(input, {})
                    items[input.split(":")[1]]["input"] = items[input.split(":")[1]].get("input", {})
                    items[input.split(":")[1]]["input"][recipe["file"][6:]] = image_url
        except:
            error_int = recipes.index(recipe)
            errors.append(error_int)
            print(f"Error in image {error_int+1}")
            
    for k,v in items.items():
        with open(f"{DIR}/recipedata/{k}.json", "w") as file:
            json.dump(v, file)
    time2 = int(time.time())
    await interaction.channel.send(f"Finished uploads. Started at {time1}, ended at {time2}, total time: {time2-time1}s, or {(time2-time1)/60}m.")


bot.run(TOKEN)