SELECT
    territories_id,
    captures AS territories_captures
FROM Territories
WHERE player_match_id = ?
LIMIT 1;