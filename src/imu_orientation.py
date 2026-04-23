#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from scipy.spatial.transform import Rotation as R
from apriltag_msgs.msg import AprilTagDetectionArray
import numpy as np
import math
from std_msgs.msg import Float64
import tf2_ros
from geometry_msgs.msg import TransformStamped

class Orientation(Node):
    def __init__(self):
        super().__init__('imu_pose_error')

        self.create_subscription(Imu, '/bno055/imu', self.print_yaw, 10)
        # self.create_subscription(AprilTagDetectionArray, '/detections', self.record_tag_pose, 10)

        self.rotation_error = self.create_publisher(Float64, '/rotation_error', 10)
        self.imu_angle = self.create_publisher(Float64, '/imu_angle', 10)
        self.tag_angle = self.create_publisher(Float64, '/tag_angle', 10)

        self.create_timer(0.25, self.orientation_offset)

        self.apriltag_yaw = None
        self.imu_yaw = None

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

    def print_yaw(self, msg: Imu):
        '''Extract yaw from IMU quaternion (no flips, clean conversion)'''
        quat = msg.orientation
        quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

        # Normalize quaternion
        quat_norm = np.linalg.norm(quat_array)
        quat_normalized = quat_array / quat_norm if quat_norm > 0 else quat_array

        # Convert to Euler angles (roll, pitch, yaw)
        rotation = R.from_quat(quat_normalized)
        euler = rotation.as_euler('xyz')  # ROS IMU default is usually 'xyz'

        # Yaw in degrees, wrapped to [0, 360)
        yaw_deg = math.degrees(euler[2]) % 360

        self.imu_yaw = yaw_deg
        self.imu_angle.publish(Float64(data=yaw_deg))

    # def record_tag_pose(self, msg:AprilTagDetectionArray):
    #     '''record Apriltag rotation angle'''
    #     if msg.detections:
    #         tag_pose_stamped = msg.detections[0].pose  # likely PoseStamped
        
    #         tag_pose = tag_pose_stamped.pose if hasattr(tag_pose_stamped, 'pose') else tag_pose_stamped
    #         position = tag_pose.position
    #         orientation = tag_pose.orientation
    #         self.get_logger().info(f"AprilTag position: x={position.x}, y={position.y}, z={position.z}")
            
    #         quat = orientation
    #         quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

    #         # normalize
    #         quat_norm = np.linalg.norm(quat_array)
    #         if quat_norm > 0: 
    #             quat_normalized = quat_array / quat_norm
    #         else:
    #             quat_normalized = quat_array 

    #         rotation = R.from_quat(quat_normalized)

    #         euler = rotation.as_euler('xyz') # THIS IS IN RADIANS!
    #         deg_angle = math.degrees(euler[2]) # get yaw value
    #         self.apriltag_yaw = deg_angle
        
    #     else:
    #         self.get_logger().info("No AprilTags detected.")

        #self.get_logger().info(f'Apriltag rotation: {deg_angle}')
    

    def orientation_offset(self):
        '''calc difference in IMU and tag yaw'''
        try:
            trans: TransformStamped = self.tf_buffer.lookup_transform(
                'field_cam',  # or your reference frame
                'ground_truth_rotation',      # the tag frame you want
                rclpy.time.Time())
            # Access rotation quaternion
            rot = trans.transform.rotation
            quat_array = np.array([rot.x, rot.y, rot.z, rot.w])

            # Normalize quaternion
            quat_norm = np.linalg.norm(quat_array)
            quat_normalized = quat_array / quat_norm if quat_norm > 0 else quat_array

            # Convert to Euler angles (roll, pitch, yaw)
            rotation = R.from_quat(quat_normalized)
            euler = rotation.as_euler('xyz')

            # Yaw in degrees, wrapped to [0, 360)
            tag_yaw_deg = math.degrees(euler[2]) % 360

            self.apriltag_yaw = tag_yaw_deg
            self.tag_angle.publish(Float64(data=tag_yaw_deg))

        except Exception as e:
            self.get_logger().info(f"Transform not available: {e}")

        if self.apriltag_yaw is None or self.imu_yaw is None:
            error = 0.0
        else:
            def angle_diff_deg(a, b):
                """Compute minimal difference between two angles in degrees."""
                diff = (a - b + 180) % 360 - 180
                return abs(diff)
            error = angle_diff_deg(self.apriltag_yaw, self.imu_yaw)
        self.rotation_error.publish(Float64(data=error))


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