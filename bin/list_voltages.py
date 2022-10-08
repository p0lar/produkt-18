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

for entry in fha.device_information():
    if entry['NewMultimeterIsEnabled'] != "ENABLED":
        continue
    ain = entry['NewAIN']
    product_name = entry['NewProductName']
    descr = entry['NewDeviceName']
    power = -1.0
    consumption = -1.0
    if entry['NewMultimeterIsValid']:
        power = int(entry['NewMultimeterPower']) / 100.0
        consumption = int(entry['NewMultimeterEnergy']) / 1000.0

    # print(f"{ain} {product_name} {temperature}")

    price = consumption * config.get('power', 'price_per_kwh', fallback=0.35)

    print(f"Consumption of {descr}: {power} Watts")
    print(f"Total energy used by {descr}: {consumption} kWh (approx {price:.2f} €)")
