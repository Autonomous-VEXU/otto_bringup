#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random

class TestPublisher(Node):
    '''test node to see if I set up Docker + CycloneDDS correctly'''
    def __init__(self):
        super().__init__('test_publisher')
        self.publisher_ = self.create_publisher(Int32, '/jetson_test', 10)
        self.timer = self.create_timer(3.0, self.timer_callback)
        self.get_logger().info('jetson test publisher node started')

    def timer_callback(self):
        msg = Int32()
        msg.data = random.randint(0, 100)
        self.publisher_.publish(msg)
        self.get_logger().info(f'publishing: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = TestPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
            node.destroy_node()
            rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()