#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from scipy.spatial.transform import Rotation as R
from apriltag_msgs.msg import AprilTagDetectionArray
import numpy as np
import math
from std_msgs.msg import Float64

class Orientation(Node):
    def __init__(self):
        super().__init__('imu_angles')

        self.create_subscription(Imu, '/imu', self.print_yaw, 10)
        self.create_subscription(AprilTagDetectionArray, '/detections', self.record_tag_pose, 10)

        self.rotation_error = self.create_publisher(Float64, '/rotation_error', 10)

        self.create_timer(0.25, self.orientation_offset)

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
        deg_angle = math.degrees(euler[2]) # get yaw value
        self.imu_yaw = deg_angle

        self.get_logger().info(f'yaw from IMU: {deg_angle}')
    
    def record_tag_pose(self, msg:AprilTagDetectionArray):
        '''record Apriltag rotation angle'''
        tag_pose = msg.detections[0].pose

        quat = tag_pose.orientation
        quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

        # normalize
        quat_norm = np.linalg.norm(quat_array)
        if quat_norm > 0: 
            quat_normalized = quat_array / quat_norm
        else:
            quat_normalized = quat_array 

        rotation = R.from_quat(quat_normalized)

        euler = rotation.as_euler('xyz') # THIS IS IN RADIANS!
        deg_angle = math.degrees(euler[2]) # get yaw value
        self.apriltag_yaw = deg_angle

        self.get_logger().info(f'Apriltag rotation: {deg_angle}')

    def orientation_offset(self):
        '''calc difference in IMU and tag yaw'''

        error = abs(self.apriltag_yaw - self.imu_yaw)

        self.rotation_error.publish(error)


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