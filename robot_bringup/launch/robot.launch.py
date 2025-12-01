#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, ExecuteProcess, IncludeLaunchDescription
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_dir = get_package_share_directory('robot_bringup')
    lidar_bringup_script = os.path.join(pkg_dir, 'scripts', 'lidar_bringup.bash')

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([
            FindPackageShare("robot_description"),
            "urdf",
            "x_drive.urdf.xacro"
        ])
    ])
    
    robot_description = {"robot_description": robot_description_content}

    controller_config = PathJoinSubstitution([
        FindPackageShare("robot_description"),
        "config",
        "omni_wheel_params.yaml"
    ])

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config],
        output="both",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    omni_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["omni_wheel_drive_controller", "--controller-manager", "/controller_manager"],
    )

    delay_omni_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[omni_controller_spawner],
        )
    )

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

    lidar_script =  ExecuteProcess(
        cmd=[lidar_bringup_script],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        delay_omni_controller
        # lidar_script
        #right_lidar,
        #left_lidar
    ])