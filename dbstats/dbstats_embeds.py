from typing import Dict, List
import discord

def create_betrayers_embed(betrayers_data: List[Dict]) -> discord.Embed:
    per_page = 10
    embeds = []

    for i in range(0, len(betrayers_data), per_page):
        chunk = betrayers_data[i:i + per_page]

        embed = discord.Embed(
            title=f"Top Betrayers",
            description="Players who have committed the most betrayals",
            color=discord.Color.blue()
        )

        for rank, row in enumerate(chunk, start=i + 1):
            player_name = row["player_name"]
            total_betrays = row["total_betrays"]

            embed.add_field(
                name=f"#{rank} {player_name}",
                value=f"Betrays: **{total_betrays}**.",
                inline=False
            )

        embed.set_footer(text=f"Page {i // per_page + 1} of {((len(betrayers_data) - 1) // per_page) + 1}")
        embeds.append(embed)

    return embeds