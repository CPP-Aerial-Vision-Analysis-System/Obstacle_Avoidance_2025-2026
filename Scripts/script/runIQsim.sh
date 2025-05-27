#!/bin/bash

gnome-terminal --title Gazebo --working-directory=$HOME/catkin_ws -- bash -c "roslaunch iq_sim lidar.launch"

sh ~/catkin_ws/src/Obstacle_Avoidance_2025-2026/Scripts/script/runSitl.sh

sleep 10

gnome-terminal --title MavROS --working-directory=$HOME/catkin_ws -- bash -c "roslaunch iq_gnc apm.launch"

gnome-terminal --title IQAvoidance --working-directory=$HOME/catkin_ws -- bash -c "rosrun iq_gnc avoidance_sol"