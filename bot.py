import os
import discord
import classyjson as cj
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    intents=discord.Intents.all()
)


with open("data/config.json", "r", encoding="utf-8") as CONFIG:
    bot.c = cj.load(CONFIG)

with open("data/emojis.json", "r", encoding="utf-8") as EMOJIS:
    bot.e = cj.load(EMOJIS)


bot.help_command = None

bot.cog_list = [
    "cogs.core.events",
    "cogs.automation.email"
]
for cog in bot.cog_list:
    bot.load_extension(cog)


@bot.check
def check_author(ctx):
    return ctx.author.id == bot.c.me


bot.run(DISCORD_TOKEN)
