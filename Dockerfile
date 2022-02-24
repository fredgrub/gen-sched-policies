FROM ubuntu:16.04

# system-wide dependencies
RUN apt-get -yq update && apt-get install -y \
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
RUN apt-get install -y python-scipy python-numpy python-matplotlib

# build variables
ARG BUILD_ROOT=/opt
ARG TARGET_DIR=/opt/simgrid
ARG CLONE_DIR=simgrid-313
ARG SIMGRID_URL=https://framagit.org/simgrid/simgrid.git
ARG SIMGRID_VERSION=v3_13

# prepare
WORKDIR ${BUILD_ROOT}
RUN rm -f ${TARGET_DIR} && ln -s ${CLONE_DIR} ${TARGET_DIR}

# clone
RUN git clone -b ${SIMGRID_VERSION} --single-branch ${SIMGRID_URL} ${CLONE_DIR}

# build
WORKDIR ${TARGET_DIR}
RUN cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=${TARGET_DIR}
RUN make && make check && make install
RUN ln -s /opt/simgrid/lib/libsimgrid.so /usr/lib/libsimgrid.so && \
ln -s /opt/simgrid/lib/libsimgrid.so.3.13 /usr/lib/libsimgrid.so.3.13

WORKDIR /usr/src/dev

