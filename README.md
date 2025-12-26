# otto_bringup
Package for initializing robot hardware. Contains top level and sensor subsystem launch files for Otto. </br>

#### Package File Tree:
```
otto_bringup/
├── config/
│   ├── lidar_config.yaml
│   └── xbox_controller.yaml
├── launch/
│   ├── controller.launch.py
│   ├── robot_cams.launch.py
│   ├── robot.launch.py
│   └── tim7xxS.launch.py
├── CMakeLists.txt
└── package.xml
```

## Launch Files
Robot launch file: `robot.launch.py`

## controller.launch.py
_Allows for driving the robot with a game controller, does this by publishing messages to `/cmd_vel`</br>_
```yaml
controller_name: 'xbox_controller.yaml' # name of the config file you want to use
joy_dev: 0 # Device and/or controller ID
publish_twist_stamped: true # Toggle for publishing Twist vs TwistStamped messages
```

## robot_cams.launch.py
_Launches all four USB cameras on Otto</br>_
> Note: This is only used if the full robot is being brought up when launching `robot.launch.py`

## robot.launch.py
_The top level bringup launch file for Otto. Includes LiDAR, camera (optional), and ros2 controllers </br>_
```yaml
cams: False # toggles camera bringup
lidar: True # toggles lidar bringup
```

## tim7xxS.launch.py
_A reworked version of SICK's launch file. Allows for passing parameters through a YAML config file.</br>_
```yaml
side: 'right' # which side of the robot the lidar is located
```
> see `config/lidar_config.yaml` for more parameters and options. look at the repository `sick_scan_xd` for the full set of available parameters.

## Configuration Files
- `lidar_config.yaml`: parameters for `tim7xxS.launch.py`
- `xbox_controller.yaml`: parameters for `controllers.launch.py`

## Links + Resources
- LiDAR driver repository: [SICKAG/sick_scan_xd](https://github.com/SICKAG/sick_scan_xd)
- [ROS Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [ROS 2 Launch docs](https://docs.ros.org/en/jazzy/p/launch/)
