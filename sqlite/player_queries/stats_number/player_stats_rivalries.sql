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
),

most_killed AS (
    SELECT 
        P.player_id,
        R.most_killed_player AS rival,
        SUM(R.most_killed_count) AS total_count,
        AVG(R.most_killed_kill_ratio) AS avg_kill_ratio
    FROM recent_matches rm
    JOIN Profiles P ON P.player_id = rm.player_id
    JOIN Rivalries R ON R.player_match_id = rm.player_match_id
    GROUP BY R.most_killed_player
    ORDER BY total_count DESC
    LIMIT 1
),

most_killer AS (
    SELECT 
        P.player_id,
        R.most_killer_player AS rival,
        SUM(R.most_killer_count) AS total_count,
        AVG(R.most_killer_death_ratio) AS avg_death_ratio
    FROM recent_matches rm
    JOIN Profiles P ON P.player_id = rm.player_id
    JOIN Rivalries R ON R.player_match_id = rm.player_match_id
    GROUP BY R.most_killer_player
    ORDER BY total_count DESC
    LIMIT 1
)

SELECT
    P.player_name,
    P.player_id,
    mk.rival            AS most_killed_player,
    mk.total_count      AS most_killed_count,
    mk.avg_kill_ratio   AS most_killed_kill_ratio,
    mr.rival            AS most_killer_player,
    mr.total_count      AS most_killer_count,
    mr.avg_death_ratio  AS most_killer_death_ratio
FROM Profiles P
JOIN most_killed mk ON mk.player_id = P.player_id
JOIN most_killer mr ON mr.player_id = P.player_id
WHERE P.player_name = ?;
