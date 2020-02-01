FROM atlas/athanalysis:21.2.104
ADD . /analysis/src
WORKDIR /analysis/build
RUN source ~/release_setup.sh &&  \
    sudo chown -R atlas /analysis && \
    cmake ../src && \
    make -j4


