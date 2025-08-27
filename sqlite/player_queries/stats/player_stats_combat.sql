WITH recent_matches AS (
    SELECT 
        PL.player_match_id, 
        PL.player_id, 
        T.match_id, 
        M.match_timestamp
    FROM Players AS PL
    JOIN Teams AS T ON PL.team_id = T.team_id
    JOIN Matches AS M ON T.match_id = M.match_id
    JOIN Profiles AS P2 ON P2.player_id = PL.player_id
    WHERE P2.player_name = ?
    ORDER BY M.match_timestamp DESC
    LIMIT ?
)
SELECT
    P.player_name,
    P.player_id,
    SUM(C.kills)                  AS kills,
    SUM(C.deaths)                 AS deaths,
    SUM(C.assists)                AS assists,
    SUM(C.involvements)           AS involvements,
    SUM(C.consecutive_kills)      AS consecutive_kills,
    AVG(C.kills_per_minute)       AS kills_per_minute,
    AVG(C.deaths_per_minute)      AS deaths_per_minute,
    AVG(C.involvements_per_minute) AS involvements_per_minute,
    AVG(C.kill_death_ratio)       AS kill_death_ratio,
    AVG(C.kill_death_assists_ratio) AS kill_death_assists_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Combat AS C ON C.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;