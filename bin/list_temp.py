import argparse
import configparser
import fritzconnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

parser = argparse.ArgumentParser("Ambient sensor listing from a Fritz!Box")
parser.add_argument("--config", required=True, help="The configfile for accessing the FritzBox")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read_file(open(args.config))

fc = fritzconnection.FritzConnection(config.get('node', 'hostname'), user=config.get('auth', 'username'), password=config.get('auth', 'password'))
fha = FritzHomeAutomation(fc=fc)
# print(fha.device_information())

for entry in fha.device_information():
    if entry['NewTemperatureIsEnabled'] != "ENABLED":
        continue
    ain = entry['NewAIN']
    product_name = entry['NewProductName']
    descr = entry['NewDeviceName']
    temperature = -1.0
    if entry['NewTemperatureIsValid']:
        temp_int = int(entry['NewTemperatureCelsius'])
        temperature = temp_int / 10.0

    # print(f"{ain} {product_name} {temperature}")
    print(f"{descr} {temperature}°C")

