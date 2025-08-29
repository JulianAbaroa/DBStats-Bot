SELECT
    P.player_name,
    P.player_id,
    SUM(1) AS total_betrays
FROM Penalties AS Pen
JOIN Players AS PL ON Pen.player_match_id = PL.player_match_id
JOIN Profiles AS P ON PL.player_id = P.player_id
WHERE Pen.penalty_type = 'betrays'
GROUP BY P.player_id, P.player_name
ORDER BY total_betrays DESC;
