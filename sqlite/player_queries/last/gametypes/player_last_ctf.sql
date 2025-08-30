SELECT
    ctf_id,
    flag_captures,
    flag_recovers,
    flag_carry_time
FROM CaptureTheFlag
WHERE player_match_id = ?
LIMIT 1;