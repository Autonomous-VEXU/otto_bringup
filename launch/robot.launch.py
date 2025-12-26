#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, IncludeLaunchDescription, DeclareLaunchArgument
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from launch.conditions import IfCondition


'''Top level launch file for launching all of the controllers and sensors on Otto'''

def generate_launch_description():

    # package directories
    pkg_dir = get_package_share_directory('otto_bringup')

    # camera launch argument
    launch_cams = LaunchConfiguration('cams')
    launch_cams_cmd = DeclareLaunchArgument(
        'cams',
        default_value='false',
        description='toggle for camera nodes being launched'
    )

    # lidar launch argument
    launch_lidar = LaunchConfiguration('lidar')
    launch_lidar_cmd = DeclareLaunchArgument(
        'lidar',
        default_value='true',
        description='toggle for lidar nodes being launched'
    )

    # conditionally select URDF
    urdf_file = PythonExpression([
        "'otto.urdf.xacro' if '",
        launch_cams,
        "' == 'true' else 'otto_lite.urdf.xacro'"
    ])

    # robot URDF/Xacro processing
    robot_description_urdf = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([
            FindPackageShare("otto_description"),
            "robot",
            urdf_file
        ])
    ])

    robot_description = {"robot_description": robot_description_urdf}

    # ros2_control nodes + controller managers
    controller_config = PathJoinSubstitution([
        FindPackageShare("otto_description"),
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

    # lidar bringup 
    right_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'tim7xxS.launch.py')
        ),
        condition=IfCondition(launch_lidar),
        launch_arguments={'side':'right'}.items()
    )

    left_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'tim7xxS.launch.py')
        ),
        condition=IfCondition(launch_lidar),
        launch_arguments={'side':'left'}.items()
    )

    # camera bringup
    robot_cams = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'robot_cams.launch.py')
        ),
        condition=IfCondition(launch_cams)
    )

    return LaunchDescription([
        launch_cams_cmd,
        launch_lidar_cmd,
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        delay_omni_controller,
        right_lidar,
        left_lidar,
        robot_cams
    ])