#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # file paths and packages
    pkg_dir = get_package_share_directory('otto_bringup')
    scan_merger_pkg = get_package_share_directory('laser_scan_merger')

    shadow_config = PathJoinSubstitution(pkg_dir, "config", "shadow_filter.yaml")

    # scan merger argument
    merge_scans = LaunchConfiguration('scan_merge')
    merge_scans_cmd = DeclareLaunchArgument(
        'scan_merge',
        default_value='true',
        description='toggle for merging lidar scans'
    )

    # scan filter argument
    scan_filter = LaunchConfiguration('scan_filter')
    scan_filter_cmd = DeclareLaunchArgument(
        'scan_filter',
        default_value='true',
        description='toggle for filtering lidar scans'
    )

    # lidar bringup 
    right_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'tim7xxS.launch.py')
        ),
        launch_arguments={'side':'right'}.items()
    )

    left_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'tim7xxS.launch.py')
        ),
        launch_arguments={'side':'left'}.items()
    )

    # laser_scan_merger launch file
    scan_merger = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(scan_merger_pkg, 'launch', 'start.launch.py')
        ),
        launch_arguments={'robotname':'otto'}.items(),
        condition=IfCondition(merge_scans)
    )

    # shadow filter for lidar
    shadow_filter = Node(
        package="laser_filters",
        executable="scan_to_scan_filter_chain",
        parameters=[shadow_config],
        condition=IfCondition(scan_filter)
    )
  
    return LaunchDescription([
        merge_scans_cmd,
        scan_filter_cmd,
        right_lidar,
        left_lidar,
        scan_merger,
        shadow_filter
  ])