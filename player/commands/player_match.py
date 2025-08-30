from sqlite.query_loader import QueryLoader
from dictionaries import gametypes
from player import player_embeds
from discord.ext import commands
from views import paginator_view
import aiosqlite, traceback, sys
import paths

queries = QueryLoader("sqlite/player_queries/match")

class PlayerMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="player_match")
    async def player_match(self, ctx, player_name: str, match_id: str):
        """
        Displays the match of the player with the specified `match_id`.
        """
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row

                player_match_query = queries.get("player_match")
                async with db.execute(player_match_query, (player_name, match_id)) as reader:
                    player_match = await reader.fetchone()

                if not player_match:
                    await ctx.send(f"No match found for '{player_name}' with ID '{match_id}'.")
                    return
                
                subqueries = {
                    "team": queries.get("player_match_team"),
                    "rating": queries.get("player_match_rating"),
                    "combat": queries.get("player_match_combat"),
                    "breakdown": queries.get("player_match_breakdown"),
                    "rivalries": queries.get("player_match_rivalries"),
                    "survivability": queries.get("player_match_survivability"),
                    "choice": queries.get("player_match_choice"),
                    "medals": queries.get("player_match_medals"),
                    "penalties": queries.get("player_match_penalties"),
                }

                gametype_to_query = {
                    "slayer": "player_match_slayer",
                    "capturetheflag": "player_match_ctf",
                    "oddball": "player_match_oddball",
                    "kingofthehill": "player_match_koth",
                    "juggernaut": "player_match_juggernaut",
                    "infection": "player_match_infection",
                    "territories": "player_match_territories",
                    "assault": "player_match_assault",
                    "stockpile": "player_match_stockpile",
                    "headhunter": "player_match_headhunter",
                    "actionsack": "player_match_actionsack"
                }

                # Saved in DB as integer (0 = Slayer, 1 = CTF, ...) 
                gametype = player_match["gametype"]
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
                        player_match_id = player_match["player_match_id"]

                        if player_match_id:
                            params = (player_match_id, )
                    else:
                        params = (player_match["player_name"], )

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
                    player_embeds.create_player_match_embed(player_match),
                    player_embeds.create_player_team_embed(player_match, data.get("team", {})),
                    player_embeds.create_player_rating_embed(player_match, data.get("rating", {})),
                    player_embeds.create_player_gametype_embed(dict(player_match), data.get("gametype", {})),
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
                    await ctx.send("Could not build any embeds for the requested match.")
                    return
                
                view = paginator_view.PaginatorView(pages=all_embeds)
                await ctx.send(embed=all_embeds[0], view=view)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while fetching the requested match.")

async def setup(bot):
    cog = PlayerMatch(bot)
    await bot.add_cog(cog)

    parent = bot.get_command("player")
    if parent is None:
        print("Warning: parent command 'player' not found. Make sure player_group is loaded before this extension.")
        return

    cog.player_match.name = "match"
    parent.add_command(cog.player_match)