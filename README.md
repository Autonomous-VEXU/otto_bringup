# vex_robot
Simulation packages for an x-drive vex like holonomic robot.

Core dependencies:
- ros2_control
- gz_ros2_control

### robot_bringup
Package for launching the robot on hardware. </br>

Package File Tree:
```
/robot_bringup
├── /config
│   └── omni_wheel_params.yaml
├── /launch
│   ├── robot.launch.py
│   └── rviz2.launch.py
├── CMakeLists.txt
└── package.xml
```

### robot_description
Files + CAD models that describe the robot's physical properties. </br>

Package File Tree:
```
/robot_description
├── /models
│   ├── chassis_1.stl
│   ├── chassis.dae
│   ├── wheel.dae
│   └── wheel.stl
├── /rviz
│   └── model.rviz
├── /urdf
│   └── x_drive.urdf.xacro
├── CMakeLists.txt
└── package.xml
```
