WITH recent_matches AS (
    SELECT PL.player_match_id, PL.player_id, T.match_id, M.match_timestamp
    FROM Players AS PL
    JOIN Teams AS T ON PL.team_id = T.team_id
    JOIN Matches AS M ON T.match_id = M.match_id
    JOIN Profiles AS P2 ON P2.player_id = PL.player_id
    WHERE P2.player_name = ?
    ORDER BY M.match_timestamp DESC
    LIMIT ?
),

most_killed AS (
    SELECT 
        rm.player_id,
        R.most_killed_player AS rival,
        SUM(R.most_killed_count) AS total_kills,
        AVG(R.most_killed_kill_ratio) AS avg_kill_ratio
    FROM recent_matches rm
    JOIN Rivalries R ON R.player_match_id = rm.player_match_id
    GROUP BY R.most_killed_player, rm.player_id
    ORDER BY total_kills DESC
    LIMIT 1
),

most_killer AS (
    SELECT 
        rm.player_id,
        R.most_killer_player AS rival,
        SUM(R.most_killer_count) AS total_kills_against,
        AVG(R.most_killer_death_ratio) AS avg_death_ratio
    FROM recent_matches rm
    JOIN Rivalries R ON R.player_match_id = rm.player_match_id
    GROUP BY R.most_killer_player, rm.player_id
    ORDER BY total_kills_against DESC
    LIMIT 1
)

SELECT
    P.player_name,
    P.player_id,
    mk.rival            AS most_killed_player,
    mk.total_kills      AS most_killed_count,
    mk.avg_kill_ratio   AS most_killed_kill_ratio,
    mr.rival            AS most_killer_player,
    mr.total_kills_against AS most_killer_count,
    mr.avg_death_ratio  AS most_killer_death_ratio
FROM most_killed mk
JOIN most_killer mr ON mr.player_id = mk.player_id
JOIN Profiles P ON P.player_id = mk.player_id;
