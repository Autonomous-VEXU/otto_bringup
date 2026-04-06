#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from scipy.spatial.transform import Rotation as R
import numpy as np
import math

class Orientation(Node):
    def __init__(self):
        super().__init__('imu_angles')

        self.create_subscription(Imu, '/bno055/imu', self.print_yaw, 10)

    def print_yaw(self, msg:Imu):
        '''record the current pose of the robot'''

        quat = msg.orientation
        quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

        # normalize
        quat_norm = np.linalg.norm(quat_array)
        if quat_norm > 0: 
            quat_normalized = quat_array / quat_norm
        else:
            quat_normalized = quat_array 

        rotation = R.from_quat(quat_normalized)

        euler = rotation.as_euler('xyz') # THIS IS IN RADIANS!
        deg_angle = math.degrees(euler[0])
        self.get_logger().info(f'yaw from IMU: {deg_angle}')

def main(args=None):
    rclpy.init(args=args)
    node = Orientation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()