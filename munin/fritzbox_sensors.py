#!/usr/bin/python3

import os
import sys
import subprocess

import fritzconnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

class Graph():

    def __init__(self, name=None, title=None, vlabel=None, category="default"):
        self._name = name # Name for multipgraph
        self._title = title
        self._vlabel = vlabel
        self._catgory = category
        self._datasources = {}

    def populate_sensors(
            self,
            check_attribute=None,
            data_attribute=None,
            data=None,
            base=1.0
        ):
        if (check_attribute is None or data_attribute is None or data is None):
            return
        for entry in data:
            if entry[check_attribute] != "VALID":
                continue
            sensor_key = "s" + entry['NewAIN'].replace(" ", "") # munin needs the data source start with a character and no blanks contained
            self.add_datasource(sensor_key, label=entry['NewDeviceName'])

            # Add the data here and now
            data = int(entry[data_attribute]) / base
            self._datasources[sensor_key]['value'] = data

    def add_datasource(self, key, label="No label", type="GAUGE", min=None):
        if key in self._datasources:
            return
        datasource = {}
        datasource['value'] = None # This is the actual data value
        datasource['label'] = label
        datasource['type'] = type
        if (min is not None):
            datasource['min'] = min
        self._datasources[key] = datasource

    def print_config(self):
        if (self._name is not None):
            sys.stdout.write(f"multigraph {self._name}\n")
        sys.stdout.write(f"graph_title {self._title}\n")
        sys.stdout.write(f"graph_vlabel {self._vlabel}\n")
        sys.stdout.write(f"graph_category {self._catgory}\n")
        for source_key in sorted(self._datasources.keys()):
            data_source = self._datasources[source_key]
            for property in sorted(data_source):
                if (property == "value"):
                    # No data for config
                    continue
                sys.stdout.write(f"{source_key}.{property} {data_source[property]}\n")
        sys.stdout.write(f"\n")

    def print_values(self):
        if (self._name is not None):
            sys.stdout.write(f"multigraph {self._name}\n")
        for source_key in sorted(self._datasources.keys()):
            data_source = self._datasources[source_key]
            for property in sorted(data_source):
                if (property == "value"):
                    sys.stdout.write(f"{source_key}.{property} {data_source[property]}\n")
                continue
        sys.stdout.write(f"\n")

hostname = os.environ['hostname']
login = os.environ['auth_username']
password = os.environ['auth_password']

fc = fritzconnection.FritzConnection(hostname, user=login, password=password)
fha = FritzHomeAutomation(fc=fc)
sensor_data = fha.device_information()

graphs = []

g_temp = Graph(name="fritz_temp_sensors", title="Ambient indoor temperatures", category="temp", vlabel="Temperature (°C)")
g_temp.populate_sensors(check_attribute="NewTemperatureIsValid", data_attribute="NewTemperatureCelsius", data=sensor_data, base=10.0)

g_power = Graph(name="fritz_power_sensors", title="Current power consumption", category="energy", vlabel="Power (Watts)")
g_power.populate_sensors(check_attribute="NewMultimeterIsValid", data_attribute="NewMultimeterPower", data=sensor_data, base=100.0)

g_total_energy = Graph(name="fritz_total_energy", title="Total energy consumption", category="energy", vlabel="Energy (kWh)")
g_total_energy.populate_sensors(check_attribute="NewMultimeterIsValid", data_attribute="NewMultimeterEnergy", data=sensor_data, base=1000.0)

graphs.append(g_temp)
graphs.append(g_power)
graphs.append(g_total_energy)

config = len(sys.argv) > 1 and sys.argv[1] == "config"

if config:
    for g in graphs:
        g.print_config()
    sys.exit(0)

# No config

for g in graphs:
    g.print_values()
sys.exit(0)