# Introduction to Vision and Robotics
## Table of Contents
- [Installation guide](#installation-guide)	
- [How to run](#how-to-run)

## Installation guide
1. Install git: `sudo apt install git`
2. Clone this repo: `git clone https://github.com/ccimrie/IVR-Labs.git`
3. cd to cloned folder: `cd IVR-Labs`

Follow the next steps according to your situation.

### Only on DICE machines
4. Run installation script: `source install.bash` :+1:

### Only on self-managed machines (Non-DICE or VM)
#### Without an existing Conda installation
4. Install python-pip: `sudo apt install python-pip`
5. Upgrade python-pip: `sudo pip install --upgrade pip`
6. Install required packages: `sudo apt install autotools-dev libtool automake autoconf mercurial pkg-config`
7. Run installation script: `source install.bash` :+1:

#### With an existing Conda installation
4. Create a new python environment: `conda create --name ivrlabenv python=2.7 pip scipy numpy cython -y`
5. Activate environment: `conda activate ivrlabenv`
6. Run installation script: `source conda_install.bash` :+1:

## How to run
On every new terminal you will have to navigate to the cloned folder and run `source setup.bash`.
This is to initialize the relevant environment variables.

If you want to avoid sourcing the setup.bash file with every new terminal, you can add it to you .bashrc file: `echo "source </path/to>/setup.bash" >> ~/.bashrc`.
Make sure you replace the `</path/to>` with the path to the setup file.

Also, in case you are using Conda, do not forget to activate the environment with `conda activate ivrlabenv`