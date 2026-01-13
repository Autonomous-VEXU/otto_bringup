#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CmdVelConverter(Node):
    def __init__(self):
        super().__init__('cmd_vel_converter')

        # subscribe to /joy_cmd_vel
        self.joy_output = self.create_subscription(TwistStamped, '/joy_cmd_vel', self.convert_frame, 10)

        # publish to /cmd_vel
        self.output = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def convert_frame(self, msg:TwistStamped):
        new_vel = TwistStamped()

        # header
        new_vel.header.frame_id = 'base_link'
        new_vel.header.stamp = self.get_clock().now().to_msg()

        # velocities
        new_vel.twist = msg.twist

        self.output.publish(new_vel)
   
def main(args=None):
    rclpy.init(args=args)
    node = CmdVelConverter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()