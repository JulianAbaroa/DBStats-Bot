SELECT
    slayer_id,
    rating AS slayer_rating
FROM Slayer
WHERE player_match_id = ?
LIMIT 1;
