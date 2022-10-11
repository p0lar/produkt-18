#!/usr/bin/python3

import os
import sys

import fritzconnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

hostname = os.environ['hostname']
login = os.environ['auth_username']
password = os.environ['auth_password']
munin_category = "energy"
if 'category' in os.environ.keys():
    munin_category = os.environ['category']

fc = fritzconnection.FritzConnection(hostname, user=login, password=password)
fha = FritzHomeAutomation(fc=fc)

config = len(sys.argv) > 1 and sys.argv[1] == "config"

if config:
    sys.stdout.write("graph_title Total energy consumption\n")
    sys.stdout.write("graph_vlabel Energy (kWh)\n")
    sys.stdout.write(f"graph_category {munin_category}\n")
    
for entry in fha.device_information():
    if entry['NewTemperatureIsEnabled'] != "ENABLED":
        continue
    ain = entry['NewAIN']
    product_name = entry['NewProductName']
    descr = entry['NewDeviceName']
    consumption = "U"
    if entry['NewMultimeterIsValid'] == "VALID":
        consumption = int(entry['NewMultimeterEnergy']) / 1000.0
    ain_munin = "s" + ain.replace(" ", "")  # munin needs the data source start with a character

    if config:
        sys.stdout.write(f"{ain_munin}.label {descr}\n")
        sys.stdout.write(f"{ain_munin}.min 0\n")
        continue

    sys.stdout.write(f"{ain_munin}.value {consumption}\n")
