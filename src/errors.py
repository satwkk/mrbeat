from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        message = ""
        if isinstance(error, commands.CommandNotFound):
            message = f"{ctx.message.content} command not found."

        await ctx.channel.send(message)

def setup(bot):
    bot.add_cog(ErrorHandling(bot))
