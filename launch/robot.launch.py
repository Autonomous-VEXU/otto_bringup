#!/usr/bin/env python3
import os
import launch
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    default_model_path = PathJoinSubstitution([
        FindPackageShare('vex_robot'),
        'urdf',
        'x-drive.urdf.xacro'
    ])
    
    # Rviz configuration file 
    rviz_config = os.path.join(
        get_package_share_directory('vex_robot'), 
        'rviz', 
        'robot_visualizer.rviz'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )
    
    robot_state = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output="screen",
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')])
        }]
    )
    
    joints = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output="screen"
    )
    
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='model',
            default_value=default_model_path,
            description='path to robot model'
        ),
        joints,
        robot_state,
        rviz
    ])
