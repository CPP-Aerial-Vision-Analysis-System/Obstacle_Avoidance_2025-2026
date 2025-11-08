#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Define a Node class for the listener
class Listener(Node):
    def __init__(self):
        super().__init__('listener')  # Initialize the node with the name "listener"

        self.subscription = self.create_subscription(String,'chatter',self.listener_callback,10)

    def listener_callback(self, msg):
        # This function is called whenever a new message arrives on "chatter"
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)         # Initialize ROS 2 Python
    node = Listener()             # Create the Listener node
    rclpy.spin(node)              # Keep node alive to receive messages
    node.destroy_node()           # Clean up
    rclpy.shutdown()              # Shut down ROS 2

if __name__ == '__main__':
    main()

#----------------------------------------------------------
#Add to package.xml
"<depend>std_msgs</depend>"

# Add Talker and listener to setup.py
"talker = py_minisystem.talker:main",
"listener = py_minisystem.listener:main"
#----------------------------------------------------------