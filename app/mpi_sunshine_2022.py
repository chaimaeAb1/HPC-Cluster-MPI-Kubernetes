from mpi4py import MPI
import csv
import os
import socket

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

DATA_DIR = os.environ.get("DATA_DIR", "/weather_data")

FILES = sorted(os.listdir(DATA_DIR))

def parse_year(date_str: str) -> int | None:
    if not date_str:
        return None
    # On accepte plusieurs formats courants
    date_str = date_str.strip().replace("/", "-")
    parts = date_str.split("-")
    for part in parts:
        if len(part) == 4 and part.isdigit():
            try:
                return int(part)
            except:
                pass
    return None


def to_float(x: str) -> float:
    if not x:
        return 0.0
    x = x.strip().replace(",", ".")
    try:
        # Conversion secondes → heures
        return float(x) / 3600.0
    except:
        return 0.0


# Vérification nombre de processus
if size != len(FILES):
    if rank == 0:
        print(f"ERREUR : Il faut exactement {len(FILES)} processus MPI (actuel = {size})")
    comm.Abort(1)


#  Traitement par rang

hostname = socket.gethostname()
fname = FILES[rank]
path = os.path.join(DATA_DIR, fname)

total_sun_2022 = 0.0
count_days_2022 = 0

try:
    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            year = parse_year(row.get("Date", ""))
            if year == 2022:
                sunshine = to_float(row.get("Sunshine_Duration", ""))
                if sunshine > 0:  # on compte que les valeurs positives
                    total_sun_2022 += sunshine
                    count_days_2022 += 1

except Exception as e:
    if rank == 0:
        print(f"Erreur critique sur {fname} : {e}")

# Envoi résultat + hostname vers rank 0
result = (fname, total_sun_2022, count_days_2022, hostname)
all_results = comm.gather(result, root=0)


#  Affichage final (uniquement rank 0) 

if rank == 0:
    print("\n" + "═" * 80)
    print("   TOTAL HEURES D'ENSOLLEILLEMENT - ANNEE 2022")
    print("═" * 80)

    # Tri par nom de pays
    all_results.sort(key=lambda x: x[0].lower())

    pod_mapping = {}
    grand_total = 0.0
    total_days = 0

    for fname, sun_hours, days, hostname in all_results:
        country = fname.replace(".csv", "")
        print(f" {country:12} : {sun_hours:8.2f} h  ({days:3} jours)   → Pod: {hostname}")
        
        grand_total += sun_hours
        total_days += days
        
        pod_mapping.setdefault(hostname, []).append(country)

    print("═" * 80)
    print(f"  TOTAL GLOBAL : {grand_total:8.2f} heures")
    print(f"  MOYENNE / pays : {grand_total / len(FILES):8.2f} heures")
    print("═" * 80)

    print("\nRépartition par Pod :")
    for pod, countries in sorted(pod_mapping.items()):
        print(f"  {pod:16} → {', '.join(countries)}  ({len(countries)} pays)")
    
    print("═" * 80)
