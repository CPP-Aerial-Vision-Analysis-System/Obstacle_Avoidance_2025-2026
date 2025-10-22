#! /usr/bin/env python

import rclpy                                     #ROS 2 Python client library
from mavros_msgs.msg import Mavlink              #MAVLink Ros 2 message type
from mavros import mavlink as mavlink_ros        #Conversion helper
from pymavlink.dialects.v20 import ardupilotmega as mavlink2
import time

#create mavlink instance for message packing
mavlink_instance = mavlink2.MAVLink(None)

# millisecond timer starter
start_time =  int(round(time.time() * 1000))
current_milli_time = lambda: int(round(time.time() * 1000) - start_time)
current_time_ms = current_milli_time()

def main(args = None):
    rclpy.init(args=args)   #init ros2 communication protocol
    obstacleTestNode = rclpy.create_node('send_obstacle_3D_test')
    rate = obstacleTestNode.create_rate(10) #loop at 10 Hz
    pub = obstacleTestNode.create_publisher(Mavlink,"/mavlink/to",20)
 
    while rclpy.ok():
        # create the OBSTACLE_DISTANCE_3D data structure
        obstacle_msg = mavlink2.MAVLink_obstacle_distance_3d_message(
            time_boot_ms = round(time.time() * 1000) - start_time,
            sensor_type= 0,
            frame = mavlink2.MAV_FRAME_BODY_FRD,
            obstacle_id = 65535, # max uint16_t
            x = 1,
            y = 0,
            z = 0,
            min_distance = .2,
            max_distance = 25
            
        )
        # populate internal headers
        obstacle_msg.pack(mavlink_instance)
        # convert to ROS message
        rosmsg = mavlink_ros.convert_to_rosmsg(obstacle_msg)

        # manually update mavlink version
        rosmsg.magic = mavlink2.PROTOCOL_MARKER_V2

        pub.publish(rosmsg) #send message

        #rate.sleep()        #maintain loop rate

    rclpy.spin(obstacleTestNode)
    #obstacleTestNode.destroy_node()
    #rclpy.shutdown()

if __name__ == '__main__':
     main()