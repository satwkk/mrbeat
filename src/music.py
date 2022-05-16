import discord
from discord import Embed
from src.youtube import Youtube
from src.logger import Logger
from discord.ext import commands

class Song():
    def __init__(self):
        self.url = None
        self.title = None
        self.thumbnail = None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song = Song()
        self.youtube = Youtube()
        self.queue = {}
        self.logger = Logger()
        self.current_song = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    ######################################################## HELPER FUNCTIONS ################################################################
    def get_queue(self, ctx):
        return self.queue[ctx.guild.name]

    def is_queue_empty(self, ctx):
        if len(self.get_queue(ctx)) == 0:
            return True
        else:
            return False

    async def play_next_song(self, ctx):
        try:
            if len(self.queue[ctx.guild.name]) == 0:
                return
        except Exception as e:
            pass
        
        if ctx.guild.name in self.queue:
            await self.play_song(self.queue[ctx.guild.name][0], ctx)
            self.queue[ctx.guild.name].pop(0)
    
    async def play_song(self, url, ctx):
        ctx.voice_client.stop()
        stream_quality, self.song.url, self.song.title, self.song.thumbnail = self.youtube.fetch_music_data(url)
        audio_source = await discord.FFmpegOpusAudio.from_probe(self.song.url, **self.FFMPEG_OPTIONS)
        if audio_source:
            music_embed = Embed(title="Playing 🎵", colour=0x3498db)
            music_embed.add_field(name=f"{self.song.title}", value='\u200b')
            music_embed.set_image(url=self.song.thumbnail)
            self.logger.log(f"Playing song {self.song.title} at quality {stream_quality}.")
            await ctx.channel.send(embed=music_embed)
            ctx.voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
        
    ######################################################## COMMANDS ########################################################################
    ''' Pauses the currently playing song'''
    @commands.command(aliases=['pau', 'paus', 'stop', 'pa'], pass_context=True)
    async def pause(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')
           
        await ctx.channel.send("PAUSED ⏸")
        ctx.voice_client.pause()

    ''' Resumes the currently paused song'''
    @commands.command(aliases=['r', 'res', 'resum', 'resu'], pass_context=True)
    async def resume(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')
           
        await ctx.channel.send("RESUMED ⏯")
        ctx.voice_client.resume()

    ''' Removes the bot from voice channel '''
    @commands.command(aliases=['lea', 'leav'], pass_context=True)
    async def leave(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')
           
        del self.queue[ctx.guild.name]
        await ctx.voice_client.disconnect()
    
    @commands.command(aliases=['q', 'que'], pass_context=True)
    async def queue(self, ctx, *, song):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')
           
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            if self.is_queue_empty(ctx):
                self.queue[ctx.guild.name] = [song]
            else:
                self.queue[ctx.guild.name].append(song)
            await ctx.channel.send(f"_{song}_ added to the queue.")
        else:
            await ctx.channel.send('Play a fucking music before queuing retard.')
    
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx):
        if self.is_queue_empty(ctx):
            return await ctx.channel.send('No songs in queue')
        
        embed = Embed(title="Queued Songs")
        for idx, songs in enumerate(self.queue[ctx.guild.name]):
            embed.add_field(name="\u200b", value=f"**{idx + 1}. {songs}**", inline=False)
        await ctx.channel.send(embed=embed)
        
    @commands.command(name='debug', pass_context=True)
    @commands.has_role('Developer')
    async def debug(self, ctx):
        print(self.queue)
        
    @commands.command(aliases=['f', 'fl', 'fq', 'flushq', 'flushqueue'], pass_context=True)
    async def flush(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')
           
        if self.is_queue_empty(ctx):
            await ctx.channel.send('No songs in queue.')
        self.queue[ctx.guild.name].clear()
    
    @commands.command(aliases=['s', 'sk', 'ski'], pass_context=True)
    async def skip(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')

        if not self.is_queue_empty(ctx):
            ctx.voice_client.stop()
        else:
            await ctx.channel.send('No songs in queue to skip.')
          
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx, *, url):
        if ctx.message.author.voice is None:
            return await ctx.channel.send('Stop disturbing others dumbo, join a voice channel if you want to listen music.')

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            self.queue[ctx.guild.name] = []
            
        if not self.is_queue_empty(ctx):
            await ctx.channel.send(f"There are music in queues retard.")
        else:
            await self.play_song(url, ctx)
            
def setup(bot):
    bot.add_cog(Music(bot))
