SELECT
    oddball_id,
    carry_time AS oddball_carry_time,
    ball_kills AS oddball_ball_kills
FROM Oddball
WHERE player_match_id = ?
LIMIT 1;