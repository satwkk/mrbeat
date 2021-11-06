import re
import json
import random
import aiohttp
import asyncio
import discord
from src.youtube import Youtube
from discord.ext import commands

# CONSTANTS
CMD_PREFIX = "-"

class Bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

    def __init__(self):
        pass
    
    @staticmethod
    def parse_json():
        with open('config.json') as file_handle:
            cmds = json.load(file_handle)
        return cmds

    async def on_ready(self):
        print("Bot ready")

    @bot.command(name="hello")
    async def greet(ctx):
        greet = random.choice(Bot.parse_json()["greeting"])
        await ctx.channel.send(f"{greet} {ctx.message.author.mention}")

    @bot.command(name="users")
    async def get_users_count(ctx):
        await ctx.channel.send(f"Number of throwers in channel: {ctx.guild.member_count}")
    
    @bot.command(name="owner")
    async def get_guild_owner(ctx):
       await ctx.channel.send(f"Our king 👑 : {ctx.guild.owner.name}") 
    
    @bot.command(name="join")
    async def join(ctx):
        if ctx.author.voice is None:
            await ctx.send('Join a voice channel before running this command.')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            ctx.voice_client.move_to(voice_channel)

    @bot.command(name="leave")
    async def leave(ctx):
        await ctx.voice_client.disconnect()

    @bot.command(name="play")
    async def play_music(ctx, *, url):
        ctx.voice_client.stop()
        yt = Youtube()
        if url.startswith('http'):
            audio_source = await yt.extract_audio(url)    
            ctx.voice_client.play(audio_source)
        else:
            params = {'search_query': f'{url}'}
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.youtube.com/results", params=params) as response:
                    response = await response.text()
                found = re.findall(r'watch\?v=(\S{11})', response)
                final_url = f"https://www.youtube.com/watch?v={found[0]}"
                audio_source = await yt.extract_audio(final_url)
                ctx.voice_client.play(audio_source)

    @bot.command(name="pause")
    async def pause_music(ctx):
        ctx.voice_client.pause()
        await ctx.channel.send("PAUSED !!")
    
    @bot.command(name="resume")
    async def resume_music(ctx):
        ctx.voice_client.resume()
        await ctx.channel.send("RESUMING !!")

mybot = Bot()
