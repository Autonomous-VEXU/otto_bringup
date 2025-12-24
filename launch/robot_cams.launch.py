#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction, DeclareLaunchArgument
from ament_index_python import get_package_share_directory

def generate_launch_description():
    # directory file paths
    config_dir= get_package_share_directory('otto_description')
    config_file = os.path.join(config_dir, 'config', 'camera_params.yaml')

    # camera nodes
    camera_1 = Node( 
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_1',
        remappings=[
            ('/image_raw', 'cam1/image_raw'),
            ('/camera_info', 'cam1/camera_info'),
            ('image_raw/compressed', 'cam1/image_raw/compressed')
        ],
        #namespace='c1',
        parameters=[config_file]
    ) 
    
    camera_2 = Node( 
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_2',
        remappings=[
            ('/image_raw', 'cam2/image_raw'),
            ('/camera_info', 'cam2/camera_info'),
            ('image_raw/compressed', 'cam2/image_raw/compressed')
        ],

        #namespace='c2',
        parameters=[config_file]
    )  

    camera_3 = Node( 
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_3',
        remappings=[
                ('/image_raw', 'cam3/image_raw'),
                ('/camera_info', 'cam3/camera_info'),
                ('image_raw/compressed', 'cam3/image_raw/compressed') 
            ],
        parameters=[config_file] 
    )  
    
    camera_4 = Node(
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='camera_4',
        remappings=[
                ('/image_raw', 'cam4/image_raw'),
                ('/camera_info', 'cam4/camera_info'),
                ('image_raw/compressed', 'cam4/image_raw/compressed') 
            ],
        parameters=[config_file]
    )  
    
    # delays for the camera nodes to prevent crashing
    timer_2 = TimerAction( 
        period=2.0,
        actions=[camera_2]
    )

    timer_3 = TimerAction(
        period=5.0,
        actions=[camera_3]
    )

    timer_4 = TimerAction(
        period=8.0,
        actions=[camera_4]
    )
    
    return LaunchDescription([
        camera_1,
        timer_2,
        timer_3,
        timer_4
    ])