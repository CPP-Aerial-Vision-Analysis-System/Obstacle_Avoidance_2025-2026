#!/usr/bin

gnome-terminal --title Gazebo --working-directory=/home/suas/Desktop/Obstacle_Avoidance_2024-2025/ROS-IQ-Tutorials -e "bash -c 'roslaunch iq_sim lidar.launch'"

sh ~/catkin_ws/src/Obstacle_Avoidance_2025-2026/Scripts/script/runSitl.sh

sleep 10

gnome-terminal --title MavROS --working-directory=/home/suas/Desktop/Obstacle_Avoidance_2024-2025/ROS-IQ-Tutorials -e "bash -c 'roslaunch iq_gnc apm.launch'"

gnome-terminal --title IQAvoidance --working-directory=/home/suas/Desktop/Obstacle_Avoidance_2024-2025/ROS-IQ-Tutorials -e "bash -c 'rosrun iq_gnc avoidance3D_sol'"