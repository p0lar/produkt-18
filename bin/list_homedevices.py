import argparse
import configparser
import fritzconnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

parser = argparse.ArgumentParser("Ambient sensor listing from a Fritz!Box")
parser.add_argument("--config", required=True, help="The configfile for accessing the FritzBox")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read_file(open(args.config))

# fc = fritzconnection.FritzConnection('uplink2.int.850nm.net', user='homebridge', password='homebridge1')
fc = fritzconnection.FritzConnection(config.get('node', 'hostname'), user=config.get('auth', 'username'), password=config.get('auth', 'password'))
# print(fc)
fha = FritzHomeAutomation(fc=fc)
# print(fha.device_information())
"""
{
    'NewAIN': '11630 0057153', 
    'NewDeviceId': 16, 
    'NewFunctionBitMask': 35712, 
    'NewFirmwareVersion': '04.25', 
    'NewManufacturer': 'AVM', 
    'NewProductName': 'FRITZ!DECT 200', 
    'NewDeviceName': 'Steckerleiste schwarz', 
    'NewPresent': 'CONNECTED', 
    'NewMultimeterIsEnabled': 'ENABLED', 
    'NewMultimeterIsValid': 'VALID', 
    'NewMultimeterPower': 4227, -> 42.55 W
    'NewMultimeterEnergy': 49308, -> 49308 Wh -> 49.3 kWh
    'NewTemperatureIsEnabled': 'ENABLED', 
    'NewTemperatureIsValid': 'VALID', 
    'NewTemperatureCelsius': 185, -> 18,5°
    'NewTemperatureOffset': 0, 
    'NewSwitchIsEnabled': 'ENABLED', 
    'NewSwitchIsValid': 'VALID', # Schaltbar
    'NewSwitchState': 'ON', 
    'NewSwitchMode': 'MANUAL', 
    'NewSwitchLock': True, 
    ## Hkr = Heizkörper
    'NewHkrIsEnabled': 'DISABLED', 
    'NewHkrIsValid': 'INVALID', 
    'NewHkrIsTemperature': 0, 
    'NewHkrSetVentilStatus': 'CLOSED', 
    'NewHkrSetTemperature': 0, 
    'NewHkrReduceVentilStatus': 'CLOSED', 
    'NewHkrReduceTemperature': 0, 
    'NewHkrComfortVentilStatus': 'CLOSED', 
    'NewHkrComfortTemperature': 0
}
"""

for entry in fha.device_information():
    ain = entry['NewAIN']
    product_name = entry['NewProductName']
    descr = entry['NewDeviceName']
    print(f"{ain} {product_name} {descr}")
