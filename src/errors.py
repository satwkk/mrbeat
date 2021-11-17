from discord.ext import commands
from discord import Embed

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            message = Embed(color=0x71368a)
            message.add_field(name="Available Commands", value="-user => Number of users in the channel\n-owner => Owner of the channel\n-totalmessages => Number of messages sent in respective text channel\n-play => Joins voice channel and plays song from url or keyword\n-pause => Pause the song\n-resume => Resume the song")

            await ctx.channel.send(embed=message)

def setup(bot):
    bot.add_cog(ErrorHandling(bot))
