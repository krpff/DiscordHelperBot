import asyncio
import json
import os
import sys

import aiohttp
import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Lyceum(commands.Cog, name="template-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="randomcat",
        description="Send a random cat image.",
    )
    @checks.not_blacklisted()
    async def randomcat(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    await context.send(data[0]["url"])
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                    await context.send(embed=embed)

    @commands.command(
        name="timer",
        description="Set a timer for a specific amount of time.",
    )
    @checks.not_blacklisted()
    async def timer(self, context: Context, seconds):
        try:
            secondint = int(seconds)
            if secondint > 3600:
                await context.send("Maximum timer is 1 hour. Please try again.")
            if secondint <= 0:
                await context.send("Numbers must be above 0.")
            message = await context.send("*Timer: {seconds} seconds*")
            while True:
                secondint -= 1
                if secondint == 0:
                    break
                await message.edit(content=f"*Timer: {secondint} seconds*")
                await asyncio.sleep(1)
            await context.send(f"{context.author.mention} Your countdown Has ended!")
        except ValueError:
            await context.send("Must be a number!")


def setup(bot):
    bot.add_cog(Lyceum(bot))
