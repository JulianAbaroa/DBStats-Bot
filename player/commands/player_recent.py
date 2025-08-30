from player.commands.player_group import PlayerGroup
from player import player_embeds, player_views
from sqlite.query_loader import QueryLoader
from discord.ext import commands
import aiosqlite, traceback, sys
import paths

queries = QueryLoader("sqlite/player_queries/recent")

class PlayerRecent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @PlayerGroup.player_group.command(name="player_recent", parent="player")
    async def player_recent(self, ctx, player_name: str, num_matches: str = "5"):
        """
        Displays the recent matches for the specified player.
        Defaults to 5 matches if a number is not provided.
        """
        if num_matches.lower() == "all":
            n = 99999
        else:
            try:
                n = int(num_matches)
            except ValueError:
                await ctx.send(f"Invalid number of games: {num_matches}")
                return
            
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row

                recent_matches_sql = queries.get("player_recent_matches")
                async with db.execute(recent_matches_sql, (player_name, n)) as reader:
                    recent_matches = await reader.fetchall()
                
                if not recent_matches:
                    await ctx.send(f"No recent matches were found for '{player_name}'")
                    return
                
                all_embeds = player_embeds.create_player_recent_embeds(player_name, recent_matches)

                if not all_embeds:
                    await ctx.send("Could not build any embed for recent matches.")
                    return
                
                view = player_views.RecentPaginatorView(pages=all_embeds, all_matches_data=recent_matches)
                await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching recent matches.")

async def setup(bot):
    cog = PlayerRecent(bot)
    await bot.add_cog(cog)

    parent = bot.get_command("player")
    if parent is None:
        print("Warning: parent command 'player' not found. Make sure player_group is loaded before this extension.")
        return

    parent.add_command(cog.player_recent, name="recent")