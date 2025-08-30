SELECT
    head_hunter_id,
    max_skulls AS headhunter_max_skulls
FROM HeadHunter
WHERE player_match_id = ?
LIMIT 1;
