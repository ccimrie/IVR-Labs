WS=$PWD
pip install -I --prefix $WS/VRInstall --upgrade pip
export PATH=$PWD/VRInstall/bin:$PATH
pip install cython -I --prefix $WS/VRInstall
pip install numpy -I --prefix $WS/VRInstall
pip install scipy -I --prefix $WS/VRInstall
pip install gym -I --prefix $WS/VRInstall
hg clone https://bitbucket.org/odedevs/ode
cd ode
echo "Running aclocal"
aclocal --force -I m4 --install || exit 1
echo "Running libtoolize"
libtoolize --force --copy --automake --install || exit 1
echo "Running autoheader"
autoheader || exit 1
echo "Running automake"
automake --foreign --add-missing --copy || exit 1
echo "Running autoconf"
autoconf || exit 1
chmod +x ou/bootstrap
echo "Running bootstrap in ou directory"
(cd ou && ./bootstrap)
chmod +x libccd/bootstrap
if [ -d libccd ]; then
    echo "Running bootstrap in libccd directory"
    (cd libccd && ./bootstrap)
fi;

#echo "Now you are ready to run ./configure"
./configure --prefix=$WS/VRInstall --disable-demos --enable-shared --enable-static --with-pic

make install
cd $WS
source setup.bash
cd ode/bindings/python
pip install . -I --prefix $WS/VRInstall
pip install opencv-python -I --prefix $WS/VRInstall
cd $WS
source setup.bash
echo "Finished!\n"
