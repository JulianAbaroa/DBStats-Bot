from sqlite.query_loader import QueryLoader
from player import player_views
from player import player_embeds
from discord.ext import commands
import aiosqlite
import paths
import traceback
import sys

queries = QueryLoader()

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="player", invoke_without_command=True)
    async def player_group(self, ctx, *, arg: str = None):
        """Player-related commands (lookup, last, best, avg, etc)."""
        if arg is None:
            await ctx.send("Use `!help player` to see all available subcommands.")
            return

        await ctx.invoke(self.lookup, player_name=arg)

    @player_group.command(name="lookup")
    async def lookup(self, ctx, *, player_name: str):
        """Shows the player's profile and customization."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                query = queries.get("player_profile")
                async with db.execute(query, (player_name,)) as cursor:
                    player_data = await cursor.fetchone()

            if not player_data:
                await ctx.send(f"I didn't find the player '{player_name}'")
                return

            embed, files_to_send = player_embeds.create_player_embed(player_data)
            if files_to_send:
                await ctx.send(files=files_to_send, embed=embed)
            else:
                await ctx.send(embed=embed)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while looking up the player. Check the bot logs.")

    @player_group.command(name="last")
    async def last(self, ctx, *, player_name: str):
        """Shows the last saved match for the specified player."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                query = queries.get("player_last_match")
                async with db.execute(query, (player_name,)) as cursor:
                    player_match = await cursor.fetchone()

                if not player_match:
                    await ctx.send(f"I didn't find any games for '{player_name}'")
                    return

                subqueries = {
                    "team": queries.get("player_last_team"),
                    "rating": queries.get("player_last_rating"),
                    "combat": queries.get("player_last_combat"),
                    "breakdown": queries.get("player_last_breakdown"),
                    "rivalries": queries.get("player_last_rivalries"),
                    "survivability": queries.get("player_last_survivability"),
                    "choice": queries.get("player_last_choice"),
                    "medals": queries.get("player_last_medals"),
                    "penalties": queries.get("player_last_penalties"),
                }
                data = {}
                for name, query in subqueries.items():
                    async with db.execute(query, (player_match["player_name"],)) as cursor:
                        if name == "medals":
                            rows = await cursor.fetchall()
                            data[name] = [dict(row) for row in rows]
                        else:
                            row = await cursor.fetchone()
                            data[name] = dict(row) if row else None
            
            all_embeds = [
                player_embeds.create_player_match_embed(player_match),
                player_embeds.create_player_team_embed(player_match, data.get("team", {})),
                player_embeds.create_player_rating_embed(player_match, data.get("rating", {})),
                player_embeds.create_player_combat_embed(player_match, data.get("combat", {})),
                player_embeds.create_player_breakdown_embed(player_match, data.get("breakdown", {})),
                player_embeds.create_player_rivalries_embed(player_match, data.get("rivalries", {})),
                player_embeds.create_player_survivability_embed(player_match, data.get("survivability", {})),
                player_embeds.create_player_choice_embed(player_match, data.get("choice", {})),
                player_embeds.create_player_medals_embed(player_match, data.get("medals", {})),
                player_embeds.create_player_penalties_embed(player_match, data.get("penalties", {})),
            ]
            
            # Filtrar los embeds que no se pudieron construir
            all_embeds = [embed for embed in all_embeds if embed is not None]

            if not all_embeds:
                await ctx.send("Could not build any embeds for the last match. Check logs.")
                return

            view = player_views.MatchPaginatorView(pages=all_embeds)
            await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the last match. Check the bot logs.")
    
    @player_group.command(name="best")
    async def best(self, ctx, *, player_name: str):
        """Shows the best saved match in terms of rating for the specified player."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                query = queries.get("player_best_match")
                async with db.execute(query, (player_name,)) as cursor:
                    player_match = await cursor.fetchone()

                if not player_match:
                    await ctx.send(f"I didn't find any games for '{player_name}'")
                    return

                subqueries = {
                    "team": queries.get("player_best_team"),
                    "rating": queries.get("player_best_rating"),
                    "combat": queries.get("player_best_combat"),
                    "breakdown": queries.get("player_best_breakdown"),
                    "rivalries": queries.get("player_best_rivalries"),
                    "survivability": queries.get("player_best_survivability"),
                    "choice": queries.get("player_best_choice"),
                    "medals": queries.get("player_best_medals"),
                    "penalties": queries.get("player_best_penalties"),
                }
                data = {}
                for name, query in subqueries.items():
                    async with db.execute(query, (player_match["player_name"],)) as cursor:
                        if name == "medals":
                            rows = await cursor.fetchall()
                            data[name] = [dict(row) for row in rows]
                        else:
                            row = await cursor.fetchone()
                            data[name] = dict(row) if row else None
            
            all_embeds = [
                player_embeds.create_player_match_embed(player_match),
                player_embeds.create_player_team_embed(player_match, data.get("team", {})),
                player_embeds.create_player_rating_embed(player_match, data.get("rating", {})),
                player_embeds.create_player_combat_embed(player_match, data.get("combat", {})),
                player_embeds.create_player_breakdown_embed(player_match, data.get("breakdown", {})),
                player_embeds.create_player_rivalries_embed(player_match, data.get("rivalries", {})),
                player_embeds.create_player_survivability_embed(player_match, data.get("survivability", {})),
                player_embeds.create_player_choice_embed(player_match, data.get("choice", {})),
                player_embeds.create_player_medals_embed(player_match, data.get("medals", {})),
                player_embeds.create_player_penalties_embed(player_match, data.get("penalties", {})),
            ]
            
            all_embeds = [embed for embed in all_embeds if embed is not None]

            if not all_embeds:
                await ctx.send("Could not build any embeds for the last match. Check logs.")
                return

            view = player_views.MatchPaginatorView(pages=all_embeds)
            await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the last match. Check the bot logs.")

    @player_group.command(name="avg")
    async def avg(self, ctx, player_name: str, num_matches: str = "5"):
        """
        Shows the player's average stats over their last `number` matches. 
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

                rating_query = queries.get("player_stats_rating")
                async with db.execute(rating_query, (player_name, n)) as cursor:
                    rating_row = await cursor.fetchone()

                if not rating_row:
                    await ctx.send(f"I didn't find any games for '{player_name}'")
                    return

                data = {}
                player_match = dict(rating_row)
                data["rating"] = player_match

                subqueries = {
                    "combat": queries.get("player_stats_combat"),
                    "breakdown": queries.get("player_stats_breakdown"),
                    "rivalries": queries.get("player_stats_rivalries"),
                    "survivability": queries.get("player_stats_survivability"),
                    "choice": queries.get("player_stats_choice"),
                    "medals": queries.get("player_stats_medals"),
                    "penalties": queries.get("player_stats_penalties"),
                }

                for name, query in subqueries.items():
                    async with db.execute(query, (player_name, n)) as cursor:
                        if name == "medals":
                            rows = await cursor.fetchall()
                            data[name] = [dict(row) for row in rows] if rows else []
                        else:
                            row = await cursor.fetchone()
                            data[name] = dict(row) if row else None

            all_embeds = [
                player_embeds.create_player_rating_embed(player_match, data.get("rating", {})),
                player_embeds.create_player_combat_embed(player_match, data.get("combat", {})),
                player_embeds.create_player_breakdown_embed(player_match, data.get("breakdown", {})),
                player_embeds.create_player_rivalries_embed(player_match, data.get("rivalries", {})),
                player_embeds.create_player_survivability_embed(player_match, data.get("survivability", {})),
                player_embeds.create_player_choice_embed(player_match, data.get("choice", {})),
                player_embeds.create_player_medals_embed(player_match, data.get("medals", {})),
                player_embeds.create_player_penalties_embed(player_match, data.get("penalties", {})),
            ]

            all_embeds = [embed for embed in all_embeds if embed is not None]

            if not all_embeds:
                await ctx.send("Could not build any embeds for the requested matches. Check logs.")
                return

            view = player_views.MatchPaginatorView(pages=all_embeds)
            await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the stats. Check the bot logs.")

    @player_group.command(name="recent")
    async def recent(self, ctx, player_name: str, num_matches: str = "5"):
        """
        Shows the recent matches for the specified player.
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
                recent_matches_query = queries.get("player_recent_matches")
                
                async with db.execute(recent_matches_query, (player_name, n)) as cursor:
                    matches_data = await cursor.fetchall()

                if not matches_data:
                    await ctx.send(f"No games were found for '{player_name}'")
                    return
                
                all_embeds = player_embeds.create_player_recent_embeds(player_name, matches_data)

                if not all_embeds:
                    await ctx.send("Could not build any embed for recent games.")
                    return

                view = player_views.MatchPaginatorView(pages=all_embeds)
                
                await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching recent games. Please check the bot logs.")

async def setup(bot):
    await bot.add_cog(Player(bot))