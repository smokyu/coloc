from discord.ext import commands
from bot import ColoBot

class BaseCog(commands.Cog):
    def __init__(self, colobot: ColoBot):
        self.colobot = colobot