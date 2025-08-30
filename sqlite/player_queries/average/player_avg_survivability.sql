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
    AVG(S.minutes_alive)    AS minutes_alive,
    AVG(S.minutes_played)   AS minutes_played,
    AVG(S.alive_time_ratio) AS alive_time_ratio
FROM recent_matches rm
JOIN Profiles AS P ON P.player_id = rm.player_id
JOIN Survivability AS S ON S.player_match_id = rm.player_match_id
GROUP BY P.player_name, P.player_id;
