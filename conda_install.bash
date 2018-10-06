# Setup
WS=$PWD
green=$(tput setaf 2)
normal=$(tput sgr0)

printf "\n${green}Create installation folder${normal}\n\n"
mkdir VRInstall

printf "\n${green}Install required packages via apt${normal}\n\n"
sudo apt install cmake mercurial -y

printf "\n${green}Upgrade pip${normal}\n\n"
pip install --upgrade pip

printf "\n${green}Install OpenAI Gym and OpenCV${normal}\n\n"
pip install gym opencv-python

printf "\n${green}ODE installation${normal}\n\n"
hg clone https://bitbucket.org/odedevs/ode
mkdir ode-build
cd ode-build
cmake -G "Unix Makefiles" $WS/ode -DCMAKE_INSTALL_PREFIX=$WS/VRInstall -DODE_WITH_OU=true -DODE_WITH_LIBCCD=true -DODE_WITH_DEMOS=false
cmake --build . --target install

printf "\n${green}ODE python bindings installation${normal}\n\n"
cd $WS
source setup.bash
cd ode/bindings/python
pip install . -I --prefix $WS/VRInstall

cd $WS
printf "\n${green}Finished!${normal}\n"