SELECT
    P.player_name,
    P.player_id,
    PL.player_match_id,
    ME.total_medals,
    ME.medals_per_kill,
    ME.medals_per_minute,
    MEIN.medal_type,
    MEIN.count
FROM Profiles AS P
JOIN Players AS PL ON P.player_id = PL.player_id
JOIN Medals AS ME ON ME.player_match_id = PL.player_match_id
JOIN MedalsInfo AS MEIN ON MEIN.medals_id = ME.medals_id
WHERE P.player_name = ?
  AND PL.player_match_id = (
      SELECT player_match_id
      FROM Players
      WHERE player_id = P.player_id
      ORDER BY rating DESC
      LIMIT 1
  )
ORDER BY MEIN.count DESC;