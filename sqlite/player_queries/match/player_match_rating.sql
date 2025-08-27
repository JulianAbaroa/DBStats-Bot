SELECT
    P.player_name,
    P.player_id,
    PL.rating
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
WHERE P.player_name = ? AND M.match_id = ?;