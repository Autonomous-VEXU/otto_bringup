#!/usr/bin/env python3
import os

from ament_index_python import get_package_share_directory
from launch_ros.actions import SetRemap
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration

# ros2 launch sick_scan_xd sick_tim_7xxS.launch.py hostname:=192.168.0.51 (port is 2112)
   
def generate_launch_description(): 
	sick_scan_pkg = get_package_share_directory('sick_scan_xd')

	set_hostname_right = DeclareLaunchArgument('hostname1', default_value='192.168.0.51')
	set_hostname_left = DeclareLaunchArgument('hostname2', default_value='192.168.0.50')
    
	hostname_right = LaunchConfiguration('hostname1')
	hostname_left = LaunchConfiguration('hostname2')

    # Right lidar
	right_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sick_scan_pkg, 'launch', 'sick_tim_7xxS.launch.py')),
        launch_arguments={
            'hostname': hostname_right,
            'use_binary_protocol': 'true'
        }.items()
    )

	# Left lidar
	left_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sick_scan_pkg, 'launch', 'sick_tim_7xxS.launch.py')),
        launch_arguments={
            'hostname': hostname_left,
            'use_binary_protocol': 'true',
        }.items()
    )

	right_group = GroupAction([
		SetRemap('/scan', '/scan_right'),
		right_lidar,
	])

	left_group = GroupAction([
		SetRemap('/scan', '/scan_left'),
		left_lidar,
	])


	return LaunchDescription([
		set_hostname_right,
		set_hostname_left,
		right_group,
		left_group
		])



'''
pre launch setup:
---

sudo ip addr flush dev enx00e04c68003f
sudo ip addr add 192.168.0.100/24 dev enx00e04c68003f
sudo ip link set enx00e04c68003f up
'''