import re
import discord
import youtube_dl
import http.client
from discord.ext import commands

class Song():
    def __init__(self):
        self.url = None
        self.title = None
        self.thumbnail = None

    def get_url(self) -> str:
        return self.url
    
    def get_title(self) -> str:
        return self.title

    def get_thumbnail(self) -> str:
        return self.thumbnail

class Youtube():
    def __init__(self):
        self.YDL_OPTIONS = {'format': 'bestaudio'}

    def create_youtubde_dl_player(self):
        return youtube_dl.YoutubeDL(self.YDL_OPTIONS)

    def fetch_music_url(self, url: str) -> str:
        connection = http.client.HTTPSConnection('www.youtube.com')
        if ' ' in url:
            url = url.replace(' ', '+')
        connection.request('GET', f'/results?search_query={url}')
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
        self.music_embed = MusicEmbed()
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    ''' Pauses the currently playing song'''
    @commands.command(name='pause', pass_context=True)
    async def pause(self, ctx):
        await ctx.channel.send(f"PAUSED ⏸ : {self.song.get_title()}")
        ctx.voice_client.pause()

    ''' Resumes the currently paused song'''
    @commands.command(name='resume', pass_context=True)
    async def resume(self, ctx):
        await ctx.channel.send(f"RESUMED ⏯ : {self.song.get_title()}")
        ctx.voice_client.resume()

    ''' Removes the bot from voice channel '''
    @commands.command(name='leave', pass_context=True)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    ''' Plays the music based on keyword'''    
    @commands.command(name='play', pass_context=True)
    async def play(self, ctx, *, url):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        
        ''' Fetching the music url from youtube '''
        ctx.voice_client.stop()
        music_url = self.youtube.fetch_music_url(url)
        self.song.url, self.song.title, self.song.thumbnail = self.youtube.extract_audio_info(music_url)
        audio_source = await discord.FFmpegOpusAudio.from_probe(self.song.url, **self.FFMPEG_OPTIONS)

        ''' TODO: This might cause problems in future. Change it to regular embed maybe ?'''
        embed_msg = self.music_embed.add_embed_fields(self.song.get_title(), ctx.message.author, self.song.get_thumbnail())
        await ctx.channel.send(embed=embed_msg)
        self.music_embed.destroy_embed()

        ''' Creating an embed '''
        if audio_source:
            ctx.voice_client.play(audio_source)

def setup(bot):
    bot.add_cog(Music(bot))
