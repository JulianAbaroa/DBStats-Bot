SELECT
    koth_id,
    time_in_hill AS hill_time
FROM KingOfTheHill
WHERE player_match_id = ?
LIMIT 1;
