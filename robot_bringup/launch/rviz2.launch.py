#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
  rviz_config_dir = os.path.join( # get path to Rviz2 config file
    get_package_share_directory('robot_description'),
    'rviz',
    'model.rviz')
  
  rviz = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    arguments=['-d', rviz_config_dir],
    output='screen'
  )
  
  static_world_to_odom = Node(
    package="tf2_ros",
    executable="static_transform_publisher",
    name="static_world_to_odom_broadcaster",
    arguments=["0", "0", "0", "0", "0", "0", "world", "odom"],
    output="screen"
  )

  return LaunchDescription([
    static_world_to_odom,
    rviz
  ])