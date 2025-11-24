#!/bin/bash

# launch both lidars
ros2 launch sick_scan_xd sick_tim_7xxS.launch.py hostname:=192.168.0.51 __ns:=/right frame_id:=laser_frame_1 & \
ros2 launch sick_scan_xd sick_tim_7xxS.launch.py hostname:=192.168.0.50 __ns:=/left frame_id:=laser_frame_2

