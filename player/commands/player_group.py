from discord.ext import commands

class PlayerGroup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="player", invoke_without_command=True)
    async def player_group(self, ctx, *, arg: str = None):
        """Player-related commands (lookup, last, best, avg, etc)."""
        if arg is None:
            await ctx.send("Use `!help player` to see all available subcommands.")
            return
        
        cmd = self.bet.get_command("player lookup")
        if cmd:
            await ctx.invoke(cmd, player_name=arg)
        else:
            await ctx.send("Lookup command not available.")

async def setup(bot):
    await bot.add_cog(PlayerGroup(bot))