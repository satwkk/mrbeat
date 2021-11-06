import re
import aiohttp
import asyncio
import discord
import youtube_dl

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio'}

class Youtube():
    def __init__(self):
        pass

    async def extract_audio(self, url):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            music_url = info['formats'][0]['url']
            audio_source = await discord.FFmpegOpusAudio.from_probe(music_url, **FFMPEG_OPTIONS)
        return audio_source

