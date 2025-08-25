SELECT
    P.player_name,
    P.player_id,
    PL.rating
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
WHERE P.player_name = ?
ORDER BY PL.rating DESC
LIMIT 1;