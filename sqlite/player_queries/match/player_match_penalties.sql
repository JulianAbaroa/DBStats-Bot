SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    PE.suicides,
    PE.suicides_per_death,
    PE.betrayals,
    PE.betrayals_per_kill
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
JOIN Penalties AS PE ON PE.player_match_id = PL.player_match_id
WHERE P.player_name = ? AND M.match_id = ?;