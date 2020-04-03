#!/usr/bin/env python

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


# Victron packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/velib_python'))
from vedbus import VeDbusService

# setup timezone
os.environ['TZ'] = 'Europe/Berlin'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
serial_port.flushInput()
logging.info(serial_port.name)  


# connect and register to dbus

driver = {
	'name'        : "Chargery BMS",
	'servicename' : "chargerybms",
	'instance'    : 1,
	'id'          : 0x01,
	'version'     : 1.1,
	'serial'      : "CHGBMS04032020A1",
	'connection'  : "com.victronenergy.battery.ttyUSB0"
}

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

# Create the chargery bms path
dbusservice.add_path('/Info/Soc',                 -1)
dbusservice.add_path('/Info/CurrentMode',         -1)
dbusservice.add_path('/Info/Current',             -1)
dbusservice.add_path('/Info/Temp/Sensor1',        -1)
dbusservice.add_path('/Info/Temp/Sensor2',        -1)
dbusservice.add_path('/Info/Capacity',            -1)
dbusservice.add_path('/Info/ChargeEndVoltage',    -1)
dbusservice.add_path('/Info/UpdateTimestamp',     -1)
dbusservice.add_path('/Voltages/Cell1',           -1)
dbusservice.add_path('/Voltages/Cell2',           -1)
dbusservice.add_path('/Voltages/Cell3',           -1)
dbusservice.add_path('/Voltages/Cell4',           -1)
dbusservice.add_path('/Voltages/Cell5',           -1)
dbusservice.add_path('/Voltages/Cell6',           -1)
dbusservice.add_path('/Voltages/Cell7',           -1)
dbusservice.add_path('/Voltages/Cell8',           -1)
dbusservice.add_path('/Voltages/Cell9',           -1)
dbusservice.add_path('/Voltages/Cell10',          -1)
dbusservice.add_path('/Voltages/Cell11',          -1)
dbusservice.add_path('/Voltages/Cell12',          -1)
dbusservice.add_path('/Voltages/Cell13',          -1)
dbusservice.add_path('/Voltages/Cell14',          -1)
dbusservice.add_path('/Voltages/Cell15',          -1)
dbusservice.add_path('/Voltages/Cell16',          -1)
dbusservice.add_path('/Voltages/Sum',             -1)
dbusservice.add_path('/Voltages/Diff',            -1)
dbusservice.add_path('/Voltages/Max',             -1)
dbusservice.add_path('/Voltages/Min',             -1)
dbusservice.add_path('/Voltages/UpdateTimestamp', -1)


# Create the real values paths
dbusservice.add_path('/Raw/Info/Soc',                 -1)
dbusservice.add_path('/Raw/Info/CurrentMode',         -1)
dbusservice.add_path('/Raw/Info/Current',             -1)
dbusservice.add_path('/Raw/Info/Temp/Sensor1',        -1)
dbusservice.add_path('/Raw/Info/Temp/Sensor2',        -1)
dbusservice.add_path('/Raw/Info/Capacity',            -1)
dbusservice.add_path('/Raw/Info/ChargeEndVoltage',    -1)
dbusservice.add_path('/Raw/Info/UpdateTimestamp',     -1)
dbusservice.add_path('/Raw/Voltages/Cell1',           -1)
dbusservice.add_path('/Raw/Voltages/Cell2',           -1)
dbusservice.add_path('/Raw/Voltages/Cell3',           -1)
dbusservice.add_path('/Raw/Voltages/Cell4',           -1)
dbusservice.add_path('/Raw/Voltages/Cell5',           -1)
dbusservice.add_path('/Raw/Voltages/Cell6',           -1)
dbusservice.add_path('/Raw/Voltages/Cell7',           -1)
dbusservice.add_path('/Raw/Voltages/Cell8',           -1)
dbusservice.add_path('/Raw/Voltages/Cell9',           -1)
dbusservice.add_path('/Raw/Voltages/Cell10',          -1)
dbusservice.add_path('/Raw/Voltages/Cell11',          -1)
dbusservice.add_path('/Raw/Voltages/Cell12',          -1)
dbusservice.add_path('/Raw/Voltages/Cell13',          -1)
dbusservice.add_path('/Raw/Voltages/Cell14',          -1)
dbusservice.add_path('/Raw/Voltages/Cell15',          -1)
dbusservice.add_path('/Raw/Voltages/Cell16',          -1)
dbusservice.add_path('/Raw/Voltages/Sum',             -1)
dbusservice.add_path('/Raw/Voltages/Diff',            -1)
dbusservice.add_path('/Raw/Voltages/Max',             -1)
dbusservice.add_path('/Raw/Voltages/Min',             -1)
dbusservice.add_path('/Raw/Voltages/UpdateTimestamp', -1)



PACKET_HEADER       = 0x24
PACKET_STATUS_CELLS = 0x56
PACKET_STATUS_BMS   = 0x57

PACKET_LENGTH_MINIMUM      = 15
PACKET_LENGTH_STATUS_CELLS = 38
PACKET_LENGTH_STATUS_BMS   = 15

MIN_CELL_VOLTAGE = 1.0

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
	'cells' : {
		'capacity' : {
			'value' : -1,
			'text'  : ""
		},
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
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		}
	}
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


def get_temperature_value(byte1, byte2):
	return float((float(byte1 * 256) + float(byte2)) / 10)



def parse_packet(packet):
	logging.debug("Parse Packet")

	while (len(packet) > PACKET_LENGTH_MINIMUM): 
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
					
						if (len(packet) < PACKET_LENGTH_STATUS_BMS):
							logging.debug("Packet Status BMS too short, skip")
							packet = ""
						else:
							logging.debug("Packet Status BMS")

							# checksum value
							checksum = ord(packet[14])

							# calculate checksum
							checksum_check = (ord(packet[0])
								+ ord(packet[1])
								+ ord(packet[2])
								+ ord(packet[3])
								+ ord(packet[4])
								+ ord(packet[5])
								+ ord(packet[6])
								+ ord(packet[7])
								+ ord(packet[8])
								+ ord(packet[9])
								+ ord(packet[10])
								+ ord(packet[11])
								+ ord(packet[12])
								+ ord(packet[13])) % 256
							logging.debug("Packet Checksum : " + str(checksum) + "|" + str(checksum_check))
							
							# data integrity does match
							if (checksum == checksum_check):

								# charge end voltage
								BMS_STATUS['bms']['charged_end_voltage']['value'] = get_voltage_value(ord(packet[4]), ord(packet[5]))
								BMS_STATUS['bms']['charged_end_voltage']['text'] = "{:.2f}".format(BMS_STATUS['bms']['charged_end_voltage']['value']) + "V"
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
									BMS_STATUS['bms']['current']['text'] = "+" + str(BMS_STATUS['bms']['current']['value']) + "A"
								elif (bms_charge_mode == 0x02):
									BMS_STATUS['bms']['current_mode']['value'] = 1
									BMS_STATUS['bms']['current_mode']['text']  = "Storage"
									BMS_STATUS['bms']['current']['text'] = str(BMS_STATUS['bms']['current']['value']) + "A"
								else:
									BMS_STATUS['bms']['current_mode']['value'] = -1
									BMS_STATUS['bms']['current_mode']['text']  = ""
									BMS_STATUS['bms']['current']['text'] = ""

								dbusservice["/Info/CurrentMode"] = BMS_STATUS['bms']['current_mode']['text']
								dbusservice["/Info/Current"] = BMS_STATUS['bms']['current']['text']

								dbusservice["/Raw/Info/CurrentMode"] = BMS_STATUS['bms']['current_mode']['value']
								dbusservice["/Raw/Info/Current"] = BMS_STATUS['bms']['current']['value']

								# current temperatures
								BMS_STATUS['bms']['temperature']['sensor_t1']['value'] = get_temperature_value(ord(packet[9]), ord(packet[10]))
								BMS_STATUS['bms']['temperature']['sensor_t1']['text'] = str(BMS_STATUS['bms']['temperature']['sensor_t1']['value']) + "C"
								BMS_STATUS['bms']['temperature']['sensor_t2']['value'] = get_temperature_value(ord(packet[11]), ord(packet[12]))
								BMS_STATUS['bms']['temperature']['sensor_t2']['text'] = str(BMS_STATUS['bms']['temperature']['sensor_t2']['value']) + "C"

								dbusservice["/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['text']
								dbusservice["/Info/Temp/Sensor2"] = BMS_STATUS['bms']['temperature']['sensor_t2']['text']
								dbusservice["/Raw/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['value']
								dbusservice["/Raw/Info/Temp/Sensor2"] = BMS_STATUS['bms']['temperature']['sensor_t2']['value']

								# soc value
								BMS_STATUS['bms']['soc']['value'] = ord(packet[13])
								BMS_STATUS['bms']['soc']['text'] = str(ord(packet[13])) + "%"
								dbusservice["/Info/Soc"] = BMS_STATUS['bms']['soc']['text']
								dbusservice["/Raw/Info/Soc"] = BMS_STATUS['bms']['soc']['value']
								
								# update timestamp
								current_date = datetime.datetime.now()
								BMS_STATUS['bms']['timestamp']['value'] = time.time()
								BMS_STATUS['bms']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
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

						if (len(packet) < PACKET_LENGTH_STATUS_CELLS):
							logging.debug("Packet Status Cells too short, skip")
							packet = ""
						else:
							logging.debug("Packet Status Cells")

							# checksum value
							checksum = ord(packet[37])

							# calculate checksum
							checksum_check = (ord(packet[0])
								+ ord(packet[1])
								+ ord(packet[2])
								+ ord(packet[3])
								+ ord(packet[4])
								+ ord(packet[5])
								+ ord(packet[6])
								+ ord(packet[7])
								+ ord(packet[8])
								+ ord(packet[9])
								+ ord(packet[10])
								+ ord(packet[11])
								+ ord(packet[12])
								+ ord(packet[13])
								+ ord(packet[14])
								+ ord(packet[15])
								+ ord(packet[16])
								+ ord(packet[17])
								+ ord(packet[18])
								+ ord(packet[19])
								+ ord(packet[20])
								+ ord(packet[21])
								+ ord(packet[22])
								+ ord(packet[23])
								+ ord(packet[24])
								+ ord(packet[25])
								+ ord(packet[26])
								+ ord(packet[27])
								+ ord(packet[28])
								+ ord(packet[29])
								+ ord(packet[30])
								+ ord(packet[31])
								+ ord(packet[32])
								+ ord(packet[33])
								+ ord(packet[34])
								+ ord(packet[35])
								+ ord(packet[36])) % 256
							logging.debug("Packet Checksum : " + str(checksum) + "|" + str(checksum_check))
							
							# data integrity does match
							if (checksum == checksum_check):


								# cell voltages
								BMS_STATUS['cells']['cell1_voltage']['value'] = get_voltage_value(ord(packet[4]), ord(packet[5]))
								BMS_STATUS['cells']['cell1_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell1_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell1"] = BMS_STATUS['cells']['cell1_voltage']['text']
								dbusservice["/Raw/Voltages/Cell1"] = BMS_STATUS['cells']['cell1_voltage']['value']

								BMS_STATUS['cells']['cell2_voltage']['value'] = get_voltage_value(ord(packet[6]), ord(packet[7]))
								BMS_STATUS['cells']['cell2_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell2_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell2"] = BMS_STATUS['cells']['cell2_voltage']['text']
								dbusservice["/Raw/Voltages/Cell2"] = BMS_STATUS['cells']['cell2_voltage']['value']

								BMS_STATUS['cells']['cell3_voltage']['value'] = get_voltage_value(ord(packet[8]), ord(packet[9]))
								BMS_STATUS['cells']['cell3_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell3_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell3"] = BMS_STATUS['cells']['cell3_voltage']['text']
								dbusservice["/Raw/Voltages/Cell3"] = BMS_STATUS['cells']['cell3_voltage']['value']

								BMS_STATUS['cells']['cell4_voltage']['value'] = get_voltage_value(ord(packet[10]), ord(packet[11]))
								BMS_STATUS['cells']['cell4_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell4_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell4"] = BMS_STATUS['cells']['cell4_voltage']['text']
								dbusservice["/Raw/Voltages/Cell4"] = BMS_STATUS['cells']['cell4_voltage']['value']

								BMS_STATUS['cells']['cell5_voltage']['value'] = get_voltage_value(ord(packet[12]), ord(packet[13]))
								BMS_STATUS['cells']['cell5_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell5_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell5"] = BMS_STATUS['cells']['cell5_voltage']['text']
								dbusservice["/Raw/Voltages/Cell5"] = BMS_STATUS['cells']['cell5_voltage']['value']

								BMS_STATUS['cells']['cell6_voltage']['value'] = get_voltage_value(ord(packet[14]), ord(packet[15]))
								BMS_STATUS['cells']['cell6_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell6_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell6"] = BMS_STATUS['cells']['cell6_voltage']['text']
								dbusservice["/Raw/Voltages/Cell6"] = BMS_STATUS['cells']['cell6_voltage']['value']

								BMS_STATUS['cells']['cell7_voltage']['value'] = get_voltage_value(ord(packet[16]), ord(packet[17]))
								BMS_STATUS['cells']['cell7_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell7_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell7"] = BMS_STATUS['cells']['cell7_voltage']['text']
								dbusservice["/Raw/Voltages/Cell7"] = BMS_STATUS['cells']['cell7_voltage']['value']

								BMS_STATUS['cells']['cell8_voltage']['value'] = get_voltage_value(ord(packet[18]), ord(packet[19]))
								BMS_STATUS['cells']['cell8_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell8_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell8"] = BMS_STATUS['cells']['cell8_voltage']['text']
								dbusservice["/Raw/Voltages/Cell8"] = BMS_STATUS['cells']['cell8_voltage']['value']

								BMS_STATUS['cells']['cell9_voltage']['value'] = get_voltage_value(ord(packet[20]), ord(packet[21]))
								BMS_STATUS['cells']['cell9_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell9_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell9"] = BMS_STATUS['cells']['cell9_voltage']['text']
								dbusservice["/Raw/Voltages/Cell9"] = BMS_STATUS['cells']['cell9_voltage']['value']

								BMS_STATUS['cells']['cell10_voltage']['value'] = get_voltage_value(ord(packet[22]), ord(packet[23]))
								BMS_STATUS['cells']['cell10_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell10_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell10"] = BMS_STATUS['cells']['cell10_voltage']['text']
								dbusservice["/Raw/Voltages/Cell10"] = BMS_STATUS['cells']['cell10_voltage']['value']

								BMS_STATUS['cells']['cell11_voltage']['value'] = get_voltage_value(ord(packet[24]), ord(packet[25]))
								BMS_STATUS['cells']['cell11_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell11_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell11"] = BMS_STATUS['cells']['cell11_voltage']['text']
								dbusservice["/Raw/Voltages/Cell11"] = BMS_STATUS['cells']['cell11_voltage']['value']

								BMS_STATUS['cells']['cell12_voltage']['value'] = get_voltage_value(ord(packet[26]), ord(packet[27]))
								BMS_STATUS['cells']['cell12_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell12_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell12"] = BMS_STATUS['cells']['cell12_voltage']['text']
								dbusservice["/Raw/Voltages/Cell12"] = BMS_STATUS['cells']['cell12_voltage']['value']

								BMS_STATUS['cells']['cell13_voltage']['value'] = get_voltage_value(ord(packet[28]), ord(packet[29]))
								BMS_STATUS['cells']['cell13_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell13_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell13"] = BMS_STATUS['cells']['cell13_voltage']['text']
								dbusservice["/Raw/Voltages/Cell13"] = BMS_STATUS['cells']['cell13_voltage']['value']

								BMS_STATUS['cells']['cell14_voltage']['value'] = get_voltage_value(ord(packet[30]), ord(packet[31]))
								BMS_STATUS['cells']['cell14_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell14_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell14"] = BMS_STATUS['cells']['cell14_voltage']['text']
								dbusservice["/Raw/Voltages/Cell14"] = BMS_STATUS['cells']['cell14_voltage']['value']

								BMS_STATUS['cells']['cell15_voltage']['value'] = get_voltage_value(ord(packet[32]), ord(packet[33]))
								BMS_STATUS['cells']['cell15_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell15_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell15"] = BMS_STATUS['cells']['cell15_voltage']['text']
								dbusservice["/Raw/Voltages/Cell15"] = BMS_STATUS['cells']['cell15_voltage']['value']

								BMS_STATUS['cells']['cell16_voltage']['value'] = get_voltage_value(ord(packet[34]), ord(packet[35]))
								BMS_STATUS['cells']['cell16_voltage']['text'] = "{:.3f}".format(BMS_STATUS['cells']['cell16_voltage']['value']) + "V"
								dbusservice["/Voltages/Cell16"] = BMS_STATUS['cells']['cell16_voltage']['text']
								dbusservice["/Raw/Voltages/Cell16"] = BMS_STATUS['cells']['cell16_voltage']['value']

								# capacity value
								BMS_STATUS['cells']['capacity']['value'] = ord(packet[36])
								BMS_STATUS['cells']['capacity']['text'] = str(ord(packet[36])) + "Ah"
								dbusservice["/Info/Capacity"] = BMS_STATUS['cells']['capacity']['text']
								dbusservice["/Raw/Info/Capacity"] = BMS_STATUS['cells']['capacity']['value']

								# get min/max voltages to calculate the diff
								cell_voltages = []

								if (BMS_STATUS['cells']['cell1_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell1_voltage']['value'])
								if (BMS_STATUS['cells']['cell2_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell2_voltage']['value'])
								if (BMS_STATUS['cells']['cell3_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell3_voltage']['value'])
								if (BMS_STATUS['cells']['cell4_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell4_voltage']['value'])
								if (BMS_STATUS['cells']['cell5_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell5_voltage']['value'])
								if (BMS_STATUS['cells']['cell6_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell6_voltage']['value'])
								if (BMS_STATUS['cells']['cell7_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell7_voltage']['value'])
								if (BMS_STATUS['cells']['cell8_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell8_voltage']['value'])
								if (BMS_STATUS['cells']['cell9_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell9_voltage']['value'])
								if (BMS_STATUS['cells']['cell10_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell10_voltage']['value'])
								if (BMS_STATUS['cells']['cell11_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell11_voltage']['value'])
								if (BMS_STATUS['cells']['cell12_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell12_voltage']['value'])
								if (BMS_STATUS['cells']['cell13_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell13_voltage']['value'])
								if (BMS_STATUS['cells']['cell14_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell14_voltage']['value'])
								if (BMS_STATUS['cells']['cell15_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell15_voltage']['value'])
								if (BMS_STATUS['cells']['cell16_voltage']['value'] > MIN_CELL_VOLTAGE):
									cell_voltages.append(BMS_STATUS['cells']['cell16_voltage']['value'])
									
								BMS_STATUS['cells']['agg_voltages']['sum']['value']  = sum(cell_voltages)
								BMS_STATUS['cells']['agg_voltages']['sum']['text']   = "{:.2f}".format(BMS_STATUS['cells']['agg_voltages']['sum']['value']) + "V" 
								BMS_STATUS['cells']['agg_voltages']['max']['value']  = max(cell_voltages)
								BMS_STATUS['cells']['agg_voltages']['max']['text']   = "{:.3f}".format(BMS_STATUS['cells']['agg_voltages']['max']['value']) + "V" 
								BMS_STATUS['cells']['agg_voltages']['min']['value']  = min(cell_voltages)
								BMS_STATUS['cells']['agg_voltages']['min']['text']   = "{:.3f}".format(BMS_STATUS['cells']['agg_voltages']['min']['value']) + "V" 
								BMS_STATUS['cells']['agg_voltages']['diff']['value'] = BMS_STATUS['cells']['agg_voltages']['max']['value'] - BMS_STATUS['cells']['agg_voltages']['min']['value']
								BMS_STATUS['cells']['agg_voltages']['diff']['text']  = "{:.0f}".format(BMS_STATUS['cells']['agg_voltages']['diff']['value'] * 1000) + "mV"

								dbusservice["/Voltages/Sum"]      = BMS_STATUS['cells']['agg_voltages']['sum']['text']
								dbusservice["/Raw/Voltages/Sum"]  = BMS_STATUS['cells']['agg_voltages']['sum']['value']
								dbusservice["/Voltages/Max"]      = BMS_STATUS['cells']['agg_voltages']['max']['text']
								dbusservice["/Raw/Voltages/Max"]  = BMS_STATUS['cells']['agg_voltages']['max']['value']
								dbusservice["/Voltages/Min"]      = BMS_STATUS['cells']['agg_voltages']['min']['text']
								dbusservice["/Raw/Voltages/Min"]  = BMS_STATUS['cells']['agg_voltages']['min']['value']
								dbusservice["/Voltages/Diff"]     = BMS_STATUS['cells']['agg_voltages']['diff']['text']
								dbusservice["/Raw/Voltages/Diff"] = BMS_STATUS['cells']['agg_voltages']['diff']['value']

								
								# update timestamp
								current_date = datetime.datetime.now()
								BMS_STATUS['cells']['timestamp']['value'] = time.time()
								BMS_STATUS['cells']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
								dbusservice["/Voltages/UpdateTimestamp"] = BMS_STATUS['cells']['timestamp']['text']
								dbusservice["/Raw/Voltages/UpdateTimestamp"] = BMS_STATUS['cells']['timestamp']['value']
									

								# print (BMS_STATUS)
								logging.info("BMS cells [DIFF|" + BMS_STATUS['cells']['agg_voltages']['diff']['text'] +
									"][SUM|" + BMS_STATUS['cells']['agg_voltages']['sum']['text'] +
									"][#1|"  + BMS_STATUS['cells']['cell1_voltage']['text'] +
									"][#2|"  + BMS_STATUS['cells']['cell2_voltage']['text'] + 
									"][#3|"  + BMS_STATUS['cells']['cell3_voltage']['text'] + 
									"][#4|"  + BMS_STATUS['cells']['cell4_voltage']['text'] +
									"][#5|"  + BMS_STATUS['cells']['cell5_voltage']['text'] +
									"][#6|"  + BMS_STATUS['cells']['cell6_voltage']['text'] + "]")

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
				logging.debug("Packet to short")
				packet = ""


def handle_serial_data():
	#try:
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
	#except KeyboardInterrupt:
	#	raise
	#except:
	#	logging.debug("Exception")
	
		# recheck every second
		gobject.timeout_add(1000, handle_serial_data)

		
gobject.timeout_add(1000, handle_serial_data)
mainloop = gobject.MainLoop()
mainloop.run()
