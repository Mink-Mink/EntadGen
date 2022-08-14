import json
from entadGen import sampleEntad
from constants import *
from fileLoading import *
import discord
from discord import app_commands
from discord.ext import commands

formatWordDictionary()
wordDictionary = loadWordDictionary()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="?",
    description="Bot used for generating ideas for custom magic item creation",
    intents=intents,
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.tree.command(name="entad", description="generates a new entad")
async def entad(interaction: discord.Interaction):
    await interaction.response.send_message(sampleEntad(wordDictionary))


if __name__ == "__main__":
    with open(DISCORD_KEY_FILE) as keyFile:
        discordKey = json.load(keyFile)[DISCORD_API_KEY]
    bot.run(discordKey)
