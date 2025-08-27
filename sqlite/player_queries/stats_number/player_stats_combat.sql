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
    SUM(PE.suicides)            AS total_suicides,
    AVG(PE.suicides_per_death)  AS avg_suicides_per_death,
    SUM(PE.betrayals)           AS total_betrayals,
    AVG(PE.betrayals_per_kill)  AS avg_betrayals_per_kill
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Penalties AS PE ON PE.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;
