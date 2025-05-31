from pymavlink import mavutil
import time

import sys
sys.path.append("/usr/local/lib/")

# Set MAVLink protocol to 2.
import os
os.environ["MAVLINK20"] = "1"
os.environ['MAVLINK_DIALECT'] = 'ardupilotmega'

master= mavutil.mavlink_connection('tcp:localhost:5762', dialect='ardupilotmega')

start_time =  int(round(time.time() * 1000))
current_milli_time = lambda: int(round(time.time() * 1000) - start_time)
current_time_ms = current_milli_time()

while True:

    msg=master.recv_match(type='HEARTBEAT', blocking=False)
    if(msg):
        print(f"Heartbeat from CUBE: {msg}")

    print(round(time.time() * 1000) - start_time)
    mav_msg = master.mav.obstacle_distance_3d_send(
            current_time_ms,    # us Timestamp (UNIX time or time since system boot)
            0,                  
            mavutil.mavlink.MAV_FRAME_BODY_FRD,                  
            65535,              
            float(1),	    
            float(0),       
            float(0),	    
            float(.01),       
            float(25)
        )
    
    time.sleep(.1)