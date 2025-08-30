SELECT
    infection_id,
    survival_time AS infection_survival_time,
    infections AS infection_count
FROM Infection
WHERE player_match_id = ?
LIMIT 1;
