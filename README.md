# Obstacle_Avoidance_2025-2026
A repository containing Project Astra Obstacle Avoidance team's ROS packages and tools.

# Prerequisites
Ubuntu 20.04

ROS noetic:<br/>
https://wiki.ros.org/ROS/Installation/TwoLineInstall/

Ardupilot:<br/>
https://ardupilot.org/dev/docs/building-setup-linux.html

MAVROS:<br/>
https://ardupilot.org/dev/docs/ros-install.html

Gazebo:<br/>
https://github.com/khancyr/ardupilot_gazebo


# Usage
`cd ~/catkin_ws/src`

`git clone --recurse-submodules https://github.com/CPP-Aerial-Vision-Analysis-System/Obstacle_Avoidance_2025-2026.git`

`cd ~/catkin_ws`

`catkin_make`

# Currently working one line node/sim scripts:
Launch unilidar_ros node:<br/>
`roslaunch unitree_lidar_ros run.launch`<br/>
documentation here: https://github.com/unitreerobotics/unilidar_sdk/tree/main/unitree_lidar_ros/src/unitree_lidar_ros

Launch rplidar_ros node:<br/>
`roslaunch rplidar_ros rplidar_a2m12.launch`<br/>
documentation here: https://github.com/Slamtec/rplidar_ros

Launch an iris drone with a simulated 3D LiDAR:<br/>
`roslaunch velodyne_description iris-unitree.launch # add gpu:=true if not running linux on a VM`

Launch 2D avoidance using the method of potential fields:<br/>
`sh src/Obstacle_Avoidance_2025-2026/Scripts/script/runIQsim.sh`
