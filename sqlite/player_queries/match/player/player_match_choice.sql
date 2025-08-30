SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    CH.most_used_weapon,
    CH.most_used_weapon_kills,
    CH.most_used_weapon_kills_ratio
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Teams AS T ON PL.team_id = T.team_id
JOIN Matches AS M ON T.match_id = M.match_id
JOIN Choice AS CH ON CH.player_match_id = PL.player_match_id
WHERE P.player_name = ? AND M.match_id = ?;