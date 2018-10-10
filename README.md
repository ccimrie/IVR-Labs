# Introduction to Vision and Robotics

## Installation guide

### Recommended: Virtual Machine Installation

The easiest way to get started is to use the provided VirtualBox image as follows:

1. Download the Ubuntu 16 image from [here](https://datasync.ed.ac.uk/index.php/s/wtlCUFKnAkujBDa). The password is: `ivr`
2. Import the image in VirtualBox following [these instructions](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html).
3. Start the virtual machine. It should automatically login and bring up a terminal window.
4. To check if everything works properly, type `python main.py` in the terminal. If everything was successful you should see the robot model on screen. That's it, you can start playing with the first tutorial :+1:

### On DICE machines

1. Clone this repo: `git clone https://github.com/ccimrie/IVR-Labs.git`
2. cd to cloned folder: `cd IVR-Labs`
3. Clear the pip cache which is in the home directory: `rm -rf ~/.cache/pip/`
4. Run the installation script: `source install.bash`
5. Check the [How to run](#how-to-run) section to test whether everything went as expected.

### If you are comfortable using the command line for installations then you can choose to install on your own machine

Keep in mind that the following instructions and scripts work in Ubuntu. If you are using Windows or any other operating system they won't work as expected. Consider using the VirtualBox image instead.

#### Without an existing Conda installation

1. Clone this repo: `git clone https://github.com/ccimrie/IVR-Labs.git`
2. cd to cloned folder: `cd IVR-Labs`
3. Install python-pip: `sudo apt install python-pip`
4. Upgrade python-pip: `sudo pip install --upgrade pip`
5. Install required packages: `sudo apt install autotools-dev libtool automake autoconf mercurial pkg-config`
6. Run the installation script: `source install.bash`
7. Check the [How to run](#how-to-run) section to test whether everything went as expected.

#### With an existing Conda installation

1. Clone this repo: `git clone https://github.com/ccimrie/IVR-Labs.git`
2. cd to cloned folder: `cd IVR-Labs`
3. Update conda to the latest version: `conda update --all`
4. Create a new python environment: `conda create --name ivrlabenv python=2.7 pip scipy numpy cython -y`
5. Activate environment: `conda activate ivrlabenv`. If you modified your PATH during the Conda installation you might receive a warning. Check [this part](https://github.com/conda/conda/blob/a4c4feae404b2b378e106bd25f62cc8be15c768f/CHANGELOG.md#recommended-change-to-enable-conda-in-your-shell) of the Changelog to fix it.
6. Run the installation script: `source conda_install.bash`
7. Check the [How to run](#how-to-run) section to test whether everything went as expected.

### How to run

On every new terminal you will have to navigate to the cloned folder and run `source setup.bash`.
This is to initialize the relevant environment variables.

If you want to avoid sourcing the setup.bash file with every new terminal, you can add it to you .bashrc file: `echo "source </path/to>/setup.bash" >> ~/.bashrc`.
Make sure you replace the `</path/to>` with the path to the setup file.

Also, in case you are using Conda, do not forget to activate the environment with `conda activate ivrlabenv` :+1: