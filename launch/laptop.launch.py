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

    pkg_dir = get_package_share_directory('otto_bringup')
    scan_merger_pkg = get_package_share_directory('laser_scan_merger')

    shadow_config = os.path.join(pkg_dir, "config", "shadow_filter.yaml")
  
    # laser_scan_merger launch file
    scan_merger = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(scan_merger_pkg, 'launch', 'start.launch.py')
        ),
        launch_arguments={'robotname':'otto'}.items()
    )

    # shadow filter for lidar
    shadow_filter = Node(
        package="laser_filters",
        executable="scan_to_scan_filter_chain",
        parameters=[shadow_config]
    )

    return LaunchDescription([scan_merger, shadow_filter])