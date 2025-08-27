from match import match_embeds 
from discord.ext import commands
import aiosqlite
import paths

class Match(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="match", invoke_without_command=True)
    async def match_group(self, ctx):   
        """Match-related commands (last, etc)."""
        await ctx.send("Use `!help match` to see all available subcommands.")
    
    @match_group.command(name="last")
    async def last_match(self, ctx):
        """!match last -> Shows the last saved match."""
        async with aiosqlite.connect(paths.DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
    
            cursor = await db.execute("SELECT * FROM Matches ORDER BY match_timestamp DESC LIMIT 1")
            match_data = await cursor.fetchone()
    
            if not match_data:
                await ctx.send("There are no registered games.")
                return
            
            cursor = await db.execute(
                "SELECT * FROM Teams WHERE match_id = ?", 
                (match_data["match_id"],)
            )
    
            teams_data = await cursor.fetchall()
    
            embed = match_embeds.create_match_embed(match_data, teams_data)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Match(bot))