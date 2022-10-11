#!/usr/bin/python3

import os
import sys
import subprocess

class Graph():

    def __init__(self, name=None, title=None, vlabel=None, category="default"):
        self._name = name # Name for multipgraph
        self._title = title
        self._vlabel = vlabel
        self._catgory = category
        self._datasources = {}

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

    def update_data(self, lines):
        for line in lines:
            if ("" == line):
                continue
            (keyw, value)= list(map(str.strip, line.split(":", 1)))
            data_point = value.split(" ", 1)[0]
            data_source = None
            if "LOADPCT" == keyw and "load" in self._datasources:
                data_source = "load"
            elif "LINEV" == keyw and "voltage_mains" in self._datasources:
                data_source = "voltage_mains"
            elif "TIMELEFT" == keyw and "time_left" in self._datasources:
                data_source = "time_left"
            
            if data_source is None:
                # Nothing found
                continue

            self._datasources[data_source]['value'] = data_point

        pass

munin_category = "usv"
if 'category' in os.environ.keys():
    munin_category = os.environ['category']

graphs = []

g_mains = Graph(name="usv_mains", title="USV mains", category=munin_category, vlabel="Mains voltage (V)")
g_mains.add_datasource(key='voltage_mains', label="Mains")

g_load = Graph(name="usv_load", title="USV load", category=munin_category, vlabel="Load (%)")
g_load.add_datasource(key='load', label="Load")

g_batt_timeleft = Graph(name="usv_batt_runtime", title="USV time left", category=munin_category, vlabel="Time left (minutes)")
g_batt_timeleft.add_datasource(key='time_left', label="Battery time left")

graphs.append(g_mains)
graphs.append(g_load)
graphs.append(g_batt_timeleft)

config = len(sys.argv) > 1 and sys.argv[1] == "config"

if config:
    for g in graphs:
        g.print_config()
    sys.exit(0)

# No config, fetch new data
apc_bin = '/usr/sbin/apcaccess'
if 'apc_bin' in os.environ.keys():
    apc_bin = os.environ['apc_bin']

p = subprocess.run([apc_bin, "status"], capture_output=True, encoding="UTF-8")
lines = p.stdout.split("\n")

for g in graphs:
    g.update_data(lines)
    g.print_values()
sys.exit(0)
