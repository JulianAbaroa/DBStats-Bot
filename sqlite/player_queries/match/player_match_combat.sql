SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    C.kills,
    C.deaths,
    C.assists,
    C.involvements,
    C.consecutive_kills,
    C.kills_per_minute,
    C.deaths_per_minute,
    C.involvements_per_minute,
    C.kill_death_ratio,
    C.kill_death_assists_ratio
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
JOIN Combat AS C ON C.player_match_id = PL.player_match_id
WHERE P.player_name = ? AND M.match_id = ?;