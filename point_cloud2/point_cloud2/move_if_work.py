#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, CommandBool


# === TARGET COORDINATE (in meters, ENU frame) ===
TARGET_X = 5.0    # Forward (+X)
TARGET_Y = 3.0    # Left (+Y)
TARGET_Z = 2.0    # Up (+Z)
# ================================================


class GoToPoint(Node):
    def __init__(self):
        super().__init__('go_to_point')

        # State subscription
        self.state = State()
        self.state_sub = self.create_subscription(State, '/mavros/state', self.state_cb, 10)

        # Publisher for local position setpoints
        self.pose_pub = self.create_publisher(PoseStamped, '/mavros/setpoint_position/local', 10)

        # Services for mode/arming
        self.set_mode_cli = self.create_client(SetMode, '/mavros/set_mode')
        self.arm_cli = self.create_client(CommandBool, '/mavros/cmd/arming')

    def state_cb(self, msg):
        self.state = msg

    def wait_for_connection(self, timeout=20.0):
        self.get_logger().info("Waiting for FCU connection...")
        start = time.time()
        while not self.state.connected and time.time() - start < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
        return self.state.connected

    def set_mode(self, mode="GUIDED"):
        if not self.set_mode_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("set_mode service not available")
            return False
        req = SetMode.Request(custom_mode=mode)
        fut = self.set_mode_cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut, timeout_sec=5.0)
        ok = fut.result() and fut.result().mode_sent
        self.get_logger().info(f"Mode {mode}: {'OK' if ok else 'FAIL'}")
        return ok

    def arm(self, value=True):
        if not self.arm_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("arming service not available")
            return False
        req = CommandBool.Request(value=value)
        fut = self.arm_cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut, timeout_sec=5.0)
        ok = fut.result() and fut.result().success
        self.get_logger().info(f"{'Arm' if value else 'Disarm'}: {'OK' if ok else 'FAIL'}")
        return ok

    def publish_target(self, x, y, z, rate_hz=20.0, duration_s=10.0):
        msg = PoseStamped()
        msg.header.frame_id = "map"
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        dt = 1.0 / rate_hz
        steps = int(duration_s / dt)
        for _ in range(steps):
            if not rclpy.ok():
                break
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pose_pub.publish(msg)
            time.sleep(dt)

    def run(self):
        if not self.wait_for_connection():
            self.get_logger().error("No FCU connection")
            return

        self.get_logger().info("Priming setpoints...")
        self.publish_target(0.0, 0.0, 0.0, duration_s=2.0)

        if self.state.mode != "GUIDED":
            self.set_mode("GUIDED")
        if not self.state.armed:
            self.arm(True)

        self.get_logger().info(f"Flying to: X={TARGET_X}  Y={TARGET_Y}  Z={TARGET_Z}")
        self.publish_target(TARGET_X, TARGET_Y, TARGET_Z, duration_s=15.0)

        self.get_logger().info("Reached target (approx). Holding position...")
        self.publish_target(TARGET_X, TARGET_Y, TARGET_Z, duration_s=5.0)

        # Optional disarm
        self.arm(False)


def main():
    rclpy.init()
    node = GoToPoint()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

