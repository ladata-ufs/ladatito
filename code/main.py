import discord
import os
from discord.ext import commands
import re

from dotenv import load_dotenv

from GeminiRAG import GenerateLADATITO

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)
RAG = GenerateLADATITO()

def clean_discord_message(input_string):
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    

@bot.event
async def on_message(message):
    if message.author == bot.user or message.mention_everyone:
        return
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):

        clean_message = clean_discord_message(message.content)
        
        async with message.channel.typing():

            print("New Message FROM:" + str(message.author.id) + ": " + clean_message)
            
            if "LADATA" in clean_message.upper():
                await message.add_reaction("<:polvin:1222249667824320562>")

                response_text = RAG.respond_query(clean_message)
                await message.channel.send(response_text)
            else:
                await message.add_reaction('💬')

                response_text = RAG.respond_general_query(clean_message)
                await message.channel.send(response_text)


bot.run(token=DISCORD_BOT_TOKEN)
