import os

media_path = "/media/maste"
drives = [os.path.join(media_path, d) for d in os.listdir(media_path)]
script_dir = os.path.dirname(os.path.abspath(__file__))
halo_drive = None


for d in drives:
    if os.path.isdir(os.path.join(d, "Halo")):
        halo_drive = d
        break

if not halo_drive:
    raise RuntimeError("External hard drive with Halo mounted was not found")

CARNAGES_DIRECTORY = os.path.join(halo_drive, "Halo", "Carnages")
DATABASE_PATH = os.path.join(halo_drive, "Halo", "DBStats DataBase", "dbstats.db")
PROCESSED_DIRECTORY = os.path.join(CARNAGES_DIRECTORY, "Processed")
DBSTATS_EXE_PATH = os.path.normpath(os.path.join(script_dir, "..", "DBStats", "publish", "DBStats.dll"))

print(f"Disco externo detectado en: {halo_drive}")
print(f"Carnages: {CARNAGES_DIRECTORY}")
print(f"DB: {DATABASE_PATH}")
