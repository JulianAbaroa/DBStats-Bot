from help_cog import HelpCog
from discord.ext import commands
import asyncio
import discord
import bridge
import os

TOKEN = os.getenv("DBSTATS_TOKEN")
if TOKEN is None:
    raise ValueError("The DBSTATS_TOKEN environment variable is not defined")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.help_command = None

@bot.event
async def on_ready():
    print(f'Bot started as {bot.user}')
    bot.loop.create_task(process_history())

async def process_history():
    try:
        await bridge.check_channel_history_and_process(bot, limit=None)
        print("History check and DBStats processing completed.")
    except Exception as e:
        print("Failed to process history:", e)

@bot.event
async def on_message(message):
    await bridge.handle_message(bot, message)    
    await bot.process_commands(message)

async def setup_extensions():
    await bot.load_extension("dbstats.dbstats_commands")
    await bot.load_extension("player.player_commands")
    await bot.load_extension("match.match_commands")
    await bot.load_extension("help_cog")

if __name__ == "__main__":
    asyncio.run(setup_extensions())
    bot.run(TOKEN)