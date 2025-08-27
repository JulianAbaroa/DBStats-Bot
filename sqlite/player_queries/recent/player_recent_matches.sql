SELECT
    P.player_name,
    PL.rating AS rating,
    M.match_timestamp,
    M.duration,
    M.gametype_name,
    M.is_matchmaking,
    M.match_id,
    T.winned
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
WHERE P.player_name = ?
ORDER BY M.match_timestamp DESC
LIMIT N;