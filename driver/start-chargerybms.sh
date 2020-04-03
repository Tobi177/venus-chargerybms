#!/bin/bash
#
# Start script for BMV vedirect
#	First parameter: tty device to use
#
# Keep this script running with daemon tools. If it exits because the
# connection crashes, or whatever, daemon tools will start a new one.
#

. /opt/victronenergy/serial-starter/run-service.sh

app="/usr/bin/python /opt/victronenergy/chargerybms/readbms.py"
verbose="-v --log-before 25 --log-after 25"
timeout=3

start $verbose -t $timeout --banner -s /dev/$tty
