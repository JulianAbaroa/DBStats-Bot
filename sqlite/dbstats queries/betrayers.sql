SELECT
    P.player_name,
    P.player_id,
    SUM(Pen.betrayals) AS total_betrays
FROM Penalties AS Pen
JOIN Players AS PL ON Pen.player_match_id = PL.player_match_id
JOIN Profiles AS P ON PL.player_id = P.player_id
GROUP BY P.player_id, P.player_name
HAVING total_betrays > 0
ORDER BY total_betrays DESC;
