#!/bin/usr/python

# paths to urdf, 
# need param called robot_description to 
# robot state publisher
# joint state publisher

import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='vex_robot').find('vex_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/x-drive.urdf.xacro')
    #default_rviz_config_path = os.path.join(pkg_share, 'rviz/config.rviz')

    robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
    )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        joint_state_publisher,
        robot_state_publisher,
        rviz_node
    ])
