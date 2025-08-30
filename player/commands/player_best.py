from player.commands.player_group import PlayerGroup
from sqlite.query_loader import QueryLoader
from dictionaries import gametypes
from discord.ext import commands
from views import paginator_view
from player import player_embeds
import aiosqlite, traceback, sys
import paths

queries = QueryLoader("sqlite/player_queries/best")

class PlayerBest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @PlayerGroup.player_group.command(name="player_best", parent="player")
    async def player_best(self, ctx, *, player_name: str):
        """Displays the best saved match in terms of rating for the specified player."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row

                player_best = queries.get("player_best_match")

                async with db.execute(player_best, (player_name, )) as reader:
                    match = await reader.fetchone()

                if not match:
                    await ctx.send(f"I didn't find a best match of '{player_name}'")
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
                    "penalties": queries.get("player_best_penalties")
                }   

                gametype_to_query = {
                    "slayer": "player_best_slayer",
                    "capturetheflag": "player_best_ctf",
                    "oddball": "player_best_oddball",
                    "kingofthehill": "player_best_koth",
                    "juggernaut": "player_best_juggernaut",
                    "infection": "player_best_infection",
                    "territories": "player_best_territories",
                    "assault": "player_best_assault",
                    "stockpile": "player_best_stockpile",
                    "headhunter": "player_best_headhunter",
                    "actionsack": "player_best_actionsack"
                }

                # Saved in DB as integer (0 = Slayer, 1 = CTF, ...) 
                gametype = match["gametype"]
                gametype_name = gametypes.id_to_gametype.get(gametype)
                gametype_query = gametype_to_query.get(gametype_name)   

                if gametype_query:
                    subqueries["gametype"] = queries.get(gametype_query)
                else:
                    subqueries["gametype"] = None

                data = {}
                for name, sql in subqueries.items():
                    if not sql:
                        data[name] = None
                        continue
                    
                    params = None

                    if name == "gametype":
                        player_match_id = match["player_match_id"]

                        if player_match_id:
                            params = (player_match_id, )
                    else:
                        params = (match["player_name"], )

                    if params:
                        async with db.execute(sql, params) as reader:
                            # Logic for medals
                            if name == "medals":
                                rows = await reader.fetchall()
                                data[name] = [dict(row) for row in rows]
                            # Logic for everything else
                            else:
                                row = await reader.fetchone()
                                data[name] = dict(row) if row else None
                    else:
                        data[name] = None
                        
            all_embeds = [
                player_embeds.create_player_match_embed(match),
                player_embeds.create_player_team_embed(match, data.get("team", {})),
                player_embeds.create_player_rating_embed(match, data.get("rating", {})),
                player_embeds.create_player_gametype_embed(dict(match), data.get("gametype", {})),
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
                await ctx.send("I couldn't build any embeds for the best match.")
                return
            
            view = paginator_view.PaginatorView(pages=all_embeds)
            await ctx.send(embed=all_embeds[0], view=view)
        
        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the best match.")

async def setup(bot):
    cog = PlayerBest(bot)
    await bot.add_cog(cog)

    parent = bot.get_command("player")
    if parent is None:
        print("Warning: parent command 'player' not found. Make sure player_group is loaded before this extension.")
        return

    cog.player_best.name = "best"
    parent.add_command(cog.player_best)