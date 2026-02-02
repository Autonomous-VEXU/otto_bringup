from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    '''Various sensors on Otto'''
    
    # IMU driver
    imu = Node(
        package="ros_imu_lsm6dsv16x",
        executable="lsm6dsv16x",
        screen="on"
    )

    # color sensor driver
    color_sensor = Node(
        package="ros_colorsens_9960",
        executable='apds9960',
        screen='on'
    )

    # fuel gauge driver
    battery_level = Node(
        package="ros_fuelgauge_max17263",
        executable="max17263_node",
        screen="on"
    )

    return LaunchDescription([
        imu,
        color_sensor,
        battery_level
    ])