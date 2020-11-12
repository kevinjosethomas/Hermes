import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot's cache is loaded"""

        self.bot.me = self.bot.get_user(self.bot.c.me)
        self.bot.guild = self.bot.get_guild(self.bot.c.guild_id)

        self.bot.error_channel = self.bot.guild.get_channel(self.bot.c.error_channel_id)
        self.bot.testing_channel = self.bot.guild.get_channel(self.bot.c.testing_channel_id)

        print("\nONLINE\n")


def setup(bot):
    bot.add_cog(Events(bot))
