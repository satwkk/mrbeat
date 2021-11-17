from discord.ext import commands
from discord import Embed

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def owner(self, ctx):
       await ctx.channel.send(f"Our king 👑 : {ctx.guild.owner.name}") 

    @commands.command(name="users", pass_context=True)
    async def get_member_count(self, ctx):
        await ctx.channel.send(f"Number of throwers {ctx.guild.member_count}")
    
    @commands.command(name="totalmessages", pass_context=True)
    async def message_count(self, ctx):
        count = 0
        async for _ in ctx.channel.history(limit=None):
            count += 1
        await ctx.send(f"There are {count} messages in {ctx.channel.mention}")

def setup(bot):
    bot.add_cog(Stats(bot))
