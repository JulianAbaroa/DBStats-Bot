WITH recent_matches AS (
    SELECT 
        PL.player_match_id, 
        PL.player_id, 
        M.match_id
    FROM Players AS PL
    JOIN Matches AS M ON PL.match_id = M.match_id
    JOIN Profiles AS P2 ON P2.player_id = PL.player_id
    WHERE P2.player_name = ?
    ORDER BY M.match_id DESC
    LIMIT ?
)

SELECT
    P.player_name,
    P.player_id,
    CH.most_used_weapon,
    SUM(CH.most_used_weapon_kills)       AS total_weapon_kills,
    AVG(CH.most_used_weapon_kills_ratio) AS avg_weapon_kills_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Choice AS CH ON CH.player_match_id = rm.player_match_id
GROUP BY CH.most_used_weapon
ORDER BY total_weapon_kills DESC
LIMIT 1;