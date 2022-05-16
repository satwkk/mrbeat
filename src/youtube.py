import pafy
import http.client
import re
import youtube_dl

class Youtube():
    def __init__(self):
        self.streaming_url = 'www.youtube.com'
        self.conn = http.client.HTTPSConnection(self.streaming_url)

    def get_music_id(self, url: str) -> str:
        self.conn.request('GET', f'/results?search_query={url.replace(" ", "+") if " " in url else url}')
        body = self.conn.getresponse().read()
        urls = re.findall(r'watch\?v=(\S{11})', body.decode())
        self.conn.close()
        return urls[0]
    
    def get_best_audio(self, music_url):
        stream = music_url.getbestaudio()
        if stream is None:
            stream = music_url.audiostreams
            return stream[-1] # return the last best audio stream
        return stream
    
    def fetch_music_data(self, url: str):
        music_id = self.get_music_id(url)
        music = pafy.new(f"https://www.youtube.com/watch/?v={music_id}")
        stream = self.get_best_audio(music)
        if music.bigthumb is None:
            return [stream, stream.url_https, music.title, music.thumb]
        return [stream, stream.url_https, music.title, music.bigthumb]
        