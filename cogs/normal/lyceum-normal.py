import asyncio
import json
import os
import sys

import aiohttp
import disnake
import requests
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

    @commands.command(
        name="translate",
        description="Translates words from English language to target.",
    )
    @checks.not_blacklisted()
    async def translate(self, context: Context, text: str, target_language: str):
        res = requests.post(
            "http://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": f"en|{target_language}",
                "target": target_language,
            },
        ).json()
        res = res["matches"][0]["translation"]
        await context.send(
            f'**"{text.capitalize()}"** translation to __{target_language}__: **"{res}"**'
        )

    @commands.command(
        name="wr",
        description="Get weather info by OpenWeatherMap.",
    )
    @checks.not_blacklisted()
    async def wr(self, context: Context, city: str):
        res = requests.post(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": config["openweathermap_api_key"],
            },
        ).json()
        print(res)

        if str(res["cod"]) == "404":
            await context.send("**City not found.**")
        elif str(res["cod"]) == "200":
            embed = disnake.Embed(color=0x9C84EF)
            embed.set_author(
                name=f"Weather in {res['name']}",
            )
            embed.add_field(
                name=":cloud: Weather",
                value=f"{res['weather'][0]['main']}",
                inline=False,
            )
            embed.add_field(
                name=":thermometer: Temperature",
                value=f"**{res['main']['temp']}°C**\n"
                f"*Feels like {res['main']['feels_like']}°C*",
                inline=False,
            )
            embed.add_field(
                name=":cloud_tornado: Wind",
                value=f"**Speed {res['wind']['speed']} m/s**\n"
                f"**Direction {res['wind']['deg']}°**\n"
                f"*Gusts {res['wind']['gust']} m/s*",
                inline=False,
            )
            embed.set_footer(text=f"Requested by {context.author}")
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Lyceum(bot))
