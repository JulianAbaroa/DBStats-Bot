SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    S.minutes_alive,
    S.minutes_played,
    S.alive_time_ratio
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Survivability AS S ON S.player_match_id = PL.player_match_id
WHERE P.player_name = ?
ORDER BY PL.rating DESC
LIMIT 1;