SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    R.most_killed_player,
    R.most_killed_count,
    R.most_killed_kill_ratio,
    R.most_killer_player,
    R.most_killer_count,
    R.most_killer_death_ratio
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
JOIN Rivalries AS R ON R.player_match_id = PL.player_match_id
WHERE P.player_name = ? AND M.match_id = ?;