SELECT
    P.player_name,
    P.player_id,
    PL.rating,
    PL.player_match_id,
    T.team_id,
    T.result,
    T.color,
    M.match_id,
    M.is_matchmaking,
    M.gametype,
    M.gametype_name,
    M.was_match_incomplete,
    M.is_teams_enabled,
    M.duration,
    M.match_timestamp
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
WHERE P.player_name = ?
ORDER BY PL.rating DESC
LIMIT 1;