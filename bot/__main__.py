import discord
from discord.ext import commands
from .config import settings
from .services.metrics import Metrics
from database.db import Database
from .cogs.status import StatusCog

class StatusBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.metrics = Metrics()
        self.db = Database(settings.database_path)

    async def setup_hook(self):
        await self.db.initialize()
        await self.add_cog(StatusCog(self))

        test_guild = discord.Object(id=settings.guild_id)
        self.tree.copy_global_to(guild=test_guild)
        await self.tree.sync(guild=test_guild)

    async def close(self):
        await self.db.close()
        await super().close()

bot = StatusBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | {len(bot.guilds)} server(s)")

bot.run(settings.token)
