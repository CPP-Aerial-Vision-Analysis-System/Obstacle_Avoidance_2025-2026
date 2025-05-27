# Obstacle_Avoidance_2025-2026
A repository containing Project Astra Obstacle Avoidance team's ROS packages and tools.

# Prerequisites
ROS noetic: https://wiki.ros.org/ROS/Installation/TwoLineInstall/

ardupilot: https://ardupilot.org/dev/docs/building-setup-linux.html

MAVROS: https://ardupilot.org/dev/docs/ros-install.html

Gazebo: https://github.com/khancyr/ardupilot_gazebo


# Usage
`cd ~/catkin_ws/src`

`git clone --recurse-submodules https://github.com/CPP-Aerial-Vision-Analysis-System/Obstacle_Avoidance_2025-2026.git`

`cd ~/catkin_ws`

`catkin_make`

# Currently working one line ROS launches:
launch an iris drone with a simulated 3D LiDAR: `roslaunch velodyne_description iris-unitree.launch`
