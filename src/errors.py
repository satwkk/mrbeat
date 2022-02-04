from discord.ext import commands
from discord import Embed

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            message = Embed(title="Available Commands (Use prefix '-')", color=0x71368a)
            message.add_field(name="Music Commands", value="**play** - Plays the song provided.\n**pause** - Pause the currently playing song.\n**resume** - Resumes the currently paused song.\n**queue** - Adds the song to queue.\n**listqueue** - Lists all songs in queue.\n**flush** - Clears the queue.\n**skip** - Skips the currently played song.")
            message.add_field(name="Server Stats", value="**totalmessages** - No. of messages in the text channel.\n**owner** - Owner of the server.\n**update** - Alert for new updates to the bot.")
            await ctx.channel.send(embed=message)

def setup(bot):
    bot.add_cog(ErrorHandling(bot))
