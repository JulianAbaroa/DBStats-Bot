SELECT 
    P.player_id, 
    P.player_name, 
    P.last_seen, 
    C.service_id, 
    C.clan_tag,
    C.nameplate_path,
    C.emblem_path
FROM Profiles AS P
LEFT JOIN Customizations AS C ON P.player_id = C.player_id
WHERE P.player_name = ? COLLATE NOCASE
LIMIT 1;