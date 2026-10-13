import json
import platform
import socket
import psutil
import subprocess
from pprint import pprint


def get_serial_number():
  """Haalt het serienummer van de computer op."""
  try:
    serial = subprocess.check_output(
        [
            "powershell",
            "-Command",
            "(Get-CimInstance Win32_BIOS).SerialNumber"
        ],
        text=True
    ).strip()

    return serial

  except:
    return "Onbekend"


def get_primary_interface_info():
  """Identificeert de actieve netwerkinterface naar buiten."""
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    active_ip = s.getsockname()[0]
    s.close()
  except Exception:
    active_ip = "127.0.0.1"

  primary_nic = None
  addrs = psutil.net_if_addrs()

  for nic, addr_list in addrs.items():
    for addr in addr_list:
      if addr.family == socket.AF_INET and addr.address == active_ip:
        primary_nic = nic
        break

    if primary_nic:
      break

  mac = None
  ipv4 = None
  ipv6_global = None
  ipv6_link_local = None

  if primary_nic and primary_nic in addrs:
    for addr in addrs[primary_nic]:

      if addr.family == psutil.AF_LINK:
        mac = addr.address

      elif addr.family == socket.AF_INET:
        ipv4 = addr.address

      elif addr.family == socket.AF_INET6:
        clean_ip = addr.address.split("%")[0]

        if clean_ip.lower().startswith("fe80:"):
          ipv6_link_local = clean_ip
        else:
          ipv6_global = clean_ip

  return mac, ipv4, ipv6_global, ipv6_link_local


def filter_system_info():

  # Serienummer
  serienummer = get_serial_number()

  # Opslag
  root_mount = "C:\\" if platform.system() == "Windows" else "/"

  disk_fs = "Onbekend"

  for part in psutil.disk_partitions(all=False):
    if part.mountpoint == root_mount:
      disk_fs = part.fstype
      break

  disk_usage = psutil.disk_usage(root_mount)
  disk_total_gb = round(disk_usage.total / (1024**3), 2)

  # Netwerk
  mac, ipv4, ipv6_global, ipv6_ll = get_primary_interface_info()

  # CPU en RAM
  freq = psutil.cpu_freq()
  max_freq_mhz = round(freq.max, 2) if freq else None

  ram_gb = round(
      psutil.virtual_memory().total / (1024**3),
      2
  )

  return {
      "serienummer": serienummer,
      "computernaam": platform.node(),
      "computermodel": platform.machine(),
      "processor": platform.processor(),
      "aantal_fysieke_cpu_cores": psutil.cpu_count(logical=False),
      "maximale_cpu_frequentie_mhz": max_freq_mhz,
      "totale_hoeveelheid_ram_gb": ram_gb,
      "bestandssysteem_opslag": disk_fs,
      "opslagcapaciteit_gb": disk_total_gb,
      "mac_adres_primaire_nic": mac,
      "ipv4_adres_primaire_nic": ipv4,
      "ipv6_adres_primaire_nic": ipv6_global,
      "ipv6_link_local_adres_primaire_nic": ipv6_ll,
  }


if __name__ == "__main__":

  # 1. Informatie filteren
  resultaat = filter_system_info()

  print("--- GEFILTERDE SYSTEEMINFORMATIE ---")
  pprint(resultaat)

  # 2. Omzetten naar JSON en opslaan in een .json-bestand
  bestandsnaam = "systeeminformatie.json"

  with open(bestandsnaam, "w", encoding="utf-8") as json_bestand:
    json.dump(resultaat, json_bestand, indent=4)

  print(f"\nGegevens succesvol weggeschreven naar {bestandsnaam}")

  # 3. Bestand opnieuw inlezen als Python dictionary
  with open(bestandsnaam, "r", encoding="utf-8") as json_bestand:
    ingelezen_data = json.load(json_bestand)

  print("Gegevens succesvol opnieuw ingelezen.")

  # 4. Controle van de gegevens
  belangrijke_velden = [
      "serienummer",
      "computernaam",
      "processor",
      "totale_hoeveelheid_ram_gb",
      "opslagcapaciteit_gb",
      "ipv4_adres_primaire_nic",
      "mac_adres_primaire_nic",
  ]

  is_correct = True

  for veld in belangrijke_velden:
    origineel = resultaat.get(veld)
    ingelezen = ingelezen_data.get(veld)

    if origineel != ingelezen:
      print(
          f"Verschil gevonden bij {veld}: "
          f"{origineel} != {ingelezen}"
      )

      is_correct = False

  if is_correct:
    print(
        "Verificatie geslaagd: alle gecontroleerde velden zijn 100% identiek!"
    )