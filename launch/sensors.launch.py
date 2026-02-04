#!/usr/bin/env python3

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    '''Various sensors on Otto'''

    # sensor configuration file...

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
        default_value='true',
        description='toggle for launching the color sensor node',
    )

    # launching fuel gauge argument
    launch_fuel_gauge = LaunchConfiguration('fuel_gauge')
    launch_fuel_gauge_cmd = DeclareLaunchArgument(
        'fuel_gauge',
        default_value='true',
        description='toggle for launching the fuel gauge node',
    )

    
    
    # IMU driver
    imu = Node(
        package="ros_imu_lsm6dsv16x",
        executable="lsm6dsv16x",
        screen="on",
        condition=IfCondition(launch_imu)
    )

    # color sensor driver
    color_sensor = Node(
        package="ros_colorsens_9960",
        executable='apds9960',
        screen='on',
        condition=IfCondition(launch_color_sensor)
    )

    # fuel gauge driver
    battery_level = Node(
        package="ros_fuelgauge_max17263",
        executable="max17263_node",
        screen="on",
        condition=IfCondition(launch_fuel_gauge)
    )

    return LaunchDescription([
        launch_imu_cmd,
        launch_color_sensor_cmd,
        launch_fuel_gauge_cmd,
        imu,
        color_sensor,
        battery_level
    ])