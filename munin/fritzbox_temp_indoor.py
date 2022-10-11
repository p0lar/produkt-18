#!/usr/bin/python3

import os
import sys

import fritzconnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

hostname = os.environ['hostname']
login = os.environ['auth_username']
password = os.environ['auth_password']
munin_category = "temp"
if 'category' in os.environ.keys():
    munin_category = os.environ['category']

fc = fritzconnection.FritzConnection(hostname, user=login, password=password)
fha = FritzHomeAutomation(fc=fc)

config = len(sys.argv) > 1 and sys.argv[1] == "config"

if config:
    sys.stdout.write("graph_title Ambient indoor temperatures\n")
    sys.stdout.write("graph_vlabel Temperature °C\n")
    sys.stdout.write(f"graph_category {munin_category}\n")
    
for entry in fha.device_information():
    if entry['NewTemperatureIsEnabled'] != "ENABLED":
        continue
    ain = entry['NewAIN']
    product_name = entry['NewProductName']
    descr = entry['NewDeviceName']
    temperature = "U"
    if entry['NewTemperatureIsValid']:
        temp_int = int(entry['NewTemperatureCelsius'])
        temperature = temp_int / 10.0
    ain_munin = "s" + ain.replace(" ", "")  # munin needs the data source start with a character

    if config:
        sys.stdout.write(f"{ain_munin}.label: {descr}\n")
        continue

    sys.stdout.write(f"{ain_munin}.value: {temperature}\n")
