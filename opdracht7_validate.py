import csv
import ipaddress
import re

csv_bestand = "alle_systeeminformatie.csv"

mac_patroon = re.compile(
    r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
)

try:
    with open(csv_bestand, mode="r", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for idx, rij in enumerate(reader, start=1):

            pc = rij.get("computernaam", f"Rij {idx}")

            print(f"\n--- Valideren van computer: {pc} ---")

            # 1. Controle serienummer
            serienummer = rij.get("serienummer")

            if serienummer and serienummer not in ["N/A", "Onbekend", ""]:
                print(
                    f"  [OK] Serienummer is aanwezig: {serienummer}"
                )
            else:
                print(
                    f"  [FOUT] Serienummer ontbreekt of is ongeldig: {serienummer}"
                )

            # 2. Controle computernaam
            computernaam = rij.get("computernaam")

            if computernaam and computernaam not in ["N/A", ""]:
                print(
                    f"  [OK] Computernaam is aanwezig: {computernaam}"
                )
            else:
                print(
                    "  [FOUT] Computernaam ontbreekt."
                )

            # 3. Controle processor
            processor = rij.get("processor")

            if processor and processor not in ["N/A", ""]:
                print(
                    f"  [OK] Processor is aanwezig: {processor}"
                )
            else:
                print(
                    "  [FOUT] Processor ontbreekt."
                )

            # 4. Controle IPv4
            ipv4 = rij.get("ipv4_adres_primaire_nic")

            try:
                ipaddress.IPv4Address(ipv4)

                print(
                    f"  [OK] IPv4 is geldig: {ipv4}"
                )

            except (ValueError, TypeError):

                print(
                    f"  [FOUT] Ongeldig IPv4-adres: {ipv4}"
                )

            # 5. Controle MAC-adres
            mac = rij.get("mac_adres_primaire_nic")

            if mac and mac_patroon.match(mac):

                print(
                    f"  [OK] MAC-formaat is correct: {mac}"
                )

            else:

                print(
                    f"  [FOUT] Ongeldig MAC-adres: {mac}"
                )

            # 6. Controle RAM-waarde
            try:

                ram = float(
                    rij.get("totale_hoeveelheid_ram_gb", 0)
                )

                if 2.0 <= ram <= 128.0:

                    print(
                        f"  [OK] RAM-waarde is realistisch: {ram} GB"
                    )

                else:

                    print(
                        f"  [WAARSCHUWING] "
                        f"Ongebruikelijke RAM-waarde: {ram} GB"
                    )

            except (ValueError, TypeError):

                print(
                    "  [FOUT] RAM kon niet naar getal worden omgezet."
                )

            # 7. Controle opslagcapaciteit
            try:

                opslag = float(
                    rij.get("opslagcapaciteit_gb", 0)
                )

                if opslag > 0:

                    print(
                        f"  [OK] Opslagcapaciteit is geldig: {opslag} GB"
                    )

                else:

                    print(
                        f"  [FOUT] Ongeldige opslagcapaciteit: {opslag} GB"
                    )

            except (ValueError, TypeError):

                print(
                    "  [FOUT] Opslagcapaciteit kon niet naar getal worden omgezet."
                )


except FileNotFoundError:

    print(
        f"Fout: Bestand '{csv_bestand}' niet gevonden. "
        "Voer eerst Opdracht 6 uit."
    )