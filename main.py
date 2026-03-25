import discord, typing
from discord import app_commands
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(DCEMI(bot=bot))

class DCEMI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="emi", description="Search EMI")
    async def emi(self, interaction: discord.Interaction, search: typing.Optional[str]):
        if not search:
            pass
        return await interaction.response.send_message(view=None)

