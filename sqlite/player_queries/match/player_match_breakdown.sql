SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    B.weapon_kills,
    B.grenade_kills,
    B.melee_kills,
    B.other_kills,
    B.weapon_kills_ratio,
    B.grenade_kills_ratio,
    B.melee_kills_ratio,
    B.other_kills_ratio,
    B.kill_success_ratio
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
JOIN Breakdown AS B ON B.player_match_id = PL.player_match_id
WHERE P.player_name = ? AND M.match_id = ?;