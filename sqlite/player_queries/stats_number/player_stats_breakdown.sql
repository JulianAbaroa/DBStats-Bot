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
    SUM(B.weapon_kills)       AS total_weapon_kills,
    SUM(B.grenade_kills)      AS total_grenade_kills,
    SUM(B.melee_kills)        AS total_melee_kills,
    SUM(B.other_kills)        AS total_other_kills,
    AVG(B.weapon_kills_ratio) AS avg_weapon_kills_ratio,
    AVG(B.grenade_kills_ratio) AS avg_grenade_kills_ratio,
    AVG(B.melee_kills_ratio)  AS avg_melee_kills_ratio,
    AVG(B.other_kills_ratio)  AS avg_other_kills_ratio,
    AVG(B.kill_success_ratio) AS avg_kill_success_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Breakdown AS B ON B.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;
