import discord
from discord.ext import commands

class ColoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())

    async def setup_hook(self):
        await self.load_extension("cogs.app")

        await self.tree.sync(guild=discord.Object(id=1218298385480683630))

    async def on_ready(self):
        print(f"{self.user.display_name} has connected. (version: demo)")