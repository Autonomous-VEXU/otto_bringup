import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration

def yaml_to_node_arguments(params): 
    # parse yaml file based on 
    return [f"{key}:={value}" for key, value in params.items()]

def launch_setup(context):

    # tell which lidar this is
    side = LaunchConfiguration('side').perform(context)

    # get yaml parameters
    robot_dir = get_package_share_directory('robot_bringup')
    config_file = os.path.join(robot_dir, 'config', 'lidar_config.yaml')
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    if side not in config:
        raise RuntimeError(f"Side '{side}' config not found in yaml! Options: {list(config.keys())}")

    # build node args
    sick_scan_pkg_prefix = get_package_share_directory('sick_scan_xd')
    # launchfile = os.path.basename(__file__)[:-3]  # "<lidar_name>.launch"
    launchfile = "sick_tim_7xxS.launch" # this is so dumb imo
    launch_file_path = os.path.join(sick_scan_pkg_prefix, 'launch', launchfile)
    node_arguments = [launch_file_path] + yaml_to_node_arguments(config[side])

    # from original launch file (sick_scan_xd/launch/sick_tim_7xxS.launch.py)
    ROS_DISTRO = os.environ.get('ROS_DISTRO', '')
    if ROS_DISTRO and ROS_DISTRO[0] <= 'e':
        node = Node(
            package='sick_scan_xd',
            node_executable='sick_generic_caller',
            output='screen',
            arguments=node_arguments
        )
    else:
        node = Node(
            package='sick_scan_xd',
            executable='sick_generic_caller',
            output='screen',
            arguments=node_arguments
        )
    return [node]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'side',
            default_value='right',
            description="Select which lidar to use: left or right"
        ),
        OpaqueFunction(function=launch_setup)
    ])