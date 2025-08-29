SELECT
    assault_id,
    bombs_planted,
    detonations,
    bomb_carry_time,
    defuses
FROM Assault
WHERE player_match_id = ?
LIMIT 1;
