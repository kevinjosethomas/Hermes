import os
import discord
import classyjson as cj
from dotenv from load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    intents=discord.Intents.all()
)

bot.help_command = None

bot.cog_list = [
    "cogs.core.events",
    "cogs.automation.email"
]
for cog in bot.cog_list:
    bot.load_extension(cog)


@bot.check
def check_author(ctx):
    return ctx.author.id == 418707912836382721


bot.run(DISCORD_TOKEN)
