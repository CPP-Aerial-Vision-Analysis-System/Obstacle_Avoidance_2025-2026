#!/user/bin/env python3
import rclpy
from rclpy.node import Node

# add <depend>std_msgs</depend>
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')

        # Create publisher called on topic chatter with queue of 10
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # create timer
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.count = 0

     # instead of constant checking, ros2 runs this every event cycle
    def timer_callback(self):
        msg = String() # new string message
        msg.data = f'Hello World: {self.count}' # fill message
        self.publisher_.publish(msg) #publish message 
        self.get_logger().info(f'Publisiong: {msg.data}') # consol log what is happening
        self.count +=1

def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown

if __name__ == '__main__':
    main()
