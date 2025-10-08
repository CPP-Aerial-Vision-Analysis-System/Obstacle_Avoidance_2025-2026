#!/bin/bash

gnome-terminal  --title MavProxy --working-directory=$HOME/ardupilot/ArduCopter/ -- bash -c "mavproxy.py --master tcp:127.0.0.1:5760"

exit 0