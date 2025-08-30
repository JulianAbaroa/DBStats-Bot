from player.player_commands.player_group import PlayerGroup
from sqlite.query_loader import QueryLoader
from discord.ext import commands
from player import player_embeds
import aiosqlite, traceback, sys
import paths

queries = QueryLoader("sqlite/player_queries/lookup")

class PlayerLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @PlayerGroup.player_group.command(name="lookup", parent="player")
    async def player_lookup(self, ctx, *, player_name: str):
        """Displays the player's profile and customization."""
        try:
            async with aiosqlite.connect(paths.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row

                player_profile_sql = queries.get("player_profile")
                async with db.execute(player_profile_sql, (player_name, )) as reader:
                    player_profile = await reader.fetchone()

            if not player_profile:
                await ctx.send(f"I didn't find the player '{player_name}'")
                return
                
            embed, files_to_send = player_embeds.create_player_embed(player_profile)

            if files_to_send:
                await ctx.send(files=files_to_send, embed=embed)
            else:
                await ctx.send(embed=embed)

        except Exception:
            traceback.print_exc(file=sys.stderr)
            await ctx.send("An error occurred while looking up the player.")

async def setup(bot):
    await bot.add_cog(PlayerLookup(bot))