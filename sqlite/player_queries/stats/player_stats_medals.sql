WITH recent_matches AS (
    SELECT PL.player_match_id, PL.player_id, T.match_id, M.match_timestamp
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
    AVG(ME.total_medals)        AS total_medals,
    AVG(ME.medals_per_kill)     AS medals_per_kill,
    AVG(ME.medals_per_minute)   AS medals_per_minute,
    MI.medal_type,
    AVG(MI.count)               AS count
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Medals AS ME ON ME.player_match_id = rm.player_match_id
JOIN MedalsInfo AS MI ON MI.medals_id = ME.medals_id
GROUP BY MI.medal_type, P.player_id
ORDER BY count DESC;