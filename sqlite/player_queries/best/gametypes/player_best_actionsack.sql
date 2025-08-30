SELECT
    action_sack_id
FROM ActionSack
WHERE player_match_id = ?
LIMIT 1;
