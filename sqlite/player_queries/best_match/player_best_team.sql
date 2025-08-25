SELECT
    P.player_name,
    P.player_id,
    T.team_id,
    T.color,
    T.rating,
    T.winned,
    T.deaths,
    T.kills
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
WHERE P.player_name = ?
ORDER BY PL.rating DESC
LIMIT 1;