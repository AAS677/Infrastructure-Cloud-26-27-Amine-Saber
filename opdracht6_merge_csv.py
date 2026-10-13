import csv
from pathlib import Path

# 1. Configuratie van mappen en bestanden
huidige_map = Path(".")
uitvoer_bestand = "alle_systeeminformatie.csv"

# 2. Vaste standaardkolommen
standaard_kolommen = [
    "serienummer",
    "computernaam",
    "computermodel",
    "processor",
    "aantal_fysieke_cpu_cores",
    "maximale_cpu_frequentie_mhz",
    "totale_hoeveelheid_ram_gb",
    "bestandssysteem_opslag",
    "opslagcapaciteit_gb",
    "mac_adres_primaire_nic",
    "ipv4_adres_primaire_nic",
    "ipv6_adres_primaire_nic",
    "ipv6_link_local_adres_primaire_nic",
]

# 3. Automatisch alle relevante CSV-bestanden opsporen
# Sluit het uitvoerbestand zelf uit om duplicaten te vermijden
csv_bestanden = [
    bestand
    for bestand in huidige_map.glob("*.csv")
    if bestand.name != uitvoer_bestand
]

print(
    f"Gevonden invoerbestanden ({len(csv_bestanden)}):"
    f" {[b.name for b in csv_bestanden]}"
)

samengevoegde_data = []

# 4. Elk CSV-bestand inlezen en toevoegen aan de gezamenlijke lijst
for bestand in csv_bestanden:
    try:
        with open(bestand, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=",")

            for rij in reader:
                opgeschoonde_rij = {}

                for kolom in standaard_kolommen:
                    waarde = rij.get(kolom)

                    if waarde is None or waarde.strip() == "":
                        opgeschoonde_rij[kolom] = "N/A"
                    else:
                        opgeschoonde_rij[kolom] = waarde.strip()

                samengevoegde_data.append(opgeschoonde_rij)

        print(f"Succesvol verwerkt: {bestand.name}")

    except Exception as e:
        print(f"Fout bij verwerken van {bestand.name}: {e}")

# 5. Gezamenlijke dataset wegschrijven naar het nieuwe centrale CSV-bestand
with open(
    uitvoer_bestand,
    mode="w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=standaard_kolommen,
        delimiter=",",
        restval="N/A"
    )

    writer.writeheader()
    writer.writerows(samengevoegde_data)

print(
    f"\nSamenvoeging voltooid! "
    f"Totaal aantal rijen: {len(samengevoegde_data)}"
)

print(
    f"Resultaat opgeslagen in: {uitvoer_bestand}"
)