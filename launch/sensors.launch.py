#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    '''Launching the driver nodes for the non-LiDAR sensors on Otto'''

    this_dir = get_package_share_directory('otto_bringup')
    sensor_config = os.path.join(this_dir, "config", "sensor_config.yaml")

    # launching IMU argument
    launch_imu = LaunchConfiguration('imu')
    launch_imu_cmd = DeclareLaunchArgument(
        'imu',
        default_value='true',
        description='toggle for launching the IMU node',
    )

    # launching color sensor argument
    launch_color_sensor = LaunchConfiguration('color_sensor')
    launch_color_sensor_cmd = DeclareLaunchArgument(
        'color_sensor',
        default_value='false',
        description='toggle for launching the color sensor node',
    )

    # launching fuel gauge argument
    launch_fuel_gauge = LaunchConfiguration('fuel_gauge')
    launch_fuel_gauge_cmd = DeclareLaunchArgument(
        'fuel_gauge',
        default_value='false',
        description='toggle for launching the fuel gauge node',
    )

    # IMU driver (Adafruit BNO055)
    bno055_imu = Node(
        package="bno055",
        executable="bno055",
        parameters=[sensor_config],
        remappings=[
                ('/bno055/imu', '/imu')], # remap in order to keep the 'bno055' namespace on other topics
        condition=IfCondition(launch_imu)
    )

    # color sensor driver
    color_sensor = Node(
        package="ros_colorsens_apds9960",
        executable='apds9960_node',
        parameters=[sensor_config],
        condition=IfCondition(launch_color_sensor)
    )

    return LaunchDescription([
        launch_imu_cmd,
        launch_color_sensor_cmd,
        launch_fuel_gauge_cmd,
        bno055_imu,
        color_sensor,
        # battery_level
    ])