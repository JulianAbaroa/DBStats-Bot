from datetime import datetime
import discord

def create_match_embed(match_data, teams_data):
    is_matchmaking = match_data["is_matchmaking"]
    type = "Matchmaking" if is_matchmaking else "Custom Game Browser"

    datetimeFormatted = match_data["match_timestamp"].split(".")[0]

    duration_minutes = float(match_data["duration"])
    minutes = int(duration_minutes)
    seconds = int((duration_minutes - minutes) * 60)
    duration_str = f"{minutes}m {seconds}s"

    embed = discord.Embed(
        title=f"Match Resume: {type}",
        description=f"{match_data['gametype_name']}, {duration_str}, {datetimeFormatted}",
        color=discord.Color.blue()
    )

    if not teams_data:
        embed.add_field(name="Teams", value="No teams recorded", inline=False)
    else:
        for team in teams_data:
            rating = int(team["rating"])

            team_name = f"{team['color']}"
            team_value = (
                f"Kills: {team['kills']}\n"
                f"Deaths: {team['deaths']}\n"
                f"Rating: {rating}\n"
                f"Result: {team['result']}"
            )
            embed.add_field(name=f"Team {team_name} resume:", value=team_value, inline=True)

    return embed
