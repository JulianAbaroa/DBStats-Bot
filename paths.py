import os

media_path = "/media/maste"
drives = [os.path.join(media_path, d) for d in os.listdir(media_path)]
halo_drive = None

for d in drives:
    if os.path.isdir(os.path.join(d, "Halo")):
        halo_drive = d
        break

if not halo_drive:
    raise RuntimeError("No se encontró el disco duro externo con Halo montado")

# Rutas
CARNAGES_DIRECTORY = os.path.join(halo_drive, "Halo", "Carnages")
DATABASE_PATH = os.path.join(halo_drive, "Halo", "DBStats DataBase", "dbstats.db")
PROCESSED_DIRECTORY = os.path.join(CARNAGES_DIRECTORY, "Processed")

print(f"Disco externo detectado en: {halo_drive}")
print(f"Carnages: {CARNAGES_DIRECTORY}")
print(f"DB: {DATABASE_PATH}")
