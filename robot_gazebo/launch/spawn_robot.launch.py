#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart
import xacro

def generate_launch_description():
   
    # URDF/ file path stuff
    urdf_path = os.path.join(
        get_package_share_directory('robot_gazebo'),
          'models',
        'x_drive.urdf.xacro'
    )

    urdf = xacro.process_file(urdf_path).toxml()

    bridge_params = os.path.join(
        get_package_share_directory('robot_gazebo'),
        'config',
        'x_drive_bridge.yaml'
    )

    controllers_params = os.path.join(
        get_package_share_directory('robot_gazebo'),
        'config',
        'omni_wheel_params.yaml'
    )

    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='0.0',
        description='Specify namespace of the robot')

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='Specify namespace of the robot') 

    # robot_state_publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': urdf},
                    {'use_sim_time': True} ]
    ) 

    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'vex_robot',
            '-topic', '/robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'
        ],
        output='screen',
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[bridge_params],
        output='screen',
    )

    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen',
    )

    joint_state_broadcaster_spawner = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]
    )

    omni_controller_spawner = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['omni_wheel_drive_controller', '--controller-manager', '/controller_manager'],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]
    )

    ld = LaunchDescription([
        start_gazebo_ros_spawner_cmd,
        start_gazebo_ros_bridge_cmd,
        start_gazebo_ros_image_bridge_cmd,
        robot_state_publisher_node,
        joint_state_broadcaster_spawner,
        omni_controller_spawner
        ])

    # Declare the launch options
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)

    return ld
