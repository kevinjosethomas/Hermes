import os
import ast
import time
import asyncio
import discord
from typing import Union
from discord.ext import commands


def insert_returns(body: str):
    """Inserts required return statements to the eval code"""

    # Insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # For if statements, we insert returns into the body and the or else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # For with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx: commands.Context, *, cog: str):
        """Unloads the specified cog"""

        if cog.lower() == "all":
            for cog_name in self.bot.cog_list:
                self.bot.unload_extension(cog_name)
            await ctx.message.add_reaction(self.bot.e.check)
            return

        if not cog.startswith("cogs."):
            cog = "cogs." + cog

        self.bot.unload_extension(cog)
        await ctx.message.add_reaction(self.bot.e.check)

    @unload.error
    async def unload_error(self, ctx: commands.Context, error):
        """Handles errors triggered while unloading cogs"""

        await ctx.send(f"{self.bot.e.cross} Error while unloading the specified extension")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx: commands.Context, *, cog: str):
        """Loads the specified cog"""

        if cog.lower() == "all":
            for cog_name in self.bot.cog_list:
                self.bot.load_extension(cog_name)
            await ctx.message.add_reaction(self.bot.e.check)
            return

        if not cog.startswith("cogs."):
            cog = "cogs." + cog

        self.bot.load_extension(cog)
        await ctx.message.add_reaction(self.bot.e.check)

    @load.error
    async def load_error(self, ctx: commands.Context, error):
        """Handles errors triggered while loading cogs"""

        await ctx.send(f"{self.bot.e.cross} Error while loading the specified extension")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: commands.Context, *, cog: str):
        """Reloads the specified cog"""

        if cog.lower() == "all":
            for cog_name in self.bot.cog_list:
                self.bot.reload_extension(cog_name)
            await ctx.message.add_reaction(self.bot.e.check)
            return

        if not cog.startswith("cogs."):
            cog = "cogs." + cog

        self.bot.reload_extension(cog)
        await ctx.message.add_reaction(self.bot.e.check)

    @reload.error
    async def reload_error(self, ctx: commands.Context, error):
        """Handles errors triggered while reloading cogs"""

        await ctx.send(f"{self.bot.e.cross} Error while reloading the specified extension")

    @commands.command()
    @is_staff()
    async def eval(self, ctx: commands.Context, *, cmd: str):
        """Evaluates the provided code"""

        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # Add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # Wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'discord': discord,
            'commands': commands,
            'asyncio': asyncio,
            'time': time,
            'os': os,
            'ctx': ctx,
            'bot': self.bot,
            '__import__': __import__           # Your variables go here
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))

        await ctx.message.add_reaction(self.bot.e.check)
        await ctx.send(result)

    @commands.command()
    @is_staff()
    async def pull(self, ctx: commands.Context):
        """Pulls latest code from GitHub"""

        os.system("git pull")
        await ctx.message.add_reaction(self.bot.e.check)

    @commands.command()
    @is_staff()
    async def restart(self, ctx: commands.Context):
        """Restarts the bot instance"""

        await ctx.message.add_reaction(self.bot.e.check)
        os.system("pm2 restart Hermes")


def setup(bot):
    bot.add_cog(Owner(bot))
