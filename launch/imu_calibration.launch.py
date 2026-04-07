#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # packages and files

    this_dir = get_package_share_directory('otto_bringup')
    sensor_config = os.path.join(this_dir, "config", "imu_calibration.yaml")
    camera_config = os.path.join(this_dir, 'config', 'camera.yaml')

    camera_node =  Node( # launches
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='field_cam',
        parameters=[camera_config]
    )       

    rectify_image = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node',
        remappings=[
            ('image', '/image_raw')
        ],
        parameters=[{'image_transport': 'raw'}]
    )

    apriltag = Node(
        package='apriltag_ros',
        executable='apriltag_node',
        name='apriltag',
        remappings=[
            ('image_rect', '/image_rect')
        ],
       parameters=[sensor_config]
    )

    # IMU driver (Adafruit BNO055)
    bno055_imu = Node(
        package="bno055",
        executable="bno055",
        parameters=[sensor_config],
        remappings=[
            ('/bno055/imu', '/imu')] # remap in order to keep the 'bno055' namespace on other topics
    )

    error_calc = Node(
        package='otto_bringup',
        executable='imu_orientation.py',
        name='imu_error_node',
        output='screen'
    )

    return LaunchDescription([
        camera_node,
        rectify_image,
        apriltag,
        bno055_imu,
        error_calc
    ])