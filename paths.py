import os

external_drive_path = "/media/pi/MiDiscoExterno"

halo_directory_external = os.path.join(external_drive_path, "Halo")

CARNAGES_DIRECTORY = os.path.join(halo_directory_external, "Carnages")
DATABASE_PATH = os.path.join(halo_directory_external, "DBStats DataBase", "dbstats.db")
PROCESSED_DIRECTORY = os.path.join(CARNAGES_DIRECTORY, "Processed")

script_directory = os.path.dirname(os.path.abspath(__file__))

project_root_msd = os.path.join(script_directory, "..")

DBSTATS_EXE_PATH = os.path.join(project_root_msd, "DBStats", "bin", "Debug", "net9.0", "DBStats.exe")

print("Rutas en el disco duro externo:")
print(f"Directorio de Carnages: {CARNAGES_DIRECTORY}")
print(f"Ruta de la base de datos: {DATABASE_PATH}")
print(f"Directorio de procesados: {PROCESSED_DIRECTORY}")
print("\n")
print("Ruta en la tarjeta microSD:")
print(f"Ejecutable de DBStats: {DBSTATS_EXE_PATH}")