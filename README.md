# K9-Buddy
K9-Buddy is an open-source quadruped robot designed to promote STEAM education and provide a solid foundation for competing in robotics events. Notable for its low cost, K9-Buddy is accessible to both students and robotics enthusiasts.
<p align="center">
  <img src="images/1.png" alt="K9-Buddy" width="500"/>
</p>

### Environment Setup
1. Update the System
   
Open a terminal and run the following commands to update the package list and upgrade the installed packages to their latest versions:
```
sudo apt-get update
sudo apt-get upgrade
```
2. Install Python and Pip 
```
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
```
3. Enable I2C and SSH services
   
Open the Raspberry Pi configuration menu
```
sudo raspi-config
```
Navigate to Interfacing Options > I2C and select Yes to enable I2C.
Navigate to Interfacing Options > SSH and select Yes to enable SSH.
Restart the Raspberry Pi to apply the changes:
```
sudo reboot
```
4. Install Additional Packages
   
Open a terminal and run the following commands:
```
# Install python-smbus and i2c-tools
sudo apt-get install -y python3-smbus
sudo apt-get install -y i2c-tools

# Verify the I2C connection
sudo i2cdetect -y 1

# Install Adafruit CircuitPython ServoKit
sudo pip3 install adafruit-circuitpython-servokit
```

### Usage
1. Cloning the Repository
```
git clone https://github.com/caulesti/k9-buddy.git
```
2. Grant permissions to the script
```
chmod +x k9-buddy/software/k9_buddy.py
```
3. Execution
```
python3 k9-buddy/software/k9_buddy.py
```
