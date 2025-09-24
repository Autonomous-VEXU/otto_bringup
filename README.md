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

### robot_gazebo
Gazebo Harmonic implementation of an x drive holonomic robot.

Package File Tree:
```
/robot_gazebo
├── /config
│   ├── omni_wheel_params.yaml
│   ├── x_drive_bridge.yaml
│   └── xbox_controller.yaml
├── /launch
│   ├── controller.launch.py
│   ├── empty_world.launch.py
│   └── spawn_robot.launch.py
├── /models
│   └── x_drive.urdf.xacro
├── CMakeLists.txt
└── package.xml
```

Inertia Matrix Calculators:</br>
[cylinder/wheels](https://amesweb.info/inertia/mass-moment-of-inertia-cylinder.aspx)</br>
[rectangle/chassis](https://amesweb.info/inertia/moment-of-inertia-of-rectangular-plate.aspx)
