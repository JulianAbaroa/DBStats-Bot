SELECT
    stockpile_id,
    carry_time AS stockpile_carry_time
FROM Stockpile
WHERE player_match_id = ?
LIMIT 1;
