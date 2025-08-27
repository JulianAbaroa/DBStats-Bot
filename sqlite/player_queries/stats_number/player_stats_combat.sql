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
    SUM(C.kills)              AS total_kills,
    SUM(C.deaths)             AS total_deaths,
    SUM(C.assists)            AS total_assists,
    SUM(C.involvements)       AS total_involvements,
    SUM(C.consecutive_kills)  AS total_consecutive_kills,
    AVG(C.kills_per_minute)   AS avg_kills_per_minute,
    AVG(C.deaths_per_minute)  AS avg_deaths_per_minute,
    AVG(C.involvements_per_minute) AS avg_involvements_per_minute,
    AVG(C.kill_death_ratio)        AS avg_kill_death_ratio,
    AVG(C.kill_death_assists_ratio) AS avg_kda_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Combat AS C ON C.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;
