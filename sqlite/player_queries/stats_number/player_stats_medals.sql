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
    SUM(ME.total_medals)       AS total_medals,
    AVG(ME.medals_per_kill)    AS avg_medals_per_kill,
    AVG(ME.medals_per_minute)  AS avg_medals_per_minute,
    MEIN.medal_type,
    SUM(MEIN.count)            AS total_count
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Medals AS ME ON ME.player_match_id = rm.player_match_id
JOIN MedalsInfo AS MEIN ON MEIN.medals_id = ME.medals_id
GROUP BY MEIN.medal_type, P.player_name, P.player_id
ORDER BY total_count DESC;
