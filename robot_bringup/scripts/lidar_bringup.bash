#!/bin/bash

# launch both lidars
ros2 launch sick_scan_xd sick_tim_7xxS.launch.py hostname:=192.168.0.51 __ns:=/right frame_id:=r_laser tf_base_frame_id:=laser_frame_2 & \
ros2 launch sick_scan_xd sick_tim_7xxS.launch.py hostname:=192.168.0.50 __ns:=/left frame_id:=l_laser tf_base_frame_id:=laser_frame_1

# LEFT LIDAR --> 1
# RIGHT LIDAR --> 2