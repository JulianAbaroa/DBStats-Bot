from dictionaries.medal_emojis import medal_emojis
from dictionaries import gametypes_ids
from datetime import datetime
from typing import Dict, Callable, Optional, Any, List
import discord
import os

# TODO: Agregar un embed que muestre los stats del gametype.

def format_duration(duration_minutes: float) -> str:
    try:
        duration_minutes = float(duration_minutes)
    except:
        return "N/A"
    
    minutes = int(duration_minutes)
    seconds = int((duration_minutes - minutes) * 60)
    return f"{minutes}m {seconds}s"

def _get_stat(stats: Optional[Dict[str, Any]], *keys, default=None):
    if not stats:
        return default
    for k in keys:
        if k in stats and stats[k] is not None:
            return stats[k]
    return default

def truncate_float(x, decimals=3):
    try:
        x_float = float(x)
        
        factor = 10 ** decimals
        truncated_value = int(x_float * factor) / factor
        
        return truncated_value
    except (ValueError, TypeError):
        return 'N/A'

def create_player_embed(player_data):
    last_seen_value = player_data['last_seen']
    formatted_date = "N/A"

    try:
        if isinstance(last_seen_value, str):
            last_seen_datetime = datetime.fromisoformat(last_seen_value)
            formatted_date = last_seen_datetime.strftime("%Y-%m-%d")
        elif last_seen_value is not None:
            formatted_date = str(last_seen_value)
    except Exception:
        formatted_date = "N/A"

    service_id = player_data['service_id'] if player_data['service_id'] else "N/A"
    clan_tag = player_data['clan_tag'] if player_data['clan_tag'] else "N/A"

    embed = discord.Embed(
        title=f"{player_data['player_name']}",
        color=discord.Color.blue()
    )

    files_to_send = []

    def try_make_file(path_raw):
        if not path_raw:
            return None, None
        try:
            p = os.path.expanduser(path_raw)
            p = os.path.abspath(p)
            if os.path.exists(p) and os.path.isfile(p):
                basename = os.path.basename(p)
                return discord.File(p, filename=basename), basename
        except Exception:
            return None, None
        return None, None

    file_emblem, emblem_basename = try_make_file(player_data['emblem_path'])
    file_nameplate, nameplate_basename = try_make_file(player_data['nameplate_path'])

    if file_emblem:
        embed.set_thumbnail(url=f"attachment://{emblem_basename}")
        files_to_send.append(file_emblem)

    if file_nameplate:
        embed.set_image(url=f"attachment://{nameplate_basename}")
        files_to_send.append(file_nameplate)

    embed.add_field(name="Service ID", value=f"{service_id}", inline=True)
    embed.add_field(name="Clan tag", value=f"{clan_tag}", inline=True)
    embed.add_field(name="Last seen", value=f"{formatted_date}", inline=False)

    return embed, files_to_send

def create_player_match_embed(player_match: Dict) -> discord.Embed:
    type_str = "Matchmaking" if player_match["is_matchmaking"] else "Custom Game Browser"
    duration_str = format_duration(float(player_match["duration"]))
    datetimeFormatted = player_match["match_timestamp"].split(".")[0]

    embed = discord.Embed(
        title=f"Match Resume: {type_str}",
        description=f"{player_match['gametype_name']}, {duration_str}, {datetimeFormatted}",
        color=discord.Color.blue()
    )

    if player_match['is_teams_enabled']:
        embed.add_field(name="Player", value=(
            f"Name: {player_match['player_name']}\n"
            f"Team: {player_match['color']}"
            ), inline=True
        )
    else:
        embed.add_field(name="Player", value=(
            f"Name: {player_match['player_name']}"
            ), inline=True
        )

    embed.add_field(name="Resume", value=(
        f"Gametype name: {player_match['gametype_name']}\n"
        f"Result: {player_match['result']}\n"
        f"Match completed: {'Yes' if player_match['was_match_incomplete'] else 'No'}"
        ), inline=False
    )

    return embed

def create_player_team_embed(player_match: Dict, team_data: Dict) -> discord.Embed:
    rating = int(team_data['rating'])

    embed = discord.Embed(
        title=f"Team for {player_match['player_name']}",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Team Resume", 
        value=(
            f"Team: {team_data['color']}\n"
            f"Team rating: {rating}\n"
            f"Team kills: {team_data['kills']}\n"
            f"Team deaths: {team_data['deaths']}\n"
            f"Result: {team_data['result']}"
        ), inline=True
    )

    return embed

def create_player_rating_embed(player_match: Dict, info: Dict) -> discord.Embed:
    ratingFormatted = int(info.get('rating', 'N/A'))

    embed = discord.Embed(
        title=f"{player_match['player_name']} Overview",
        description=f"Rating: {ratingFormatted}",
        color=discord.Color.blue()
    )

    return embed

def create_player_gametype_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    gametype_id = player_match.get("gametype")
    gametype_key = gametypes_ids.gametypes_ids_to_names.get(gametype_id)

    if not gametype_key:
        gametype_key = str(player_match.get("gametype_name", "")).strip().lower().replace(" ", "").replace("-", "").replace("_", "")

    gametype_handlers: Dict[str, Callable[[Dict[str, Any], Optional[Dict[str, Any]]], discord.Embed]] = {
        "slayer": _create_player_slayer_embed,
        "capturetheflag": _create_player_ctf_embed,
        "ctf": _create_player_ctf_embed,
        "oddball": _create_player_oddball_embed,
        "kingofthehill": _create_player_koth_embed,
        "koth": _create_player_koth_embed,
        "juggernaut": _create_player_juggernaut_embed,
        "infection": _create_player_infection_embed,
        "territories": _create_player_territories_embed,
        "assault": _create_player_assault_embed,
        "stockpile": _create_player_stockpile_embed,
        "headhunter": _create_player_headhunter_embed,
        "actionsack": _create_player_actionsack_embed
    }

    handler = gametype_handlers.get(gametype_key, _create_generic_gametype_embed)
    return handler(player_match, stats)

def _create_player_slayer_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(
        title=f"Slayer for {player_match.get('player_name', 'Unknown')}",
        color=discord.Color.blue()
    )
    if not stats:
        embed.description = "There are no specific Slayer stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    rating = _get_stat(stats, "rating", "slayer_rating", "player_rating")
    embed.add_field(name="Statistics", value=f"Rating: {truncate_float(rating)}", inline=False)
    return embed

def _create_player_ctf_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"CTF for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific CTF stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    captures = _get_stat(stats, "flag_captures", "captures")
    recovers = _get_stat(stats, "flag_recovers", "recovers")
    carry_time = _get_stat(stats, "flag_carry_time", "carry_time")

    carry_time_formatted = format_duration(carry_time)

    embed.add_field(
        name="Statistics", 
        value=(
            f"Flag captures: {captures}\n"
            f"Flag recovers: {recovers}\n"
            f"Carry time: {carry_time_formatted}\n"
        ), inline=True
    )

    return embed

def _create_player_oddball_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Oddball for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Oddball stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    carry_time = _get_stat(stats, "carry_time", "oddball_carry_time")
    carry_time_formatted = format_duration(carry_time)

    ball_kills = _get_stat(stats, "ball_kills")

    embed.add_field(
        name="Statistics", 
        value=(
            f"Carry time: {carry_time_formatted}\n"
            f"Ball kills: {ball_kills}"
        ), inline=True
    )

    return embed

def _create_player_koth_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"KOTH for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific KOTH stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    hill_time = _get_stat(stats, "time_in_hill", "hill_time")
    hill_time_formatted = format_duration(hill_time)

    embed.add_field(
        name="Statistics", 
        value=(
            f"Time in hill: {hill_time_formatted}"
        ), inline=True
    )

    return embed

def _create_player_juggernaut_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Juggernaut for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Juggernaut stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    time = _get_stat(stats, "juggernaut_time")
    time_formatted = format_duration(time)

    embed.add_field(
        name="Statistics", 
        value=(
            f"Juggernaut time: {time_formatted}"
        ), inline=True)

    return embed

def _create_player_infection_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Infection for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Infection stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed

    survival = _get_stat(stats, "survival_time", "infection_survival_time")
    survival_formatted = format_duration(survival)

    infections = _get_stat(stats, "infections", "infection_count")

    embed.add_field(
        name="Statistics", 
        value=(
            f"Survival time: {survival_formatted}\n"
            f"Infections: {infections}\n"
        ), inline=True
    )
    
    return embed

def _create_player_territories_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Territories for {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Territories stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed
    
    captures = _get_stat(stats, "captures", "territories_captures")

    embed.add_field(
        name="Statistics", 
        value=(
            f"Captures: {captures}"
        ), inline=True
    )

    return embed

def _create_player_assault_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Assault — {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Assault stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed
    
    bombs = _get_stat(stats, "bombs_planted")
    det = _get_stat(stats, "detonations")
    carry = _get_stat(stats, "bomb_carry_time", "bomb_carry_time")
    carry_formatted = format_duration(carry)
    defuses = _get_stat(stats, "defuses")

    embed.add_field(
        name="Statistics", 
        value=(
            f"Bombs planted: {bombs}\n"
            f"Detonations: {det}\n"
            f"Carry time: {carry_formatted}\n"
            f"Defuses: {defuses}\n"
        ), inline=True
    )

    return embed

def _create_player_stockpile_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Stockpile — {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Stockpile stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed
    
    carry = _get_stat(stats, "carry_time", "stockpile_carry_time")
    carry_formatted = format_duration(carry)

    embed.add_field(
        name="Statistics", 
        value=(
            f"Carry time: {carry_formatted}"
        ), inline=True
    )

    return embed

def _create_player_headhunter_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"Headhunter — {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific Headhunter stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed
    
    max_skulls = _get_stat(stats, "max_skulls", "headhunter_max_skulls")

    embed.add_field(
        name="Statistics", 
        value=(
            f"Max skulls: {max_skulls}"
        ), 
        inline=True
    )

    return embed

def _create_player_actionsack_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"ActionSack — {player_match.get('player_name', 'Unknown')}", color=discord.Color.blue())
    if not stats:
        embed.description = "There are no specific ActionSack stats for this match."
        embed.add_field(name="Match", value=player_match.get("match_id", "-"), inline=True)
        return embed
    
    embed.add_field(name="Statistics", value="No specific stats", inline=False)

    return embed

def _create_generic_gametype_embed(player_match: Dict[str, Any], stats: Optional[Dict[str, Any]]) -> discord.Embed:
    title = f"{player_match.get('gametype_name') or player_match.get('gametype') or 'Gametype'} Statistics"
    embed = discord.Embed(title=title, color=0x95a5a6)
    embed.set_author(name=player_match.get('player_name') or "Unknown")
    if not stats:
        embed.description = "There are no specific stats for this gametype."
        return embed
    
    for k, v in list(stats.items())[:10]:
        if isinstance(v, (list, tuple)):
            embed.add_field(name=k, value=", ".join(str(i) for i in v) or "—", inline=True)
        else:
            embed.add_field(name=k, value=str(v), inline=True)

    return embed

def create_player_combat_embed(player_match: Dict, combat_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Combat Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Basic",
        value=(
            f"Kills: {combat_data.get('kills', 'N/A')}\n"
            f"Deaths: {combat_data.get('deaths', 'N/A')}\n"
            f"Assists: {combat_data.get('assists', 'N/A')}\n"
            f"Involvements: {combat_data.get('involvements', 'N/A')}\n"
            f"Consecutive kills: {combat_data.get('consecutive_kills', 'N/A')}\n"
        ), inline=False
    )

    kpm = combat_data.get('kills_per_minute', 'N/A')
    kpm_truncated = truncate_float(kpm)

    dpm = combat_data.get('deaths_per_minute', 'N/A')
    dpm_truncated = truncate_float(dpm)

    ipm = combat_data.get('involvements_per_minute', 'N/A')
    ipm_truncated = truncate_float(ipm)

    embed.add_field(
        name="Per Minute",
        value=(
            f"Kills per minute: {kpm_truncated}\n"
            f"Deaths per minute: {dpm_truncated}\n"
            f"Involvements per minute: {ipm_truncated}\n"
        ), inline=False
    )

    kd = combat_data.get('kill_death_ratio', 'N/A')
    kd_truncated = truncate_float(kd)

    kda = combat_data.get('kill_death_assists_ratio', 'N/A')
    kda_truncated = truncate_float(kda)

    embed.add_field(
        name="Ratios",
        value=(
            f"KD: {kd_truncated}\n"
            f"KDA: {kda_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_breakdown_embed(player_match: Dict, breakdown_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Breakdown Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Kill Types",
        value=(
            f"Weapon kills: {breakdown_data.get('weapon_kills', 'N/A')}\n"
            f"Grenade kills: {breakdown_data.get('grenade_kills', 'N/A')}\n"
            f"Melee kills: {breakdown_data.get('melee_kills', 'N/A')}\n"
            f"Other kills: {breakdown_data.get('other_kills', 'N/A')}\n"
        ), inline=False
    )

    wkr = breakdown_data.get('weapon_kills_ratio', 'N/A')
    wkr_truncated = truncate_float(wkr)

    gkr = breakdown_data.get('grenade_kills_ratio', 'N/A')
    gkr_truncated = truncate_float(gkr)

    mkr = breakdown_data.get('melee_kills_ratio', 'N/A')
    mkr_truncated = truncate_float(mkr)

    okr = breakdown_data.get('other_kills_ratio', 'N/A')
    okr_truncated = truncate_float(okr)

    ksr = breakdown_data.get('kill_success_ratio', 'N/A')
    ksr_truncated = truncate_float(ksr)

    embed.add_field(
        name="Ratios",
        value=(
            f"Weapon kills ratio: {wkr_truncated}\n"
            f"Grenade kills ratio: {gkr_truncated}\n"
            f"Melee kills ratio: {mkr_truncated}\n"
            f"Other kills ratio: {okr_truncated}\n"
            f"Kill success ratio: {ksr_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_rivalries_embed(player_match: Dict, rivalries_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Rivalries Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    mkkr = rivalries_data.get('most_killed_kill_ratio', 'N/A')
    mkkr_truncated = truncate_float(mkkr)

    embed.add_field(
        name="Player You Killed Most",
        value=(
            f"Target: {rivalries_data.get('most_killed_player', 'N/A')}\n"
            f"Times you killed them: {rivalries_data.get('most_killed_count', 'N/A')}\n"
            f"Share of your total kills: {mkkr_truncated}\n"
        ), inline=False
    )

    mkdr = rivalries_data.get('most_killer_death_ratio', 'N/A')
    mkkr_truncated = truncate_float(mkdr)

    embed.add_field(
        name="Player Who Killed You the Most",
        value=(
            f"Nemesis: {rivalries_data.get('most_killer_player', 'N/A')}\n"
            f"Times they killed you: {rivalries_data.get('most_killer_count', 'N/A')}\n"
            f"Share of your total deaths: {mkkr_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_survivability_embed(player_match: Dict, survivability_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Survivability Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    ma = survivability_data.get('minutes_alive', 'N/A')
    ma_formatted = format_duration(ma)

    mp = survivability_data.get('minutes_played', 'N/A')
    mp_formatted = format_duration(mp)

    atr = survivability_data.get('alive_time_ratio', 'N/A')
    atr_truncated = truncate_float(atr)

    embed.add_field(
        name="Survival Performance",
        value=(
            f"Minutes alive: {ma_formatted}\n"
            f"Minutes played: {mp_formatted}\n"
            f"Survival rate: {atr_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_choice_embed(player_match: Dict, choice_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Choice Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    muwkr = choice_data.get('most_used_weapon_kills_ratio', 'N/A')
    muwkr_truncated = truncate_float(muwkr)

    embed.add_field(
        name="Weapon of Choice",
        value=(
            f"Most used weapon: {choice_data.get('most_used_weapon', 'N/A')}\n"
            f"Kills with this weapon: {choice_data.get('most_used_weapon_kills', 'N/A')}\n"
            f"Share of total kills: {muwkr_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_medals_embed(player_match: Dict, medals_data: List[Dict]) -> discord.Embed:
    embed = discord.Embed(
        title=f"Medals Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    first = medals_data[0] if medals_data else {}

    mpk = first.get('medals_per_kill', 'N/A')
    mpk_truncated = truncate_float(mpk)

    mpm = first.get('medals_per_minute', 'N/A')
    mpm_truncated = truncate_float(mpm)

    embed.add_field(
        name="Medals",
        value=(
            f"Total medals: {first.get('total_medals', 'N/A')}\n"
            f"Medals per kill: {mpk_truncated}\n"
            f"Medals per minute: {mpm_truncated}\n"
        ), inline=False
    )

    embed.add_field(
        name="Medals Info",
        value="\n".join(
            f"{medal_emojis.get(row['medal_type'])} {row['medal_type']}: {truncate_float(row['count'])} " for row in medals_data
        ) if medals_data else "N/A",
        inline=False
    )

    return embed

def create_player_penalties_embed(player_match: Dict, penalties_data: Dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"Penalties Data for {player_match['player_name']}",
        color=discord.Color.blue()
    )

    spd = penalties_data.get('suicides_per_death', 'N/A')
    spd_truncated = truncate_float(spd)

    bpk = penalties_data.get('betrayals_per_kill', 'N/A')
    bpk_truncated = truncate_float(bpk)

    embed.add_field(
        name="Penalties",
        value=(
            f"Suicides: {penalties_data.get('suicides', 'N/A')}\n"
            f"Suicides per minute: {spd_truncated}\n"
            f"Betrayals: {penalties_data.get('betrayals', 'N/A')}\n"
            f"Betrayals per minute: {bpk_truncated}\n"
        ), inline=False
    )

    return embed

def create_player_recent_embeds(player_name: str, matches_data: list) -> list[discord.Embed]:
    pages = []
    page_size = 5

    if not matches_data:
        embed = discord.Embed(
            title=f"Recent games of {player_name}",
            description="No recent games found for this player.",
            color=discord.Color.orange()
        )
        return [embed]

    for i in range(0, len(matches_data), page_size):
        page_matches = matches_data[i:i + page_size]
        
        embed = discord.Embed(
            title=f"Recent games of {player_name}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Page {len(pages) + 1}/{len(matches_data) // page_size + (1 if len(matches_data) % page_size else 0)}")

        for row in page_matches:
            match = dict(row)
            
            match_type = "Matchmaking" if match.get("is_matchmaking") else "Custom Game Browser"
            duration = format_duration(float(match["duration"]))
            datetime_str = match["match_timestamp"].split(".")[0]
            
            result = match.get("result")
            rating = int(match.get("rating", "N/A"))

            embed.add_field(
                name=f"Match resume: {match_type} ({match.get('gametype_name')})",
                value=(
                    f"Result: **{result}**\n"
                    f"Rating: {rating}\n"
                    f"Duration: {duration}\n"
                    f"Datetime: {datetime_str}\n"
                    f"Match ID: `{match.get('match_id')}`\n"
                ),
                inline=False
            )
        pages.append(embed)

    return pages