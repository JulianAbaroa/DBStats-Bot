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
    AVG(S.minutes_alive)    AS avg_minutes_alive,
    AVG(S.minutes_played)   AS avg_minutes_played,
    AVG(S.alive_time_ratio) AS avg_alive_time_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Survivability AS S ON S.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;