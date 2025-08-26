from discord.ext import commands

class DBStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="dbstats", invoke_without_command=True)
    async def dbstats_group(self, ctx, *, arg: str = None):
        if arg is None:
            await ctx.send("GIVE ME DATAAAA")
            return
        
        await ctx.send("No.")

async def setup(bot):
    await bot.add_cog(DBStats(bot))