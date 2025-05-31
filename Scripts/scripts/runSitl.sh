#!/bin/bash

gnome-terminal  --title MavProxy --working-directory=$HOME/ardupilot/ArduCopter/ -- bash -c "../Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --console --out=udp:127.0.0.1:14551"

exit 0