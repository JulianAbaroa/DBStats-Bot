from sqlite.query_loader import QueryLoader
from views import paginator_view
from discord.ext import commands
from dbstats import dbstats_embeds
import aiosqlite
import traceback
import paths
import sys

queries = QueryLoader("sqlite/dbstats queries")

class DBStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="dbstats", invoke_without_command=True)
    async def dbstats_group(self, ctx, *, arg: str = None):
        """Dbstats-related commands (none)"""
        if arg is None:
            await ctx.send("GIVE ME DATAAAA")
            return
        
        await ctx.send("No.")

    @dbstats_group.command(name="betrayers")
    async def betrayers(self, ctx):
        """Displays the top betrayers saved on the data base."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                betrayers = queries.get("betrayers")
                async with db.execute(betrayers) as cursor:
                    betrayers_data = await cursor.fetchall()

            if not betrayers_data:
                await ctx.send(f"I didn't find any betrayer.")
                return
            
            pages = dbstats_embeds.create_betrayers_embed(betrayers_data)

            if not pages:
                await ctx.send("Could not build betrayers embed. Check logs.")
                return
            
            view = paginator_view.PaginatorView(pages)     
            await ctx.send(embed=pages, view=view)  

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching betrayers. Check logs.")


async def setup(bot):
    await bot.add_cog(DBStats(bot))