import re
import aiohttp
from youtube import Youtube
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", pass_context=True)
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('Join a voice channel before running this command.')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            # await ctx.voice_client.move_to(voice_channel)
            await ctx.channel.send('Already in a voice channel')
    
    @commands.command(name="leave", pass_context=True)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command(name="play", pass_context=True)
    async def play_music(self, ctx, *, url):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            
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
    
    @commands.command(name="pause", pass_context=True)
    async def pause_music(self, ctx):
        ctx.voice_client.pause()
        await ctx.channel.send("PAUSED !!")
    
    @commands.command(name="resume", pass_context=True)
    async def resume_music(self, ctx):
        ctx.voice_client.resume()
        await ctx.channel.send("RESUMING !!")
    
def setup(bot):
    bot.add_cog(Music(bot))
