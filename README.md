# Lego EV3 Wiimote control car

This repo includes instructions for installation and files on running cwiid module on python3 ev3dev2

To run this python file and all dependencies:

## Preparation of EV3 brick and computer
1. Install ev3dev (preferably 16GB SD card)
    - [https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3]
2. Ensure you have Visual Studio Code installed with the `ev3dev-browser` extension installed

## Setup connection
3. Connect to the brick via USB (recommended)/Bluetooth
4. Follow instructions here to connect to Internet via SSH (password is maker)
    - USB: [https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb]
    - Bluetooth: [https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/]

## Updating and installing dependencies
5. Ensure the time is correct on brick, factor in timezone by runnning `date` on SSH
    a. If time is not synced, run
        ```sudo service ntp stop
        sudo ntpd -gq
        sudo service ntp start```
    and restart the brick
6. Run `sudo apt update && sudo apt upgrade` (may take up to 1 hour)
7. Once updates is complete, restart brick
8. Reconnect to brick and run
9. Run `sudo apt install git` to ensure git is installed

## Installing python3-cwiid module
10. `git clone https://github.com/azzra/python3-wiimote.git` to download the python3-cwiid module
11. Installing essentials for building module:
    - `sudo apt install build-essential python3-dev flex bison bluez-tools bluez-hcidump bluez autotools-dev automake g++ libcwiid1`
12. Enter the folder you cloned earlier `cd python3-wiimote`
13. Run the following build commands
```sh
aclocal
autoconf
./configure
make
sudo make install
```
14. Run `cd ..` to exit the folder (do not delete this folder)

## Download code
14. `git clone https://github.com/NYP-RoboticsSG/LegoCar.git` to download this code
15. Run `main.py` from the EV3 File Browser. Enjoy!
