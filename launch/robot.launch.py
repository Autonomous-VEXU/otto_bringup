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
from launch_ros.parameter_descriptions import ParameterValue

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

    # device that the robot is being run on
    jetson = LaunchConfiguration('jetson')
    launch_jetson_cmd = launch_sensors_cmd = DeclareLaunchArgument(
        'jetson',
        default_value='false',
        description='robot is being run on the Jetson Orin'
    )

    serial_port = PythonExpression(["'/dev/ttyACM0' if '", jetson, "' == 'true' else '/dev/ttyTHS1'"])
    mock_hw = PythonExpression(["'false' if '", jetson, "' == 'true' else 'true'"])

    # misc sensors (imu / color sensor / fuel gauge) launch arg
    launch_sensors = LaunchConfiguration('sensors')
    launch_sensors_cmd = DeclareLaunchArgument(
        'sensors',
        default_value='false',
        description='toggle for the other sensor nodes being launched'
    )
    
    # robot URDF/Xacro processing
    urdf_path = PathJoinSubstitution([FindPackageShare('otto_description'), "robot", 'otto.urdf.xacro'])

    robot_description_urdf = ParameterValue(
        Command(['xacro ', urdf_path, 
                 ' mock_hw:=', mock_hw,
                 ' cams:=', launch_cams,
                 ' serial_port:=', serial_port,]),
        value_type=str
    )

    robot_description = {"robot_description": robot_description_urdf}

    # ros2_control nodes + controller managers
    controller_config = PathJoinSubstitution([FindPackageShare("otto_description"), "config", "ros2_control.yaml"])

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
        remappings=[
        ('/omni_wheel_drive_controller/cmd_vel', "/cmd_vel"),
        ('/omni_wheel_drive_controller/odom', '/odom'),
        ('/intake_low_controller/commands','/intake_vel_1'),
        ('/intake_mid_controller/commands','/intake_vel_2'),
        ('/intake_high_controller/commands','/intake_vel_3')
        ],
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
        arguments=["omni_wheel_drive_controller", "--controller-manager", "/controller_manager"]
    )

    intake1_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["intake_low_controller", "--controller-manager", "/controller_manager"]
    )

    intake2_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["intake_mid_controller", "--controller-manager", "/controller_manager"]
    )

    intake3_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["intake_high_controller", "--controller-manager", "/controller_manager"]
    )

    delay_controller_spawners = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[omni_controller_spawner, intake1_controller_spawner, intake2_controller_spawner, intake3_controller_spawner]
        )
    )

    # imu / color sensor / battery gauge launch file
    misc_sensors = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'sensors.launch.py')
        ),
        condition=IfCondition(launch_sensors)
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
        launch_sensors_cmd,
        launch_jetson_cmd,
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        delay_controller_spawners,
        misc_sensors,
        right_lidar,
        left_lidar,
        robot_cams
    ])