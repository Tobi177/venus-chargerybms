#!/usr/bin/env python

import argparse
import gobject
import platform
import argparse
import logging
import sys
import os
import time
import datetime
import serial
import math
import struct
import decimal

# setup timezone
os.environ['TZ'] = 'Europe/Berlin'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


# connect and register to dbus
driver = {
	'name'        : "Chargery BMS",
	'servicename' : "chargerybms",
	'instance'    : 1,
	'id'          : 0x01,
	'version'     : 1.2,
	'serial'      : "CHGBMS11062020A1",
	'connection'  : "com.victronenergy.battery.ttyUSB0"
}


parser = argparse.ArgumentParser(description = 'Chargery BMS driver')
parser.add_argument('--version', action='version', version='%(prog)s v' + str(driver['version']) + ' (' + driver['serial'] + ')')
parser.add_argument('--debug', action="store_true", help='enable debug logging')
parser.add_argument('--test', action="store_true", help='test some stored examples network packets')
parser.add_argument('--victron', action="store_true", help='enable Victron DBUS support for VenusOS')
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument('-d', '--device', help='serial device for data (eg /dev/ttyUSB0)', required=True)
args = parser.parse_args()

if args.debug: # switch to debug level
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)


serial_port = serial.Serial(args.device, 115200, timeout=1)
serial_port.flushInput()
logging.info(serial_port.name)  


# victron stuff should be used
if args.victron:

	# Victron packages
	sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/velib_python'))
	from vedbus import VeDbusService


	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)

	dbusservice = VeDbusService(driver['connection'])

	# Create the management objects, as specified in the ccgx dbus-api document
	dbusservice.add_path('/Mgmt/ProcessName', __file__)
	dbusservice.add_path('/Mgmt/ProcessVersion', 'Unknown and Python ' + platform.python_version())
	dbusservice.add_path('/Mgmt/Connection', driver['connection'])

	# Create the mandatory objects
	dbusservice.add_path('/DeviceInstance',  driver['instance'])
	dbusservice.add_path('/ProductId',       driver['id'])
	dbusservice.add_path('/ProductName',     driver['name'])
	dbusservice.add_path('/FirmwareVersion', driver['version'])
	dbusservice.add_path('/HardwareVersion', driver['version'])
	dbusservice.add_path('/Serial',          driver['serial'])
	dbusservice.add_path('/Connected',       1)

	# Create device list
	dbusservice.add_path('/Devices/0/DeviceInstance',  driver['instance'])
	dbusservice.add_path('/Devices/0/FirmwareVersion', driver['version'])
	dbusservice.add_path('/Devices/0/ProductId',       driver['id'])
	dbusservice.add_path('/Devices/0/ProductName',     driver['name'])
	dbusservice.add_path('/Devices/0/ServiceName',     driver['servicename'])
	dbusservice.add_path('/Devices/0/VregLink',        "(API)")

	# Create the chargery bms paths
	dbusservice.add_path('/Info/Soc',                      -1)
	dbusservice.add_path('/Info/CurrentMode',              -1)
	dbusservice.add_path('/Info/Current',                  -1)
	dbusservice.add_path('/Info/Temp/Sensor1',             -1)
	dbusservice.add_path('/Info/Temp/Sensor2',             -1)
	dbusservice.add_path('/Info/ChargeEndVoltage',         -1)
	dbusservice.add_path('/Info/UpdateTimestamp',          -1)
	dbusservice.add_path('/Voltages/Cell1',                -1)
	dbusservice.add_path('/Voltages/Cell2',                -1)
	dbusservice.add_path('/Voltages/Cell3',                -1)
	dbusservice.add_path('/Voltages/Cell4',                -1)
	dbusservice.add_path('/Voltages/Cell5',                -1)
	dbusservice.add_path('/Voltages/Cell6',                -1)
	dbusservice.add_path('/Voltages/Cell7',                -1)
	dbusservice.add_path('/Voltages/Cell8',                -1)
	dbusservice.add_path('/Voltages/Cell9',                -1)
	dbusservice.add_path('/Voltages/Cell10',               -1)
	dbusservice.add_path('/Voltages/Cell11',               -1)
	dbusservice.add_path('/Voltages/Cell12',               -1)
	dbusservice.add_path('/Voltages/Cell13',               -1)
	dbusservice.add_path('/Voltages/Cell14',               -1)
	dbusservice.add_path('/Voltages/Cell15',               -1)
	dbusservice.add_path('/Voltages/Cell16',               -1)
	dbusservice.add_path('/Voltages/Cell17',               -1)
	dbusservice.add_path('/Voltages/Cell18',               -1)
	dbusservice.add_path('/Voltages/Cell19',               -1)
	dbusservice.add_path('/Voltages/Cell20',               -1)
	dbusservice.add_path('/Voltages/Cell21',               -1)
	dbusservice.add_path('/Voltages/Cell22',               -1)
	dbusservice.add_path('/Voltages/Cell23',               -1)
	dbusservice.add_path('/Voltages/Cell24',               -1)
	dbusservice.add_path('/Voltages/Sum',                  -1)
	dbusservice.add_path('/Voltages/Diff',                 -1)
	dbusservice.add_path('/Voltages/Max',                  -1)
	dbusservice.add_path('/Voltages/Min',                  -1)
	dbusservice.add_path('/Voltages/BatteryCapacityWH',    -1)
	dbusservice.add_path('/Voltages/BatteryCapacityAH',    -1)
	dbusservice.add_path('/Voltages/UpdateTimestamp',      -1)
	dbusservice.add_path('/Impedances/InstantCurrentMode', -1)
	dbusservice.add_path('/Impedances/InstantCurrent',     -1)
	dbusservice.add_path('/Impedances/Cell1',              -1)
	dbusservice.add_path('/Impedances/Cell2',              -1)
	dbusservice.add_path('/Impedances/Cell3',              -1)
	dbusservice.add_path('/Impedances/Cell4',              -1)
	dbusservice.add_path('/Impedances/Cell5',              -1)
	dbusservice.add_path('/Impedances/Cell6',              -1)
	dbusservice.add_path('/Impedances/Cell7',              -1)
	dbusservice.add_path('/Impedances/Cell8',              -1)
	dbusservice.add_path('/Impedances/Cell9',              -1)
	dbusservice.add_path('/Impedances/Cell10',             -1)
	dbusservice.add_path('/Impedances/Cell11',             -1)
	dbusservice.add_path('/Impedances/Cell12',             -1)
	dbusservice.add_path('/Impedances/Cell13',             -1)
	dbusservice.add_path('/Impedances/Cell14',             -1)
	dbusservice.add_path('/Impedances/Cell15',             -1)
	dbusservice.add_path('/Impedances/Cell16',             -1)
	dbusservice.add_path('/Impedances/Cell17',             -1)
	dbusservice.add_path('/Impedances/Cell18',             -1)
	dbusservice.add_path('/Impedances/Cell19',             -1)
	dbusservice.add_path('/Impedances/Cell20',             -1)
	dbusservice.add_path('/Impedances/Cell21',             -1)
	dbusservice.add_path('/Impedances/Cell22',             -1)
	dbusservice.add_path('/Impedances/Cell23',             -1)
	dbusservice.add_path('/Impedances/Cell24',             -1)
	dbusservice.add_path('/Impedances/Sum',                -1)
	dbusservice.add_path('/Impedances/Diff',               -1)
	dbusservice.add_path('/Impedances/Max',                -1)
	dbusservice.add_path('/Impedances/Min',                -1)
	dbusservice.add_path('/Impedances/UpdateTimestamp',    -1)


	# Create the real values paths
	dbusservice.add_path('/Raw/Info/Soc',                      -1)
	dbusservice.add_path('/Raw/Info/CurrentMode',              -1)
	dbusservice.add_path('/Raw/Info/Current',                  -1)
	dbusservice.add_path('/Raw/Info/Temp/Sensor1',             -1)
	dbusservice.add_path('/Raw/Info/Temp/Sensor2',             -1)
	dbusservice.add_path('/Raw/Info/ChargeEndVoltage',         -1)
	dbusservice.add_path('/Raw/Info/UpdateTimestamp',          -1)
	dbusservice.add_path('/Raw/Voltages/Cell1',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell2',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell3',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell4',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell5',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell6',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell7',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell8',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell9',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell10',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell11',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell12',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell13',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell14',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell15',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell16',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell17',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell18',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell19',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell20',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell21',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell22',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell23',               -1)
	dbusservice.add_path('/Raw/Voltages/Cell24',               -1)
	dbusservice.add_path('/Raw/Voltages/Sum',                  -1)
	dbusservice.add_path('/Raw/Voltages/Diff',                 -1)
	dbusservice.add_path('/Raw/Voltages/Max',                  -1)
	dbusservice.add_path('/Raw/Voltages/Min',                  -1)
	dbusservice.add_path('/Raw/Voltages/BatteryCapacityWH',    -1)
	dbusservice.add_path('/Raw/Voltages/BatteryCapacityAH',    -1)
	dbusservice.add_path('/Raw/Voltages/UpdateTimestamp',      -1)
	dbusservice.add_path('/Raw/Impedances/InstantCurrentMode', -1)
	dbusservice.add_path('/Raw/Impedances/InstantCurrent',     -1)
	dbusservice.add_path('/Raw/Impedances/Cell1',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell2',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell3',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell4',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell5',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell6',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell7',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell8',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell9',              -1)
	dbusservice.add_path('/Raw/Impedances/Cell10',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell11',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell12',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell13',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell14',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell15',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell16',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell17',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell18',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell19',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell20',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell21',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell22',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell23',             -1)
	dbusservice.add_path('/Raw/Impedances/Cell24',             -1)
	dbusservice.add_path('/Raw/Impedances/Sum',                -1)
	dbusservice.add_path('/Raw/Impedances/Diff',               -1)
	dbusservice.add_path('/Raw/Impedances/Max',                -1)
	dbusservice.add_path('/Raw/Impedances/Min',                -1)
	dbusservice.add_path('/Raw/Impedances/UpdateTimestamp',    -1)


PACKET_HEADER             = 0x24
PACKET_STATUS_CELLS       = 0x56
PACKET_STATUS_BMS         = 0x57
PACKET_STATUS_IMPEDANCES  = 0x58

PACKET_LENGTH_MINIMUM            = 15
PACKET_LENGTH_STATUS_CELLS       = [29, 45, 61]
PACKET_LENGTH_STATUS_BMS         = [15]
PACKET_LENGTH_STATUS_IMPEDANCES  = [24, 40, 56]


MIN_CELL_VOLTAGE   = 1.0
MIN_CELL_IMPEDANCE = 0.0

BMS_STATUS = {
	'bms' : { 
		'charged_end_voltage' : {
			'value' : -1.000,
			'text' : ""
		},
		'current_mode'        : {
			'value' : -1,
			'text'  : ""
		},
		'current' : {
			'value' : -1,
			'text' : ""
		},
		'temperature' : {
			'sensor_t1' : {
				'value' : -1.00,
				'text'  : ""
			},
			'sensor_t2' : {
				'value' : -1.00,
				'text'  : ""
			}
		},
		'soc' : {
			'value' : -1,
			'text'  : ""
		},
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		}
	},
	'voltages' : {
		'cell1_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell2_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell3_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell4_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell5_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell6_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell7_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell8_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell9_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell10_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell11_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell12_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell13_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell14_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell15_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell16_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell17_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell18_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell19_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell20_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell21_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell22_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell23_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell24_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'agg_voltages' : {
			'sum' : {
				'value' : -1,
				'text'  : ""
			},
			'max' : {
				'value' : -1,
				'text'  : ""
			},
			'min' : {
				'value' : -1,
				'text'  : ""
			},
			'diff' : {
				'value' : -1,
				'text'  : ""
			}
		},
		'battery_capacity_wh' : {
			'value' : -1,
			'text'  : ""
		},
		'battery_capacity_ah' : {
			'value' : -1,
			'text'  : ""
		},
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		}
	},
	'impedances' : {
		'cell1_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell2_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell3_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell4_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell5_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell6_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell7_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell8_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell9_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell10_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell11_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell12_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell13_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell14_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell15_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell16_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell17_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell18_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell19_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell20_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell21_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell22_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell23_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'cell24_impedance' : {
			'value' : -1,
			'text'  : ""
		},
		'agg_impedances' : {
			'sum' : {
				'value' : -1,
				'text'  : ""
			},
			'max' : {
				'value' : -1,
				'text'  : ""
			},
			'min' : {
				'value' : -1,
				'text'  : ""
			},
			'diff' : {
				'value' : -1,
				'text'  : ""
			}
		},
		'battery_capacity_wh' : {
			'value' : -1,
			'text'  : ""
		},
		'battery_capacity_ah' : {
			'value' : -1,
			'text'  : ""
		},
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		}
	}
	
}

# example network packets form the chargery community protocol manual v1.25
BMS_TEST_PACKETS = {
	1 : bytearray.fromhex('2424570F0E240100E6008100845B27'),
	2 : bytearray.fromhex('2424570F0E240100E4008100845B25'),
	3 : bytearray.fromhex('2424570F0E240100E1008300845B24'),
	4 : bytearray.fromhex('2424562D0CFD0D040D040D020D030D040D060D010D080D020D050CFE0D060CFB0D0F0CFC76FED50263140E0095'),
	5 : bytearray.fromhex('2424582801E4000100030003000300020003000000000001000100010000000500020003000300CC'),
	6 : bytearray.fromhex('2424570F0E240100E4008300845B27')
}


# define special unicode characters here
SPECIAL_DISPLAY_SYMBOLS = {
	'degree' : u'\u00b0',
	'ohm'    : u'\u03A9'
}

def debug_packet(packet):
	print
	for packet_byte in packet:
	 	print ord(packet_byte),"[",packet_byte.encode("hex"),"]",

	print
	print


def get_header_position(packet):

	# detect header position
	previous_packet_byte = "0"
	pos_iterator = -1
	for packet_byte in packet:
		pos_iterator += 1
		if ((ord(previous_packet_byte) == PACKET_HEADER) and (ord(packet_byte) == PACKET_HEADER)):
			break
		previous_packet_byte = packet_byte

	return pos_iterator


def get_voltage_value(byte1, byte2):
	return float((float(byte1 * 256) + float(byte2)) / 1000)


def get_current_value(byte1, byte2):
	return float((float(byte1 * 256) + float(byte2)) / 10)


def get_current1_value(byte1, byte2):
	return float((float(byte1) + float(byte2 * 256)) / 10)


def get_temperature_value(byte1, byte2):
	return float((float(byte1 * 256) + float(byte2)) / 10)
	
	
def get_battery_capacity(byte1, byte2, byte3, byte4):
	return float((float(byte1) + float(byte2 * 256) + float(byte3 * 256 * 256) + float(byte4 * 256 * 256 * 256)) / 1000)


def get_cell_impedance(byte1, byte2):
	return float((float(byte1) + float(byte2 * 256)) / 10)



def parse_packet(packet):
	logging.debug("Parse Packet [" + str(len(packet)) + "] bytes")

	while (len(packet) >= PACKET_LENGTH_MINIMUM): 
		header_position = get_header_position(packet)

		# now parse the packet	
		if ((header_position == -1) or (header_position == len(packet) - 1)):
			logging.debug("Packet Invalid")
			packet = ""
		else:
			# strip packet
			packet = packet[(header_position - 1):]
			
			if (len(packet) >= 4): 
				if ((ord(packet[0]) == PACKET_HEADER) and (ord(packet[1]) == PACKET_HEADER)):
					packet_length = ord(packet[3])
					logging.debug("Packet Length [" + str (packet_length) + " bytes]")
					# debug_packet(packet)
		
					if (ord(packet[2]) == PACKET_STATUS_BMS):
					
						if (len(packet) < PACKET_LENGTH_STATUS_BMS[0]):
							logging.debug("Packet Status BMS too short, skip")
							packet = ""
						else:

							# checksum value
							checksum = ord(packet[14])

							# calculate checksum
							checksum_check = (ord(packet[0])
								+ ord(packet[1]) + ord(packet[2])  + ord(packet[3])  + ord(packet[4])
								+ ord(packet[5]) + ord(packet[6])  + ord(packet[7])  + ord(packet[8])
								+ ord(packet[9]) + ord(packet[10]) + ord(packet[11]) + ord(packet[12])
								+ ord(packet[13])) % 256
							logging.debug("Packet Checksum : " + str(checksum) + "|" + str(checksum_check))
							
							# data integrity does match
							if (checksum == checksum_check):

								# charge end voltage
								BMS_STATUS['bms']['charged_end_voltage']['value'] = get_voltage_value(ord(packet[4]), ord(packet[5]))
								BMS_STATUS['bms']['charged_end_voltage']['text'] = "{:.2f}".format(BMS_STATUS['bms']['charged_end_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Info/ChargeEndVoltage"] = BMS_STATUS['bms']['charged_end_voltage']['text']
									dbusservice["/Raw/Info/ChargeEndVoltage"] = BMS_STATUS['bms']['charged_end_voltage']['value']

								# actual current
								BMS_STATUS['bms']['current']['value'] = get_current_value(ord(packet[7]), ord(packet[8]))

								# charge mode
								bms_charge_mode = ord(packet[6])
								if (bms_charge_mode == 0x00):
									BMS_STATUS['bms']['current_mode']['value'] = 0
									BMS_STATUS['bms']['current_mode']['text']  = "Discharge"
									BMS_STATUS['bms']['current']['text'] = "-" + str(BMS_STATUS['bms']['current']['value']) + "A"
								elif (bms_charge_mode == 0x01):
									BMS_STATUS['bms']['current_mode']['value'] = 1
									BMS_STATUS['bms']['current_mode']['text']  = "Charge"
									BMS_STATUS['bms']['current']['text'] = str(BMS_STATUS['bms']['current']['value']) + "A"
								elif (bms_charge_mode == 0x02):
									BMS_STATUS['bms']['current_mode']['value'] = 2
									BMS_STATUS['bms']['current_mode']['text']  = "Storage"
									BMS_STATUS['bms']['current']['text'] = str(BMS_STATUS['bms']['current']['value']) + "A"
								else:
									BMS_STATUS['bms']['current_mode']['value'] = -1
									BMS_STATUS['bms']['current_mode']['text']  = ""
									BMS_STATUS['bms']['current']['text'] = ""
								
								if args.victron:
									dbusservice["/Info/CurrentMode"] = BMS_STATUS['bms']['current_mode']['text']
									dbusservice["/Info/Current"]     = BMS_STATUS['bms']['current']['text']
									dbusservice["/Raw/Info/CurrentMode"] = BMS_STATUS['bms']['current_mode']['value']
									dbusservice["/Raw/Info/Current"]     = BMS_STATUS['bms']['current']['value']

								# current temperatures
								BMS_STATUS['bms']['temperature']['sensor_t1']['value'] = get_temperature_value(ord(packet[9]), ord(packet[10]))
								BMS_STATUS['bms']['temperature']['sensor_t1']['text'] = str(BMS_STATUS['bms']['temperature']['sensor_t1']['value']) + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"
								BMS_STATUS['bms']['temperature']['sensor_t2']['value'] = get_temperature_value(ord(packet[11]), ord(packet[12]))
								BMS_STATUS['bms']['temperature']['sensor_t2']['text'] = str(BMS_STATUS['bms']['temperature']['sensor_t2']['value']) + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"

								if args.victron:
									dbusservice["/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['text']
									dbusservice["/Info/Temp/Sensor2"] = BMS_STATUS['bms']['temperature']['sensor_t2']['text']
									dbusservice["/Raw/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['value']
									dbusservice["/Raw/Info/Temp/Sensor2"] = BMS_STATUS['bms']['temperature']['sensor_t2']['value']

								# soc value
								BMS_STATUS['bms']['soc']['value'] = ord(packet[13])
								BMS_STATUS['bms']['soc']['text'] = str(ord(packet[13])) + "%"
								if args.victron:
									dbusservice["/Info/Soc"] = BMS_STATUS['bms']['soc']['text']
									dbusservice["/Raw/Info/Soc"] = BMS_STATUS['bms']['soc']['value']
								
								# update timestamp
								current_date = datetime.datetime.now()
								BMS_STATUS['bms']['timestamp']['value'] = time.time()
								BMS_STATUS['bms']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
								if args.victron:
									dbusservice["/Info/UpdateTimestamp"] = BMS_STATUS['bms']['timestamp']['text']
									dbusservice["/Raw/Info/UpdateTimestamp"] = BMS_STATUS['bms']['timestamp']['value']


								# print (BMS_STATUS)
								logging.info("BMS status [SOC|" + BMS_STATUS['bms']['soc']['text'] +
									"][MODE|" + BMS_STATUS['bms']['current_mode']['text'] + 
									"][CURRENT|" + BMS_STATUS['bms']['current']['text'] + 
									"][T1|" + BMS_STATUS['bms']['temperature']['sensor_t1']['text'] + 
									"][T2|" + BMS_STATUS['bms']['temperature']['sensor_t1']['text'] + 
									"][MAX CHARGE VOLTAGE|" + BMS_STATUS['bms']['charged_end_voltage']['text'] + "]") 

							else:
								logging.info("Packet Checksum wrong, skip packet")

							# strip packet
							packet = packet[packet_length:]
			
					elif (ord(packet[2]) == PACKET_STATUS_CELLS):

						if (len(packet) < PACKET_LENGTH_STATUS_CELLS[0]):
							logging.debug("Packet Status Cells too short, skip")
							packet = ""
						else:

							# checksum value
							checksum       = 0
							checksum_check = -1

							if (packet_length == PACKET_LENGTH_STATUS_CELLS[0]): # packet from BMS8
								logging.debug("Packet Status Cells BMS8")

								if (len(packet) < PACKET_LENGTH_STATUS_CELLS[0]):
									logging.debug("Packet Status Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[28])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22]) + ord(packet[23]) + ord(packet[24]) + ord(packet[25])
										+ ord(packet[26]) + ord(packet[27])) % 256
									logging.debug("Packet Checksum BMS8: " + str(checksum) + "|" + str(checksum_check))
							
							elif (packet_length == PACKET_LENGTH_STATUS_CELLS[1]): # packet from BMS16
								logging.debug("Packet Status Cells BMS16")

								if (len(packet) < PACKET_LENGTH_STATUS_CELLS[1]):
									logging.debug("Packet Status Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[44])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22]) + ord(packet[23]) + ord(packet[24]) + ord(packet[25])
										+ ord(packet[26]) + ord(packet[27]) + ord(packet[28]) + ord(packet[29]) + ord(packet[30])
										+ ord(packet[31]) + ord(packet[32]) + ord(packet[33]) + ord(packet[34]) + ord(packet[35])
										+ ord(packet[36]) + ord(packet[37]) + ord(packet[38]) + ord(packet[39]) + ord(packet[40])
										+ ord(packet[41]) + ord(packet[42]) + ord(packet[43])) % 256
									logging.debug("Packet Checksum BMS16: " + str(checksum) + "|" + str(checksum_check))
							
							elif (packet_length == PACKET_LENGTH_STATUS_CELLS[2]): # packet from BMS24 
								logging.debug("Packet Status Cells BMS24")

								if (len(packet) < PACKET_LENGTH_STATUS_CELLS[2]):
									logging.debug("Packet Status Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[60])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22]) + ord(packet[23]) + ord(packet[24]) + ord(packet[25])
										+ ord(packet[26]) + ord(packet[27]) + ord(packet[28]) + ord(packet[29]) + ord(packet[30])
										+ ord(packet[31]) + ord(packet[32]) + ord(packet[33]) + ord(packet[34]) + ord(packet[35])
										+ ord(packet[36]) + ord(packet[37]) + ord(packet[38]) + ord(packet[39]) + ord(packet[40])
										+ ord(packet[41]) + ord(packet[42]) + ord(packet[43]) + ord(packet[44]) + ord(packet[45])
										+ ord(packet[46]) + ord(packet[47]) + ord(packet[48]) + ord(packet[49]) + ord(packet[50])
										+ ord(packet[51]) + ord(packet[52]) + ord(packet[53]) + ord(packet[54]) + ord(packet[55])
										+ ord(packet[56]) + ord(packet[57]) + ord(packet[58]) + ord(packet[59])) % 256
									logging.debug("Packet Checksum BMS16: " + str(checksum) + "|" + str(checksum_check))


							# data integrity does match
							if (checksum == checksum_check):


								# cell voltages BMS8
								BMS_STATUS['voltages']['cell1_voltage']['value'] = get_voltage_value(ord(packet[4]), ord(packet[5]))
								BMS_STATUS['voltages']['cell1_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell1_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell1"] = BMS_STATUS['voltages']['cell1_voltage']['text']
									dbusservice["/Raw/Voltages/Cell1"] = BMS_STATUS['voltages']['cell1_voltage']['value']

								BMS_STATUS['voltages']['cell2_voltage']['value'] = get_voltage_value(ord(packet[6]), ord(packet[7]))
								BMS_STATUS['voltages']['cell2_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell2_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell2"] = BMS_STATUS['voltages']['cell2_voltage']['text']
									dbusservice["/Raw/Voltages/Cell2"] = BMS_STATUS['voltages']['cell2_voltage']['value']

								BMS_STATUS['voltages']['cell3_voltage']['value'] = get_voltage_value(ord(packet[8]), ord(packet[9]))
								BMS_STATUS['voltages']['cell3_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell3_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell3"] = BMS_STATUS['voltages']['cell3_voltage']['text']
									dbusservice["/Raw/Voltages/Cell3"] = BMS_STATUS['voltages']['cell3_voltage']['value']

								BMS_STATUS['voltages']['cell4_voltage']['value'] = get_voltage_value(ord(packet[10]), ord(packet[11]))
								BMS_STATUS['voltages']['cell4_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell4_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell4"] = BMS_STATUS['voltages']['cell4_voltage']['text']
									dbusservice["/Raw/Voltages/Cell4"] = BMS_STATUS['voltages']['cell4_voltage']['value']

								BMS_STATUS['voltages']['cell5_voltage']['value'] = get_voltage_value(ord(packet[12]), ord(packet[13]))
								BMS_STATUS['voltages']['cell5_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell5_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell5"] = BMS_STATUS['voltages']['cell5_voltage']['text']
									dbusservice["/Raw/Voltages/Cell5"] = BMS_STATUS['voltages']['cell5_voltage']['value']

								BMS_STATUS['voltages']['cell6_voltage']['value'] = get_voltage_value(ord(packet[14]), ord(packet[15]))
								BMS_STATUS['voltages']['cell6_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell6_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell6"] = BMS_STATUS['voltages']['cell6_voltage']['text']
									dbusservice["/Raw/Voltages/Cell6"] = BMS_STATUS['voltages']['cell6_voltage']['value']

								BMS_STATUS['voltages']['cell7_voltage']['value'] = get_voltage_value(ord(packet[16]), ord(packet[17]))
								BMS_STATUS['voltages']['cell7_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell7_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell7"] = BMS_STATUS['voltages']['cell7_voltage']['text']
									dbusservice["/Raw/Voltages/Cell7"] = BMS_STATUS['voltages']['cell7_voltage']['value']

								BMS_STATUS['voltages']['cell8_voltage']['value'] = get_voltage_value(ord(packet[18]), ord(packet[19]))
								BMS_STATUS['voltages']['cell8_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell8_voltage']['value']) + "V"
								if args.victron:
									dbusservice["/Voltages/Cell8"] = BMS_STATUS['voltages']['cell8_voltage']['text']
									dbusservice["/Raw/Voltages/Cell8"] = BMS_STATUS['voltages']['cell8_voltage']['value']

								if (packet_length == PACKET_LENGTH_STATUS_CELLS[1]): # packet from BMS16

									BMS_STATUS['voltages']['cell9_voltage']['value'] = get_voltage_value(ord(packet[20]), ord(packet[21]))
									BMS_STATUS['voltages']['cell9_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell9_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell9"] = BMS_STATUS['voltages']['cell9_voltage']['text']
										dbusservice["/Raw/Voltages/Cell9"] = BMS_STATUS['voltages']['cell9_voltage']['value']

									BMS_STATUS['voltages']['cell10_voltage']['value'] = get_voltage_value(ord(packet[22]), ord(packet[23]))
									BMS_STATUS['voltages']['cell10_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell10_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell10"] = BMS_STATUS['voltages']['cell10_voltage']['text']
										dbusservice["/Raw/Voltages/Cell10"] = BMS_STATUS['voltages']['cell10_voltage']['value']

									BMS_STATUS['voltages']['cell11_voltage']['value'] = get_voltage_value(ord(packet[24]), ord(packet[25]))
									BMS_STATUS['voltages']['cell11_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell11_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell11"] = BMS_STATUS['voltages']['cell11_voltage']['text']
										dbusservice["/Raw/Voltages/Cell11"] = BMS_STATUS['voltages']['cell11_voltage']['value']

									BMS_STATUS['voltages']['cell12_voltage']['value'] = get_voltage_value(ord(packet[26]), ord(packet[27]))
									BMS_STATUS['voltages']['cell12_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell12_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell12"] = BMS_STATUS['voltages']['cell12_voltage']['text']
										dbusservice["/Raw/Voltages/Cell12"] = BMS_STATUS['voltages']['cell12_voltage']['value']

									BMS_STATUS['voltages']['cell13_voltage']['value'] = get_voltage_value(ord(packet[28]), ord(packet[29]))
									BMS_STATUS['voltages']['cell13_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell13_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell13"] = BMS_STATUS['voltages']['cell13_voltage']['text']
										dbusservice["/Raw/Voltages/Cell13"] = BMS_STATUS['voltages']['cell13_voltage']['value']

									BMS_STATUS['voltages']['cell14_voltage']['value'] = get_voltage_value(ord(packet[30]), ord(packet[31]))
									BMS_STATUS['voltages']['cell14_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell14_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell14"] = BMS_STATUS['voltages']['cell14_voltage']['text']
										dbusservice["/Raw/Voltages/Cell14"] = BMS_STATUS['voltages']['cell14_voltage']['value']

									BMS_STATUS['voltages']['cell15_voltage']['value'] = get_voltage_value(ord(packet[32]), ord(packet[33]))
									BMS_STATUS['voltages']['cell15_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell15_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell15"] = BMS_STATUS['voltages']['cell15_voltage']['text']
										dbusservice["/Raw/Voltages/Cell15"] = BMS_STATUS['voltages']['cell15_voltage']['value']

									BMS_STATUS['voltages']['cell16_voltage']['value'] = get_voltage_value(ord(packet[34]), ord(packet[35]))
									BMS_STATUS['voltages']['cell16_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell16_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell16"] = BMS_STATUS['voltages']['cell16_voltage']['text']
										dbusservice["/Raw/Voltages/Cell16"] = BMS_STATUS['voltages']['cell16_voltage']['value']


								if (packet_length == PACKET_LENGTH_STATUS_CELLS[2]): # packet from BMS24

									BMS_STATUS['voltages']['cell17_voltage']['value'] = get_voltage_value(ord(packet[36]), ord(packet[37]))
									BMS_STATUS['voltages']['cell17_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell17_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell17"] = BMS_STATUS['voltages']['cell17_voltage']['text']
										dbusservice["/Raw/Voltages/Cell17"] = BMS_STATUS['voltages']['cell17_voltage']['value']

									BMS_STATUS['voltages']['cell18_voltage']['value'] = get_voltage_value(ord(packet[38]), ord(packet[39]))
									BMS_STATUS['voltages']['cell18_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell18_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell18"] = BMS_STATUS['voltages']['cell18_voltage']['text']
										dbusservice["/Raw/Voltages/Cell18"] = BMS_STATUS['voltages']['cell18_voltage']['value']

									BMS_STATUS['voltages']['cell19_voltage']['value'] = get_voltage_value(ord(packet[40]), ord(packet[41]))
									BMS_STATUS['voltages']['cell19_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell19_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell19"] = BMS_STATUS['voltages']['cell19_voltage']['text']
										dbusservice["/Raw/Voltages/Cell19"] = BMS_STATUS['voltages']['cell19_voltage']['value']

									BMS_STATUS['voltages']['cell20_voltage']['value'] = get_voltage_value(ord(packet[42]), ord(packet[43]))
									BMS_STATUS['voltages']['cell20_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell20_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell20"] = BMS_STATUS['voltages']['cell20_voltage']['text']
										dbusservice["/Raw/Voltages/Cell20"] = BMS_STATUS['voltages']['cell20_voltage']['value']

									BMS_STATUS['voltages']['cell21_voltage']['value'] = get_voltage_value(ord(packet[44]), ord(packet[45]))
									BMS_STATUS['voltages']['cell21_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell21_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell21"] = BMS_STATUS['voltages']['cell21_voltage']['text']
										dbusservice["/Raw/Voltages/Cell21"] = BMS_STATUS['voltages']['cell21_voltage']['value']

									BMS_STATUS['voltages']['cell22_voltage']['value'] = get_voltage_value(ord(packet[46]), ord(packet[47]))
									BMS_STATUS['voltages']['cell22_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell22_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell22"] = BMS_STATUS['voltages']['cell22_voltage']['text']
										dbusservice["/Raw/Voltages/Cell22"] = BMS_STATUS['voltages']['cell22_voltage']['value']

									BMS_STATUS['voltages']['cell23_voltage']['value'] = get_voltage_value(ord(packet[48]), ord(packet[49]))
									BMS_STATUS['voltages']['cell23_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell23_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell23"] = BMS_STATUS['voltages']['cell23_voltage']['text']
										dbusservice["/Raw/Voltages/Cell23"] = BMS_STATUS['voltages']['cell23_voltage']['value']

									BMS_STATUS['voltages']['cell24_voltage']['value'] = get_voltage_value(ord(packet[50]), ord(packet[51]))
									BMS_STATUS['voltages']['cell24_voltage']['text'] = "{:.3f}".format(BMS_STATUS['voltages']['cell24_voltage']['value']) + "V"
									if args.victron:
										dbusservice["/Voltages/Cell24"] = BMS_STATUS['voltages']['cell24_voltage']['text']
										dbusservice["/Raw/Voltages/Cell24"] = BMS_STATUS['voltages']['cell24_voltage']['value']
								
									

								# get min/max voltages to calculate the diff
								cell_voltages = []

								if (BMS_STATUS['voltages']['cell1_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell1_voltage']['value'])
								if (BMS_STATUS['voltages']['cell2_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell2_voltage']['value'])
								if (BMS_STATUS['voltages']['cell3_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell3_voltage']['value'])
								if (BMS_STATUS['voltages']['cell4_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell4_voltage']['value'])
								if (BMS_STATUS['voltages']['cell5_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell5_voltage']['value'])
								if (BMS_STATUS['voltages']['cell6_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell6_voltage']['value'])
								if (BMS_STATUS['voltages']['cell7_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell7_voltage']['value'])
								if (BMS_STATUS['voltages']['cell8_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell8_voltage']['value'])
								if (BMS_STATUS['voltages']['cell9_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell9_voltage']['value'])
								if (BMS_STATUS['voltages']['cell10_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell10_voltage']['value'])
								if (BMS_STATUS['voltages']['cell11_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell11_voltage']['value'])
								if (BMS_STATUS['voltages']['cell12_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell12_voltage']['value'])
								if (BMS_STATUS['voltages']['cell13_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell13_voltage']['value'])
								if (BMS_STATUS['voltages']['cell14_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell14_voltage']['value'])
								if (BMS_STATUS['voltages']['cell15_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell15_voltage']['value'])
								if (BMS_STATUS['voltages']['cell16_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell16_voltage']['value'])
								if (BMS_STATUS['voltages']['cell17_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell17_voltage']['value'])
								if (BMS_STATUS['voltages']['cell18_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell18_voltage']['value'])
								if (BMS_STATUS['voltages']['cell19_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell19_voltage']['value'])
								if (BMS_STATUS['voltages']['cell20_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell20_voltage']['value'])
								if (BMS_STATUS['voltages']['cell21_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell21_voltage']['value'])
								if (BMS_STATUS['voltages']['cell22_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell22_voltage']['value'])
								if (BMS_STATUS['voltages']['cell23_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell23_voltage']['value'])
								if (BMS_STATUS['voltages']['cell24_voltage']['value'] >= MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['voltages']['cell24_voltage']['value'])
									
								BMS_STATUS['voltages']['agg_voltages']['sum']['value']  = sum(cell_voltages)
								BMS_STATUS['voltages']['agg_voltages']['sum']['text']   = "{:.2f}".format(BMS_STATUS['voltages']['agg_voltages']['sum']['value']) + "V" 
								BMS_STATUS['voltages']['agg_voltages']['max']['value']  = max(cell_voltages)
								BMS_STATUS['voltages']['agg_voltages']['max']['text']   = "{:.3f}".format(BMS_STATUS['voltages']['agg_voltages']['max']['value']) + "V" 
								BMS_STATUS['voltages']['agg_voltages']['min']['value']  = min(cell_voltages)
								BMS_STATUS['voltages']['agg_voltages']['min']['text']   = "{:.3f}".format(BMS_STATUS['voltages']['agg_voltages']['min']['value']) + "V" 
								BMS_STATUS['voltages']['agg_voltages']['diff']['value'] = BMS_STATUS['voltages']['agg_voltages']['max']['value'] - BMS_STATUS['voltages']['agg_voltages']['min']['value']
								BMS_STATUS['voltages']['agg_voltages']['diff']['text']  = "{:.0f}".format(BMS_STATUS['voltages']['agg_voltages']['diff']['value'] * 1000) + "mV"

								if args.victron:
									dbusservice["/Voltages/Sum"]      = BMS_STATUS['voltages']['agg_voltages']['sum']['text']
									dbusservice["/Raw/Voltages/Sum"]  = BMS_STATUS['voltages']['agg_voltages']['sum']['value']
									dbusservice["/Voltages/Max"]      = BMS_STATUS['voltages']['agg_voltages']['max']['text']
									dbusservice["/Raw/Voltages/Max"]  = BMS_STATUS['voltages']['agg_voltages']['max']['value']
									dbusservice["/Voltages/Min"]      = BMS_STATUS['voltages']['agg_voltages']['min']['text']
									dbusservice["/Raw/Voltages/Min"]  = BMS_STATUS['voltages']['agg_voltages']['min']['value']
									dbusservice["/Voltages/Diff"]     = BMS_STATUS['voltages']['agg_voltages']['diff']['text']
									dbusservice["/Raw/Voltages/Diff"] = BMS_STATUS['voltages']['agg_voltages']['diff']['value']


								if (packet_length == PACKET_LENGTH_STATUS_CELLS[0]): # packet from BMS8

									# get battery capacity
									BMS_STATUS['voltages']['battery_capacity_wh']['value'] = get_battery_capacity(ord(packet[20]), ord(packet[21]), ord(packet[22]), ord(packet[23]))
									BMS_STATUS['voltages']['battery_capacity_wh']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_wh']['value']) + "Wh"
									if args.victron:
										dbusservice["/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['value']

									BMS_STATUS['voltages']['battery_capacity_ah']['value'] = get_battery_capacity(ord(packet[24]), ord(packet[25]), ord(packet[26]), ord(packet[27]))
									BMS_STATUS['voltages']['battery_capacity_ah']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_ah']['value']) + "Ah"
									if args.victron:
										dbusservice["/Voltages/BatteryCapacityAH"] = BMS_STATUS['voltages']['battery_capacity_ah']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_ah']['value']


								elif (packet_length == PACKET_LENGTH_STATUS_CELLS[1]): # packet from BMS16

									# get battery capacity
									BMS_STATUS['voltages']['battery_capacity_wh']['value'] = get_battery_capacity(ord(packet[36]), ord(packet[37]), ord(packet[38]), ord(packet[39]))
									BMS_STATUS['voltages']['battery_capacity_wh']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_wh']['value']) + "Wh"
									if args.victron:
										dbusservice["/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['value']

									BMS_STATUS['voltages']['battery_capacity_ah']['value'] = get_battery_capacity(ord(packet[40]), ord(packet[41]), ord(packet[42]), ord(packet[43]))
									BMS_STATUS['voltages']['battery_capacity_ah']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_ah']['value']) + "Ah"
									if args.victron:
										dbusservice["/Voltages/BatteryCapacityAH"] = BMS_STATUS['voltages']['battery_capacity_ah']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_ah']['value']


								elif (packet_length == PACKET_LENGTH_STATUS_CELLS[2]): # packet from BMS24

									# get battery capacity
									BMS_STATUS['voltages']['battery_capacity_wh']['value'] = get_battery_capacity(ord(packet[52]), ord(packet[53]), ord(packet[54]), ord(packet[55]))
									BMS_STATUS['voltages']['battery_capacity_wh']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_wh']['value']) + "Wh"
									if args.victron:									
										dbusservice["/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['value']

									BMS_STATUS['voltages']['battery_capacity_ah']['value'] = get_battery_capacity(ord(packet[56]), ord(packet[57]), ord(packet[58]), ord(packet[59]))
									BMS_STATUS['voltages']['battery_capacity_ah']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_ah']['value']) + "Ah"
									if args.victron:
										dbusservice["/Voltages/BatteryCapacityAH"] = BMS_STATUS['voltages']['battery_capacity_ah']['text']
										dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_ah']['value']


								
								# update timestamp
								current_date = datetime.datetime.now()
								BMS_STATUS['voltages']['timestamp']['value'] = time.time()
								BMS_STATUS['voltages']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
								if args.victron:
									dbusservice["/Voltages/UpdateTimestamp"] = BMS_STATUS['voltages']['timestamp']['text']
									dbusservice["/Raw/Voltages/UpdateTimestamp"] = BMS_STATUS['voltages']['timestamp']['value']
									

								# print (BMS_STATUS)
								if (packet_length == PACKET_LENGTH_STATUS_CELLS[0]): # packet from BMS8
								
									logging.info("BMS8 cells " +
										"[CAPACITYAH|" + BMS_STATUS['voltages']['battery_capacity_ah']['text'] +
										"][CAPACITYWH|" + BMS_STATUS['voltages']['battery_capacity_wh']['text'] +
										"][DIFF|" + BMS_STATUS['voltages']['agg_voltages']['diff']['text'] +
										"][SUM|" + BMS_STATUS['voltages']['agg_voltages']['sum']['text'] +
										"][#1|"  + BMS_STATUS['voltages']['cell1_voltage']['text'] +
										"][#2|"  + BMS_STATUS['voltages']['cell2_voltage']['text'] + 
										"][#3|"  + BMS_STATUS['voltages']['cell3_voltage']['text'] + 
										"][#4|"  + BMS_STATUS['voltages']['cell4_voltage']['text'] +
										"][#5|"  + BMS_STATUS['voltages']['cell5_voltage']['text'] +
										"][#6|"  + BMS_STATUS['voltages']['cell6_voltage']['text'] +
										"][#7|"  + BMS_STATUS['voltages']['cell7_voltage']['text'] +
										"][#8|"  + BMS_STATUS['voltages']['cell8_voltage']['text'] + "]")

								elif (packet_length == PACKET_LENGTH_STATUS_CELLS[1]): # packet from BMS16

									logging.info("BMS16 cells " +
										"[CAPACITYAH|" + BMS_STATUS['voltages']['battery_capacity_ah']['text'] +
										"][CAPACITYWH|" + BMS_STATUS['voltages']['battery_capacity_wh']['text'] +
										"][DIFF|" + BMS_STATUS['voltages']['agg_voltages']['diff']['text'] +
										"][SUM|"  + BMS_STATUS['voltages']['agg_voltages']['sum']['text'] +
										"][#1|"   + BMS_STATUS['voltages']['cell1_voltage']['text'] +
										"][#2|"   + BMS_STATUS['voltages']['cell2_voltage']['text'] + 
										"][#3|"   + BMS_STATUS['voltages']['cell3_voltage']['text'] + 
										"][#4|"   + BMS_STATUS['voltages']['cell4_voltage']['text'] +
										"][#5|"   + BMS_STATUS['voltages']['cell5_voltage']['text'] +
										"][#6|"   + BMS_STATUS['voltages']['cell6_voltage']['text'] +
										"][#7|"   + BMS_STATUS['voltages']['cell7_voltage']['text'] +
										"][#8|"   + BMS_STATUS['voltages']['cell8_voltage']['text'] +
										"][#9|"   + BMS_STATUS['voltages']['cell9_voltage']['text'] + 
										"][#10|"  + BMS_STATUS['voltages']['cell10_voltage']['text'] + 
										"][#11|"  + BMS_STATUS['voltages']['cell11_voltage']['text'] +
										"][#12|"  + BMS_STATUS['voltages']['cell12_voltage']['text'] +
										"][#13|"  + BMS_STATUS['voltages']['cell13_voltage']['text'] +
										"][#14|"  + BMS_STATUS['voltages']['cell14_voltage']['text'] +
										"][#15|"  + BMS_STATUS['voltages']['cell15_voltage']['text'] +
										"][#16|"  + BMS_STATUS['voltages']['cell16_voltage']['text'] + "]")
								

								elif (packet_length == PACKET_LENGTH_STATUS_CELLS[2]): # packet from BMS24

									logging.info("BMS24 cells " +
										"[CAPACITYAH|" + BMS_STATUS['voltages']['battery_capacity_ah']['text'] +
										"][CAPACITYWH|" + BMS_STATUS['voltages']['battery_capacity_wh']['text'] +
										"][DIFF|" + BMS_STATUS['voltages']['agg_voltages']['diff']['text'] +
										"][SUM|"  + BMS_STATUS['voltages']['agg_voltages']['sum']['text'] +
										"][#1|"   + BMS_STATUS['voltages']['cell1_voltage']['text'] +
										"][#2|"   + BMS_STATUS['voltages']['cell2_voltage']['text'] + 
										"][#3|"   + BMS_STATUS['voltages']['cell3_voltage']['text'] + 
										"][#4|"   + BMS_STATUS['voltages']['cell4_voltage']['text'] +
										"][#5|"   + BMS_STATUS['voltages']['cell5_voltage']['text'] +
										"][#6|"   + BMS_STATUS['voltages']['cell6_voltage']['text'] +
										"][#7|"   + BMS_STATUS['voltages']['cell7_voltage']['text'] +
										"][#8|"   + BMS_STATUS['voltages']['cell8_voltage']['text'] +
										"][#9|"   + BMS_STATUS['voltages']['cell9_voltage']['text'] + 
										"][#10|"  + BMS_STATUS['voltages']['cell10_voltage']['text'] + 
										"][#11|"  + BMS_STATUS['voltages']['cell11_voltage']['text'] +
										"][#12|"  + BMS_STATUS['voltages']['cell12_voltage']['text'] +
										"][#13|"  + BMS_STATUS['voltages']['cell13_voltage']['text'] +
										"][#14|"  + BMS_STATUS['voltages']['cell14_voltage']['text'] +
										"][#15|"  + BMS_STATUS['voltages']['cell15_voltage']['text'] +
										"][#16|"  + BMS_STATUS['voltages']['cell16_voltage']['text'] + 
										"][#17|"  + BMS_STATUS['voltages']['cell17_voltage']['text'] +
										"][#18|"  + BMS_STATUS['voltages']['cell18_voltage']['text'] +
										"][#19|"  + BMS_STATUS['voltages']['cell19_voltage']['text'] +
										"][#20|"  + BMS_STATUS['voltages']['cell20_voltage']['text'] +
										"][#21|"  + BMS_STATUS['voltages']['cell21_voltage']['text'] +
										"][#22|"  + BMS_STATUS['voltages']['cell22_voltage']['text'] +
										"][#23|"  + BMS_STATUS['voltages']['cell23_voltage']['text'] +
										"][#24|"  + BMS_STATUS['voltages']['cell24_voltage']['text'] + "]")

							else:
								logging.debug("Packet Checksum wrong, skip packet")

							# strip packet
							packet = packet[packet_length:]

					elif (ord(packet[2]) == PACKET_STATUS_IMPEDANCES):

						if (len(packet) < PACKET_LENGTH_STATUS_IMPEDANCES[0]):
							logging.debug("Packet Impedances Cells too short, skip")
							packet = ""
						else:

							# checksum value
							checksum       = 0
							checksum_check = -1

							if (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[0]): # packet from BMS8
								logging.debug("Packet Impedances Cells BMS8")

								if (len(packet) < PACKET_LENGTH_STATUS_IMPEDANCES[0]):
									logging.debug("Packet Impedances Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[23])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22])) % 256
									logging.debug("Packet Checksum BMS8: " + str(checksum) + "|" + str(checksum_check))
							
							elif (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[1]): # packet from BMS16
								logging.debug("Packet Impedances Cells BMS16")

								if (len(packet) < PACKET_LENGTH_STATUS_IMPEDANCES[1]):
									logging.debug("Packet Impedances Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[39])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22]) + ord(packet[23]) + ord(packet[24]) + ord(packet[25])
										+ ord(packet[26]) + ord(packet[27]) + ord(packet[28]) + ord(packet[29]) + ord(packet[30])
										+ ord(packet[31]) + ord(packet[32]) + ord(packet[33]) + ord(packet[34]) + ord(packet[35])
										+ ord(packet[36]) + ord(packet[37]) + ord(packet[38])) % 256
									logging.debug("Packet Checksum BMS16: " + str(checksum) + "|" + str(checksum_check))
							
							elif (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[2]): # packet from BMS24 
								logging.debug("Packet Impedances Cells BMS24")

								if (len(packet) < PACKET_LENGTH_STATUS_IMPEDANCES[2]):
									logging.debug("Packet Impedances Cells too short, skip")
									packet = ""
								else:

									# checksum value
									checksum = ord(packet[55])

									# calculate checksum
									checksum_check = (ord(packet[0])
										+ ord(packet[1])  + ord(packet[2])  + ord(packet[3])  + ord(packet[4])  + ord(packet[5])
										+ ord(packet[6])  + ord(packet[7])  + ord(packet[8])  + ord(packet[9])  + ord(packet[10])
										+ ord(packet[11]) + ord(packet[12]) + ord(packet[13]) + ord(packet[14]) + ord(packet[15])
										+ ord(packet[16]) + ord(packet[17]) + ord(packet[18]) + ord(packet[19]) + ord(packet[20])
										+ ord(packet[21]) + ord(packet[22]) + ord(packet[23]) + ord(packet[24]) + ord(packet[25])
										+ ord(packet[26]) + ord(packet[27]) + ord(packet[28]) + ord(packet[29]) + ord(packet[30])
										+ ord(packet[31]) + ord(packet[32]) + ord(packet[33]) + ord(packet[34]) + ord(packet[35])
										+ ord(packet[36]) + ord(packet[37]) + ord(packet[38]) + ord(packet[39]) + ord(packet[40])
										+ ord(packet[41]) + ord(packet[42]) + ord(packet[43]) + ord(packet[44]) + ord(packet[45])
										+ ord(packet[46]) + ord(packet[47]) + ord(packet[48]) + ord(packet[49]) + ord(packet[50])
										+ ord(packet[51]) + ord(packet[52]) + ord(packet[53]) + ord(packet[54])) % 256
									logging.debug("Packet Checksum BMS16: " + str(checksum) + "|" + str(checksum_check))


							# data integrity does match
							if (checksum == checksum_check):

								# cell impedances BMS8
								BMS_STATUS['impedances']['cell1_impedance']['value'] = get_cell_impedance(ord(packet[7]), ord(packet[8]))
								BMS_STATUS['impedances']['cell1_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell1_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm'] 
								if args.victron:
									dbusservice["/Impedances/Cell1"] = BMS_STATUS['impedances']['cell1_impedance']['text']
									dbusservice["/Raw/Impedances/Cell1"] = BMS_STATUS['impedances']['cell1_impedance']['value']

								BMS_STATUS['impedances']['cell2_impedance']['value'] = get_cell_impedance(ord(packet[9]), ord(packet[10]))
								BMS_STATUS['impedances']['cell2_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell2_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell2"] = BMS_STATUS['impedances']['cell2_impedance']['text']
									dbusservice["/Raw/Impedances/Cell2"] = BMS_STATUS['impedances']['cell2_impedance']['value']

								BMS_STATUS['impedances']['cell3_impedance']['value'] = get_cell_impedance(ord(packet[11]), ord(packet[12]))
								BMS_STATUS['impedances']['cell3_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell3_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell3"] = BMS_STATUS['impedances']['cell3_impedance']['text']
									dbusservice["/Raw/Impedances/Cell3"] = BMS_STATUS['impedances']['cell3_impedance']['value']

								BMS_STATUS['impedances']['cell4_impedance']['value'] = get_cell_impedance(ord(packet[13]), ord(packet[14]))
								BMS_STATUS['impedances']['cell4_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell4_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell4"] = BMS_STATUS['impedances']['cell4_impedance']['text']
									dbusservice["/Raw/Impedances/Cell4"] = BMS_STATUS['impedances']['cell4_impedance']['value']

								BMS_STATUS['impedances']['cell5_impedance']['value'] = get_cell_impedance(ord(packet[15]), ord(packet[16]))
								BMS_STATUS['impedances']['cell5_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell5_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell5"] = BMS_STATUS['impedances']['cell5_impedance']['text']
									dbusservice["/Raw/Impedances/Cell5"] = BMS_STATUS['impedances']['cell5_impedance']['value']

								BMS_STATUS['impedances']['cell6_impedance']['value'] = get_cell_impedance(ord(packet[17]), ord(packet[18]))
								BMS_STATUS['impedances']['cell6_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell6_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell6"] = BMS_STATUS['impedances']['cell6_impedance']['text']
									dbusservice["/Raw/Impedances/Cell6"] = BMS_STATUS['impedances']['cell6_impedance']['value']

								BMS_STATUS['impedances']['cell7_impedance']['value'] = get_cell_impedance(ord(packet[19]), ord(packet[20]))
								BMS_STATUS['impedances']['cell7_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell7_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell7"] = BMS_STATUS['impedances']['cell7_impedance']['text']
									dbusservice["/Raw/Impedances/Cell7"] = BMS_STATUS['impedances']['cell7_impedance']['value']

								BMS_STATUS['impedances']['cell8_impedance']['value'] = get_cell_impedance(ord(packet[21]), ord(packet[22]))
								BMS_STATUS['impedances']['cell8_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell8_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
								if args.victron:
									dbusservice["/Impedances/Cell8"] = BMS_STATUS['impedances']['cell8_impedance']['text']
									dbusservice["/Raw/Impedances/Cell8"] = BMS_STATUS['impedances']['cell8_impedance']['value']


								if (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[1]): # packet from BMS16


									# cell impedances BMS8
									BMS_STATUS['impedances']['cell9_impedance']['value'] = get_cell_impedance(ord(packet[23]), ord(packet[24]))
									BMS_STATUS['impedances']['cell9_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell9_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell9"] = BMS_STATUS['impedances']['cell9_impedance']['text']
										dbusservice["/Raw/Impedances/Cell9"] = BMS_STATUS['impedances']['cell9_impedance']['value']

									BMS_STATUS['impedances']['cell10_impedance']['value'] = get_cell_impedance(ord(packet[25]), ord(packet[26]))
									BMS_STATUS['impedances']['cell10_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell10_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell10"] = BMS_STATUS['impedances']['cell10_impedance']['text']
										dbusservice["/Raw/Impedances/Cell10"] = BMS_STATUS['impedances']['cell10_impedance']['value']

									BMS_STATUS['impedances']['cell11_impedance']['value'] = get_cell_impedance(ord(packet[27]), ord(packet[28]))
									BMS_STATUS['impedances']['cell11_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell11_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell11"] = BMS_STATUS['impedances']['cell11_impedance']['text']
										dbusservice["/Raw/Impedances/Cell11"] = BMS_STATUS['impedances']['cell11_impedance']['value']

									BMS_STATUS['impedances']['cell12_impedance']['value'] = get_cell_impedance(ord(packet[29]), ord(packet[30]))
									BMS_STATUS['impedances']['cell12_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell12_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell12"] = BMS_STATUS['impedances']['cell12_impedance']['text']
										dbusservice["/Raw/Impedances/Cell12"] = BMS_STATUS['impedances']['cell12_impedance']['value']

									BMS_STATUS['impedances']['cell13_impedance']['value'] = get_cell_impedance(ord(packet[31]), ord(packet[32]))
									BMS_STATUS['impedances']['cell13_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell13_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell13"] = BMS_STATUS['impedances']['cell13_impedance']['text']
										dbusservice["/Raw/Impedances/Cell13"] = BMS_STATUS['impedances']['cell13_impedance']['value']

									BMS_STATUS['impedances']['cell14_impedance']['value'] = get_cell_impedance(ord(packet[33]), ord(packet[34]))
									BMS_STATUS['impedances']['cell14_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell14_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell14"] = BMS_STATUS['impedances']['cell14_impedance']['text']
										dbusservice["/Raw/Impedances/Cell14"] = BMS_STATUS['impedances']['cell14_impedance']['value']

									BMS_STATUS['impedances']['cell15_impedance']['value'] = get_cell_impedance(ord(packet[35]), ord(packet[36]))
									BMS_STATUS['impedances']['cell15_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell15_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell15"] = BMS_STATUS['impedances']['cell15_impedance']['text']
										dbusservice["/Raw/Impedances/Cell15"] = BMS_STATUS['impedances']['cell15_impedance']['value']

									BMS_STATUS['impedances']['cell16_impedance']['value'] = get_cell_impedance(ord(packet[37]), ord(packet[38]))
									BMS_STATUS['impedances']['cell16_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell16_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell16"] = BMS_STATUS['impedances']['cell16_impedance']['text']
										dbusservice["/Raw/Impedances/Cell16"] = BMS_STATUS['impedances']['cell16_impedance']['value']


								if (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[2]): # packet from BMS24

									BMS_STATUS['impedances']['cell17_impedance']['value'] = get_cell_impedance(ord(packet[39]), ord(packet[40]))
									BMS_STATUS['impedances']['cell17_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell17_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell17"] = BMS_STATUS['impedances']['cell17_impedance']['text']
										dbusservice["/Raw/Impedances/Cell17"] = BMS_STATUS['impedances']['cell17_impedance']['value']

									BMS_STATUS['impedances']['cell18_impedance']['value'] = get_cell_impedance(ord(packet[41]), ord(packet[42]))
									BMS_STATUS['impedances']['cell18_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell18_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell18"] = BMS_STATUS['impedances']['cell18_impedance']['text']
										dbusservice["/Raw/Impedances/Cell18"] = BMS_STATUS['impedances']['cell18_impedance']['value']

									BMS_STATUS['impedances']['cell19_impedance']['value'] = get_cell_impedance(ord(packet[43]), ord(packet[44]))
									BMS_STATUS['impedances']['cell19_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell19_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell19"] = BMS_STATUS['impedances']['cell19_impedance']['text']
										dbusservice["/Raw/Impedances/Cell19"] = BMS_STATUS['impedances']['cell19_impedance']['value']

									BMS_STATUS['impedances']['cell20_impedance']['value'] = get_cell_impedance(ord(packet[45]), ord(packet[46]))
									BMS_STATUS['impedances']['cell20_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell20_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell20"] = BMS_STATUS['impedances']['cell20_impedance']['text']
										dbusservice["/Raw/Impedances/Cell20"] = BMS_STATUS['impedances']['cell20_impedance']['value']

									BMS_STATUS['impedances']['cell21_impedance']['value'] = get_cell_impedance(ord(packet[47]), ord(packet[48]))
									BMS_STATUS['impedances']['cell21_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell21_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell21"] = BMS_STATUS['impedances']['cell21_impedance']['text']
										dbusservice["/Raw/Impedances/Cell21"] = BMS_STATUS['impedances']['cell21_impedance']['value']

									BMS_STATUS['impedances']['cell22_impedance']['value'] = get_cell_impedance(ord(packet[49]), ord(packet[50]))
									BMS_STATUS['impedances']['cell22_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell22_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell22"] = BMS_STATUS['impedances']['cell22_impedance']['text']
										dbusservice["/Raw/Impedances/Cell22"] = BMS_STATUS['impedances']['cell22_impedance']['value']

									BMS_STATUS['impedances']['cell23_impedance']['value'] = get_cell_impedance(ord(packet[51]), ord(packet[52]))
									BMS_STATUS['impedances']['cell23_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell23_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell23"] = BMS_STATUS['impedances']['cell23_impedance']['text']
										dbusservice["/Raw/Impedances/Cell23"] = BMS_STATUS['impedances']['cell23_impedance']['value']

									BMS_STATUS['impedances']['cell24_impedance']['value'] = get_cell_impedance(ord(packet[53]), ord(packet[54]))
									BMS_STATUS['impedances']['cell24_impedance']['text'] = "{:.1f}".format(BMS_STATUS['impedances']['cell24_impedance']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']
									if args.victron:
										dbusservice["/Impedances/Cell24"] = BMS_STATUS['impedances']['cell24_impedance']['text']
										dbusservice["/Raw/Impedances/Cell24"] = BMS_STATUS['impedances']['cell24_impedance']['value']

								
								# get min/max impedances to calculate the diff
								cell_impedances = []

								if (BMS_STATUS['impedances']['cell1_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell1_impedance']['value'])
								if (BMS_STATUS['impedances']['cell2_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell2_impedance']['value'])
								if (BMS_STATUS['impedances']['cell3_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell3_impedance']['value'])
								if (BMS_STATUS['impedances']['cell4_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell4_impedance']['value'])
								if (BMS_STATUS['impedances']['cell5_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell5_impedance']['value'])
								if (BMS_STATUS['impedances']['cell6_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell6_impedance']['value'])
								if (BMS_STATUS['impedances']['cell7_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell7_impedance']['value'])
								if (BMS_STATUS['impedances']['cell8_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell8_impedance']['value'])
								if (BMS_STATUS['impedances']['cell9_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell9_impedance']['value'])
								if (BMS_STATUS['impedances']['cell10_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell10_impedance']['value'])
								if (BMS_STATUS['impedances']['cell11_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell11_impedance']['value'])
								if (BMS_STATUS['impedances']['cell12_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell12_impedance']['value'])
								if (BMS_STATUS['impedances']['cell13_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell13_impedance']['value'])
								if (BMS_STATUS['impedances']['cell14_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell14_impedance']['value'])
								if (BMS_STATUS['impedances']['cell15_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell15_impedance']['value'])
								if (BMS_STATUS['impedances']['cell16_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell16_impedance']['value'])
								if (BMS_STATUS['impedances']['cell17_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell17_impedance']['value'])
								if (BMS_STATUS['impedances']['cell18_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell18_impedance']['value'])
								if (BMS_STATUS['impedances']['cell19_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell19_impedance']['value'])
								if (BMS_STATUS['impedances']['cell20_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell20_impedance']['value'])
								if (BMS_STATUS['impedances']['cell21_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell21_impedance']['value'])
								if (BMS_STATUS['impedances']['cell22_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell22_impedance']['value'])
								if (BMS_STATUS['impedances']['cell23_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell23_impedance']['value'])
								if (BMS_STATUS['impedances']['cell24_impedance']['value'] >= MIN_CELL_IMPEDANCE):
									cell_impedances.append(BMS_STATUS['impedances']['cell24_impedance']['value'])
									
								BMS_STATUS['impedances']['agg_impedances']['sum']['value']  = sum(cell_impedances)
								BMS_STATUS['impedances']['agg_impedances']['sum']['text']   = "{:.1f}".format(BMS_STATUS['impedances']['agg_impedances']['sum']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm'] 
								BMS_STATUS['impedances']['agg_impedances']['max']['value']  = max(cell_impedances)
								BMS_STATUS['impedances']['agg_impedances']['max']['text']   = "{:.1f}".format(BMS_STATUS['impedances']['agg_impedances']['max']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm'] 
								BMS_STATUS['impedances']['agg_impedances']['min']['value']  = min(cell_impedances)
								BMS_STATUS['impedances']['agg_impedances']['min']['text']   = "{:.1f}".format(BMS_STATUS['impedances']['agg_impedances']['min']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm'] 
								BMS_STATUS['impedances']['agg_impedances']['diff']['value'] = BMS_STATUS['impedances']['agg_impedances']['max']['value'] - BMS_STATUS['impedances']['agg_impedances']['min']['value']
								BMS_STATUS['impedances']['agg_impedances']['diff']['text']  = "{:.1f}".format(BMS_STATUS['impedances']['agg_impedances']['diff']['value']) + "m" + SPECIAL_DISPLAY_SYMBOLS['ohm']

								if args.victron:
									dbusservice["/Impedances/Sum"]      = BMS_STATUS['impedances']['agg_impedances']['sum']['text']
									dbusservice["/Raw/Impedances/Sum"]  = BMS_STATUS['impedances']['agg_impedances']['sum']['value']
									dbusservice["/Impedances/Max"]      = BMS_STATUS['impedances']['agg_impedances']['max']['text']
									dbusservice["/Raw/Impedances/Max"]  = BMS_STATUS['impedances']['agg_impedances']['max']['value']
									dbusservice["/Impedances/Min"]      = BMS_STATUS['impedances']['agg_impedances']['min']['text']
									dbusservice["/Raw/Impedances/Min"]  = BMS_STATUS['impedances']['agg_impedances']['min']['value']
									dbusservice["/Impedances/Diff"]     = BMS_STATUS['impedances']['agg_impedances']['diff']['text']
									dbusservice["/Raw/Impedances/Diff"] = BMS_STATUS['impedances']['agg_impedances']['diff']['value']


								# update timestamp
								current_date = datetime.datetime.now()
								BMS_STATUS['impedances']['timestamp']['value'] = time.time()
								BMS_STATUS['impedances']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
								if args.victron:
									dbusservice["/Impedances/UpdateTimestamp"] = BMS_STATUS['impedances']['timestamp']['text']
									dbusservice["/Raw/Impedances/UpdateTimestamp"] = BMS_STATUS['impedances']['timestamp']['value']
									

								# print (BMS_STATUS)
								if (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[0]): # packet from BMS8
								
									logging.info("BMS8 impedances " +
										"][SUM|" + BMS_STATUS['impedances']['agg_impedances']['sum']['text'] +
										"][#1|"  + BMS_STATUS['impedances']['cell1_impedance']['text'] +
										"][#2|"  + BMS_STATUS['impedances']['cell2_impedance']['text'] + 
										"][#3|"  + BMS_STATUS['impedances']['cell3_impedance']['text'] + 
										"][#4|"  + BMS_STATUS['impedances']['cell4_impedance']['text'] +
										"][#5|"  + BMS_STATUS['impedances']['cell5_impedance']['text'] +
										"][#6|"  + BMS_STATUS['impedances']['cell6_impedance']['text'] +
										"][#7|"  + BMS_STATUS['impedances']['cell7_impedance']['text'] +
										"][#8|"  + BMS_STATUS['impedances']['cell8_impedance']['text'] + "]")

								elif (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[1]): # packet from BMS16

									logging.info("BMS16 impedances " +
										"][SUM|"  + BMS_STATUS['impedances']['agg_impedances']['sum']['text'] +
										"][#1|"   + BMS_STATUS['impedances']['cell1_impedance']['text'] +
										"][#2|"   + BMS_STATUS['impedances']['cell2_impedance']['text'] + 
										"][#3|"   + BMS_STATUS['impedances']['cell3_impedance']['text'] + 
										"][#4|"   + BMS_STATUS['impedances']['cell4_impedance']['text'] +
										"][#5|"   + BMS_STATUS['impedances']['cell5_impedance']['text'] +
										"][#6|"   + BMS_STATUS['impedances']['cell6_impedance']['text'] +
										"][#7|"   + BMS_STATUS['impedances']['cell7_impedance']['text'] +
										"][#8|"   + BMS_STATUS['impedances']['cell8_impedance']['text'] +
										"][#9|"   + BMS_STATUS['impedances']['cell9_impedance']['text'] + 
										"][#10|"  + BMS_STATUS['impedances']['cell10_impedance']['text'] + 
										"][#11|"  + BMS_STATUS['impedances']['cell11_impedance']['text'] +
										"][#12|"  + BMS_STATUS['impedances']['cell12_impedance']['text'] +
										"][#13|"  + BMS_STATUS['impedances']['cell13_impedance']['text'] +
										"][#14|"  + BMS_STATUS['impedances']['cell14_impedance']['text'] +
										"][#15|"  + BMS_STATUS['impedances']['cell15_impedance']['text'] +
										"][#16|"  + BMS_STATUS['impedances']['cell16_impedance']['text'] + "]")
								

								elif (packet_length == PACKET_LENGTH_STATUS_IMPEDANCES[2]): # packet from BMS24

									logging.info("BMS24 impedances " +
										"][SUM|"  + BMS_STATUS['impedances']['agg_impedances']['sum']['text'] +
										"][#1|"   + BMS_STATUS['impedances']['cell1_impedance']['text'] +
										"][#2|"   + BMS_STATUS['impedances']['cell2_impedance']['text'] + 
										"][#3|"   + BMS_STATUS['impedances']['cell3_impedance']['text'] + 
										"][#4|"   + BMS_STATUS['impedances']['cell4_impedance']['text'] +
										"][#5|"   + BMS_STATUS['impedances']['cell5_impedance']['text'] +
										"][#6|"   + BMS_STATUS['impedances']['cell6_impedance']['text'] +
										"][#7|"   + BMS_STATUS['impedances']['cell7_impedance']['text'] +
										"][#8|"   + BMS_STATUS['impedances']['cell8_impedance']['text'] +
										"][#9|"   + BMS_STATUS['impedances']['cell9_impedance']['text'] + 
										"][#10|"  + BMS_STATUS['impedances']['cell10_impedance']['text'] + 
										"][#11|"  + BMS_STATUS['impedances']['cell11_impedance']['text'] +
										"][#12|"  + BMS_STATUS['impedances']['cell12_impedance']['text'] +
										"][#13|"  + BMS_STATUS['impedances']['cell13_impedance']['text'] +
										"][#14|"  + BMS_STATUS['impedances']['cell14_impedance']['text'] +
										"][#15|"  + BMS_STATUS['impedances']['cell15_impedance']['text'] +
										"][#16|"  + BMS_STATUS['impedances']['cell16_impedance']['text'] + 
										"][#17|"  + BMS_STATUS['impedances']['cell17_impedance']['text'] +
										"][#18|"  + BMS_STATUS['impedances']['cell18_impedance']['text'] +
										"][#19|"  + BMS_STATUS['impedances']['cell19_impedance']['text'] +
										"][#20|"  + BMS_STATUS['impedances']['cell20_impedance']['text'] +
										"][#21|"  + BMS_STATUS['impedances']['cell21_impedance']['text'] +
										"][#22|"  + BMS_STATUS['impedances']['cell22_impedance']['text'] +
										"][#23|"  + BMS_STATUS['impedances']['cell23_impedance']['text'] +
										"][#24|"  + BMS_STATUS['impedances']['cell24_impedance']['text'] + "]")

							else:
								logging.debug("Packet Checksum wrong, skip packet")

							# strip packet
							packet = packet[packet_length:]
						
					else:
						# debug_packet(packet)
						logging.debug("Packet Unknown [1]")
						packet = ""
				
				else:
					logging.debug("Packet Unknown [2]")
					packet = ""
			else:
				logging.debug("Packet too short, skip")
				packet = ""



def handle_serial_data(test_packet = ''):
	try:
		
		if (len(test_packet) > 0): # for testing the example packets form the chargery manual
			parse_packet(test_packet)
		else:
			serial_packet = ""
			if (serial_port.in_waiting > 0):
				logging.debug("Data Waiting [" + str(serial_port.in_waiting) + " bytes]")
			if (serial_port.in_waiting >= (PACKET_LENGTH_MINIMUM * 2)):
				data_buffer_array = serial_port.read(serial_port.in_waiting)
				logging.debug("Data Received [" + str(len(data_buffer_array)) + " bytes]")
				for data_buffer in data_buffer_array:
					serial_packet += data_buffer
				
				if (len(serial_packet) > 0):
					parse_packet(serial_packet)			
				
				data_buffer_array = ""
				serial_packet = ""

		if args.victron:	
			# recheck every second
			gobject.timeout_add(1000, handle_serial_data)

	except KeyboardInterrupt:
		if not args.victron:
			raise


if args.test:
	for item in BMS_TEST_PACKETS.items():
		handle_serial_data(str(item[1]));

	# if we registered in testing to dbus, wait until the script is exitted with keyboard interruption
	if args.victron:  
		logging.info("Waiting for keyboard interruption...")
		while True:
			time.sleep(1)
	
	

else:
	if args.victron:
		gobject.timeout_add(1000, handle_serial_data)
		mainloop = gobject.MainLoop()
		mainloop.run()
	else:
		while True:
			handle_serial_data()
			time.sleep(1)

