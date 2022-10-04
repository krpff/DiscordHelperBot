import json
import os
import platform
import random
import sys
from datetime import datetime, timedelta

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


class Logs(commands.Cog, name="logs-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="getlist",
        description="Get list",
    )
    @checks.not_blacklisted()
    async def getlist(self, context: Context, date: str) -> None:
        embed = disnake.Embed(color=0x9C84EF, type="article")
        channel = context.channel
        day = datetime.strptime(date, "%d/%m/%y")
        count_messages = 0
        day = day.replace(tzinfo=None)
        reaction_logs = {}
        async for message in channel.history(before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if message.reactions:
                    for reaction in message.reactions:
                        async for user in reaction.users():
                            print(user, user.id)
                            if int(user.id) in reaction_logs.keys():
                                reaction_logs[int(user.id)] += 1
                            else:
                                reaction_logs[int(user.id)] = 1
                count_messages += 1
            else:
                break


            print(reaction_logs)
        embed.set_author(name="TEST")
        embed.add_field(name=f"Messages at {date}", value=f"{count_messages}", inline=True)
        out = ""
        for unit in reaction_logs.items():
            out += f"<@{unit[0]}> - **{unit[1]}**\n"
        embed.add_field(name=f"Statistics", value=out, inline=True)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))
