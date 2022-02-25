#!/bin/bash

# system-wide dependencies
sudo apt-get -yq update && sudo -yq apt-get install \
python2.7 \
git \
gcc-4.8 \
g++-4.8 \
g++ \
cmake \
libboost-context-dev \
libboost-dev \
doxygen \
transfig

# python dependencies
sudo apt-get install -yq python-scipy python-numpy python-matplotlib

# build variables
export BUILD_ROOT=/opt
export TARGET_DIR=/opt/simgrid
export CLONE_DIR=simgrid-313
export SIMGRID_URL=https://framagit.org/simgrid/simgrid.git
export SIMGRID_VERSION=v3_13

# prepare
cd ${BUILD_ROOT}
sudo rm -f ${TARGET_DIR} && ln -s ${CLONE_DIR} ${TARGET_DIR}

# clone
sudo git clone -b ${SIMGRID_VERSION} --single-branch ${SIMGRID_URL} ${CLONE_DIR}

# build
cd ${TARGET_DIR}
sudo cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=${TARGET_DIR}
sudo make && make check && make install
sudo ln -s /opt/simgrid/lib/libsimgrid.so /usr/lib/libsimgrid.so && \
ln -s /opt/simgrid/lib/libsimgrid.so.3.13 /usr/lib/libsimgrid.so.3.13
