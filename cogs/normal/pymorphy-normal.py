import pymorphy2
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


class Pymorphy(commands.Cog, name="pymorphy-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="morph_commands",
        description="Send a list of commands for the morph module.",
    )
    @checks.not_blacklisted()
    async def morph_commands(self, context: Context) -> None:
        embed = disnake.Embed(color=0x9C84EF)
        embed.set_author(
            name="Pymorphy2 commands",
        )
        embed.add_field(
            name="numerals",
            value="Coordinate the word and the numeral \n" "[word] [numeral]",
            inline=False,
        )
        embed.add_field(
            name="alive", value="Definition of animate and inanimate", inline=False
        )
        embed.add_field(
            name="inf", value="Definition of the initial form", inline=False
        )
        embed.add_field(name="morph", value="Full morphological analysis", inline=False)
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.command(
        name="numerals",
        description="Coordinate the word and the numeral",
    )
    @checks.not_blacklisted()
    async def numerals(self, context: Context, word, numeral):
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(word)[0]
        result = f"{numeral} {parsed_word.make_agree_with_number(int(numeral)).word}"
        await context.send(result)

    @commands.command(
        name="alive",
        description="Definition of the initial form",
    )
    @checks.not_blacklisted()
    async def inf(self, context: Context, word):
        morph = pymorphy2.MorphAnalyzer()
        if morph.parse(word)[0].tag.POS == "NOUN":
            if morph.parse(word)[0].tag.animacy == "anim":
                await context.send(f"**{word.capitalize()}** is alive")
            else:
                await context.send(f"**{word.capitalize()}** is not alive")
        else:
            await context.send(f"**{word.capitalize()}** is not a noun")

    @commands.command(
        name="inf",
        description="Definition of animate and inanimate",
    )
    @checks.not_blacklisted()
    async def alive(self, context: Context, word):
        morph = pymorphy2.MorphAnalyzer()
        await context.send(f'Infinitive of {word} is **{str(morph.parse(word)[0].normal_form)}**')

    @commands.command(
        name="morph",
        description="Full morphological analysis",
    )
    @checks.not_blacklisted()
    async def morph(self, context: Context, word):
        morph = pymorphy2.MorphAnalyzer()
        await context.send(f'{morph.parse(word)[0]}'
                           f'\n\n ||Мне лень это парсить, но ведь анализ то делает||')


def setup(bot):
    bot.add_cog(Pymorphy(bot))
