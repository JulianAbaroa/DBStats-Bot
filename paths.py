import os

home_directory = os.path.expanduser("~")
halo_directory = os.path.join(home_directory, "OneDrive", "Documents", "Halo")

DBSTATS_EXE_PATH = os.path.join(halo_directory, "DBStats", "bin", "Debug", "net9.0", "DBStats.exe")
DATABASE_PATH = os.path.join(halo_directory, "DBStats Database", "dbstats.db")
CARNAGES_DIRECTORY = os.path.join(home_directory, "Carnages")
PROCESSED_DIRECTORY = os.path.join(CARNAGES_DIRECTORY, "Processed")