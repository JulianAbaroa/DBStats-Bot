WITH recent_matches AS (
    SELECT 
        PL.player_match_id,
        PL.player_id,
        T.match_id,
        M.match_timestamp
    FROM Players PL
    JOIN Teams T ON PL.team_id = T.team_id
    JOIN Matches M ON T.match_id = M.match_id
    JOIN Profiles P2 ON P2.player_id = PL.player_id
    WHERE P2.player_name = ?
    ORDER BY M.match_timestamp DESC
    LIMIT ?
)
SELECT
    P.player_name,
    P.player_id,
    SUM(B.weapon_kills)       AS weapon_kills,
    SUM(B.grenade_kills)      AS grenade_kills,
    SUM(B.melee_kills)        AS melee_kills,
    SUM(B.other_kills)        AS other_kills,
    AVG(B.weapon_kills_ratio) AS weapon_kills_ratio,
    AVG(B.grenade_kills_ratio) AS grenade_kills_ratio,
    AVG(B.melee_kills_ratio)  AS melee_kills_ratio,
    AVG(B.other_kills_ratio)  AS other_kills_ratio,
    AVG(B.kill_success_ratio) AS kill_success_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Breakdown AS B ON B.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;