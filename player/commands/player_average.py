from player.commands.player_group import PlayerGroup
from sqlite.query_loader import QueryLoader
from discord.ext import commands
from views import paginator_view
from player import player_embeds
import aiosqlite, traceback, sys
import paths

queries = QueryLoader("sqlite/player_queries/average")

class PlayerAverage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @PlayerGroup.player_group.command(name="avg", parent="player")
    async def player_average(self, ctx, player_name: str, num_matches: str = "5"):
        """
        Displays the player's average stats over their last `number` matches. 
        Defaults to 5 matches if number is not provided.
        """
        if num_matches.lower() == "all":
            n = 99999
        else:
            try:
                n = int(num_matches)
            except ValueError:
                await ctx.send(f"Invalid number of matches: {num_matches}")
                return
        
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row

                player_rating_sql = queries.get("player_avg_rating")
                async with db.execute(player_rating_sql, (player_name, )) as reader:
                    player_rating = await reader.fetchone()

                if not player_rating:
                    await ctx.send(f"I didn't find the requested data for '{player_name}'")
                    return
                
                data = {}
                match = dict(player_rating)
                data["rating"] = match

                subqueries = {
                    "combat": queries.get("player_avg_combat"),
                    "breakdown": queries.get("player_avg_breakdown"),
                    "rivalries": queries.get("player_avg_rivalries"),
                    "survivability": queries.get("player_avg_survivability"),
                    "choice": queries.get("player_avg_choice"),
                    "medals": queries.get("player_avg_medals"),
                    "penalties": queries.get("player_avg_penalties")
                }

                for name, sql in subqueries.items():
                    async with db.execute(sql, (player_name, )) as reader:
                        if name == "medals":
                            rows = await reader.fetchall()
                            data[name] = [dict(row) for row in rows] if rows else []
                        else:
                            row = await reader.fetchone()
                            data[name] = dict(row) if row else None

            all_embeds = [
                player_embeds.create_player_rating_embed(match, data.get("rating", {})),
                player_embeds.create_player_combat_embed(match, data.get("combat", {})),
                player_embeds.create_player_breakdown_embed(match, data.get("breakdown", {})),
                player_embeds.create_player_rivalries_embed(match, data.get("rivalries", {})),
                player_embeds.create_player_survivability_embed(match, data.get("survivability", {})),
                player_embeds.create_player_choice_embed(match, data.get("choice", {})),
                player_embeds.create_player_medals_embed(match, data.get("medals", {})),
                player_embeds.create_player_penalties_embed(match, data.get("penalties", {}))
            ]

            all_embeds = [embed for embed in all_embeds if embed is not None]

            if not all_embeds:
                await ctx.send("Could not build any embeds for the requested data.")
                return
                
            view = paginator_view.PaginatorView(pages=all_embeds)
            await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the average data.")

async def setup(bot):
    await bot.add_cog(PlayerAverage(bot))