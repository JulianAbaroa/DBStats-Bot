SELECT
    juggernaut_id,
    juggernaut_time
FROM Juggernaut
WHERE player_match_id = ?
LIMIT 1;
