# Kevin_branch

## MAVROS download

### Install MAVROS:
```
sudo apt update
sudo apt install ros-humble-mavros ros-humble-mavros-extras
```

### Install MAVROS Dependencies
GeographicLib datasets are required by MAVROS for accurate GPS to local coordinate conversions
```
source /opt/ros/humble/setup.bash
sudo apt install geographiclib-tools
sudo /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh
```




## Ardupilot Download
Download dependencies for ardupilot
```
sudo apt update
sudo apt install git python3 python3-pip python3-dev build-essential
```

#Clone Github
```
cd ~
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive
```
### Install SITL tools
```
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
echo 'export PATH=$PATH:$HOME/ardupilot/Tools/autotest' >> ~/.bashrc
source ~/.bashrc
```

### Configure Ardupilot
Set board to sitl, cube-orange, cube-black...
```
cd ~/ardupilot
./waf configure --board CubeOrange
./waf copter

```

### Run ardupilot

```
cd ~/ardupilot
Tools/autotest/sim_vehicle.py -v ArduCopter -f quad --console --map
```

## Installing Gazebo

```

#Initialize 
sudo apt update
sudo apt install lsb-release wget gnupg
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/gazebo-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gazebo-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list

Install gazebo
sudo apt update
sudo apt install gz-harmonic

# Add to .bashrc
echo 'export GZ_VERSION=harmonic' >> ~/.bashrc
source ~/.bashrc

# ROS2 - GZ bridge
sudo apt install ros-humble-ros-gz


```

## Ardu-GZ
```
# Prereqs
sudo apt update
sudo apt install python3-vcstool python3-rosdep2 -y



```