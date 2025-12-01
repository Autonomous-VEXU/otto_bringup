#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory

def generate_launch_description():
    pkg_dir= get_package_share_directory('robot_bringup')
    config_file = os.path.join(pkg_dir, 'config', 'camera_params.yaml')
    
    camera_1 = Node( 
            package='usb_cam', 
            executable='usb_cam_node_exe', 
            output='screen',
            name='camera_1',
            parameters=[config_file]
    ) 
    camera_2 = Node( 
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_2',
        parameters=[config_file]
    )  
    camera_3 = Node( 
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_3',
        parameters=[config_file] 
    )  
    
    camera_4 = Node(
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_4',
        parameters=[config_file]
    )  
    
    return LaunchDescription([
        camera_1,
        camera_2,
        camera_3,
        camera_4
    ])