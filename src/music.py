import re
import discord
import asyncio
import youtube_dl
import http.client
from discord import Embed
from discord.ext import commands

class Song():
    def __init__(self):
        self.url = None
        self.title = None
        self.thumbnail = None

class Youtube():
    def __init__(self):
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}

    def create_youtubde_dl_player(self):
        return youtube_dl.YoutubeDL(self.YDL_OPTIONS)

    def fetch_music_url(self, url: str) -> str:
        connection = http.client.HTTPSConnection('www.youtube.com')
        '''
        if ' ' in url:
            url = url.replace(' ', '+')
        '''
        connection.request('GET', f'/results?search_query={url.replace(" ", "+") if " " in url else url}')
        response = connection.getresponse()
        body = response.read()
        urls = re.findall(r'watch\?v=(\S{11})', body.decode())
        return urls[0]

    def extract_audio_info(self, url: str) -> [str, str, str]:
        ytdl = self.create_youtubde_dl_player()
        info = ytdl.extract_info(url, download=False)
        return [info['formats'][0]['url'], info['title'], info['thumbnail']]

class MusicEmbed():
    def __init__(self):
        self.embed = discord.Embed()

    def destroy_embed(self):
        self.embed.clear_fields()

    def add_embed_fields(self, title: str, author: str, thumbnail: str) -> discord.Embed:
        self.embed.add_field(name="Playing 🎵", value=f'{title}')
        self.embed.add_field(name="Requested by", value=f"{author}")
        self.embed.set_thumbnail(url=thumbnail)
        return self.embed

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song = Song()
        self.youtube = Youtube()
        self.queue = {}
        self.current_song = None
        self.music_embed = MusicEmbed()
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    ######################################################## HELPER FUNCTIONS ################################################################
    ''' Plays the next song in queue. '''
    def play_next_song(self, ctx):
        try:
            if len(self.queue[ctx.guild.name]) == 0:
                return
        except Exception as e:
            pass
        
        if ctx.guild.name in self.queue:
            asyncio.run_coroutine_threadsafe(self.play_song(self.queue[ctx.guild.name].pop(0), ctx), self.bot.loop)
    
    ''' Fetches the url and plays the song. ''' 
    async def play_song(self, url, ctx):
        ctx.voice_client.stop()
        music_url = self.youtube.fetch_music_url(url)
        self.song.url, self.song.title, self.song.thumbnail = self.youtube.extract_audio_info(music_url)
        audio_source = await discord.FFmpegOpusAudio.from_probe(self.song.url, **self.FFMPEG_OPTIONS)
        if audio_source:
            music_embed = Embed()
            music_embed.add_field(name="Playing 🎵", value=f'{self.song.title}')
            music_embed.add_field(name="Requested by", value=f"{ctx.message.author}")
            music_embed.set_thumbnail(url=self.song.thumbnail)
            await ctx.channel.send(embed=music_embed)
            self.music_embed.destroy_embed()
            ctx.voice_client.play(audio_source, after=lambda e: self.play_next_song(ctx))
    
    ######################################################## COMMANDS ########################################################################
    ''' Pauses the currently playing song'''
    @commands.command(aliases=['pau', 'paus', 'stop', 'pa'], pass_context=True)
    async def pause(self, ctx):
        await ctx.channel.send("PAUSED ⏸")
        ctx.voice_client.pause()

    ''' Resumes the currently paused song'''
    @commands.command(aliases=['r', 'res', 'resum', 'resu'], pass_context=True)
    async def resume(self, ctx):
        await ctx.channel.send("RESUMED ⏯")
        ctx.voice_client.resume()

    ''' Removes the bot from voice channel '''
    @commands.command(aliases=['lea', 'leav'], pass_context=True)
    async def leave(self, ctx):
        del self.queue[ctx.guild.name]
        await ctx.voice_client.disconnect()
    
    ''' Adds song into the queue. '''
    @commands.command(aliases=['q', 'que'], pass_context=True)
    async def queue(self, ctx, *, song):
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            if len(self.queue[ctx.guild.name]) == 0:
                self.queue[ctx.guild.name] = [song]
            else:
                self.queue[ctx.guild.name].append(song)
            await ctx.channel.send(f"_{song}_ added to the queue.")
        else:
            await ctx.channel.send('Play a fucking music before queuing retard.')
    
    ''' 
    List all music in queue 
    TODO: Create an embed to send queued items.
    '''
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx):
        if len(self.queue[ctx.guild.name]) == 0:
            await ctx.channel.send('No songs in queue')
        
        for idx, songs in enumerate(self.queue[ctx.guild.name]):
            await ctx.channel.send(f'{idx + 1}. {songs}\n')
    
    @commands.command(name='debug', pass_context=True)
    async def debug(self, ctx):
        print(self.queue)
        
    ''' Clears the queue. '''
    @commands.command(aliases=['f', 'fl', 'fq', 'flushq', 'flushqueue'], pass_context=True)
    async def flush(self, ctx):
        if len(self.queue[ctx.guild.name]) == 0:
            await ctx.channel.send('No songs in queue.')
        self.queue[ctx.guild.name].clear()
    
    ''' Skips to the next song '''
    @commands.command(aliases=['s', 'sk', 'ski'], pass_context=True)
    async def skip(self, ctx):
        if len(self.queue[ctx.guild.name]) > 0:
            ctx.voice_client.stop()
            await self.play_song(self.queue[ctx.guild.name].pop(0), ctx)
        else:
            await ctx.channel.send('No songs in queue to skip.')
          
    ''' Plays the music based on keyword '''    
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx, *, url):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            self.queue[ctx.guild.name] = []
            
        if len(self.queue[ctx.guild.name]) > 0:
            await ctx.channel.send(f"There are music in queues retard {ctx.message.author}.")
        else:
            await self.play_song(url, ctx)
            
def setup(bot):
    bot.add_cog(Music(bot))

