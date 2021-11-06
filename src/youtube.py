import re
import aiohttp
import asyncio

class Youtube():
    async def youtube_search(self, keyword):
        params = {'search_query': f'{keyword}'}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.youtube.com/results", params=params) as response:
                response = await response.text()
            found = re.findall(r'watch\?v=(\S{11})', response)
            return f"https://www.youtube.com/watch?v={found[0]}"
    
    def get_final_url(self, keyword):
        result = asyncio.get_event_loop()
        url = result.run_until_complete(self.youtube_search(keyword))
        return url


yt = Youtube()
