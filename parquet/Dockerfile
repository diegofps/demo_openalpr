FROM ubuntu:18.04

ENV DEBIAN_FRONTEND="noninteractive"
ENV LANGUAGE="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LANG="en_US.UTF-8"

RUN apt update && apt install language-pack-en -yq

# DEPENDENCIES

RUN apt install build-essential git cmake ninja-build libboost-all-dev flex bison \
    libre2-dev llvm-7-dev libssl-dev libgtest-dev liburiparser-dev \
    libbrotli-dev protobuf-compiler protobuf-c-compiler \
    python3 python3-pip -yq

RUN pip3 install cython pytest psutil lz4 re2 six
RUN pip3 install numpy
RUN pip3 install pandas

# ARROW

RUN git clone --recursive https://github.com/apache/arrow.git

WORKDIR /arrow
RUN git checkout maint-0.15.x

ENV ARROW_HOME="/usr/local"
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

WORKDIR /arrow/cpp/build

RUN apt install clang -yq

RUN cmake .. \
      -DCMAKE_INSTALL_PREFIX=$ARROW_HOME \
      -DCMAKE_INSTALL_LIBDIR=lib  \
      -DARROW_FLIGHT=ON \
      -DARROW_GANDIVA=ON  \
      -DARROW_ORC=ON  \
      -DARROW_WITH_BZ2=ON \
      -DARROW_WITH_ZLIB=ON  \
      -DARROW_WITH_ZSTD=ON  \
      -DARROW_WITH_LZ4=ON \
      -DARROW_WITH_SNAPPY=ON  \
      -DARROW_WITH_BROTLI=ON  \
      -DARROW_PARQUET=ON  \
      -DARROW_PYTHON=ON \
      -DARROW_PLASMA=ON \
      -DARROW_CUDA=OFF \
      -DARROW_BUILD_TESTS=OFF \
      -DARROW_BUILD_EXAMPLES=ON \
      -DARROW_BUILD_BENCHMARKS=ON \
      -DARROW_BUILD_BENCHMARKS_REFERENCE=ON \
      -DARROW_BUILD_UTILITIES=ON \
      -DPARQUET_BUILD_EXECUTABLES=ON \
      -DPARQUET_BUILD_EXAMPLES=ON \
      -DPYTHON_EXECUTABLE=/usr/bin/python3

RUN make -j `nproc`
RUN make install

# PYARROW

WORKDIR /arrow/python

RUN pip3 install -r requirements.txt && python3 -m pip install --user --upgrade setuptools wheel twine

ENV PYARROW_WITH_FLIGHT=1
ENV PYARROW_WITH_GANDIVA=1
ENV PYARROW_WITH_ORC=1
#ENV PYARROW_WITH_CUDA=1
ENV PYARROW_WITH_PARQUET=1
ENV PYARROW_WITH_PLASMA=1

RUN ln -s /usr/local/lib/libparquet.so /usr/local/lib/libparquet_shared.so

ENV PARQUET_HOME="/usr/local"

RUN python3 setup.py build_ext --inplace
RUN python3 setup.py sdist
RUN pip3 install dist/pyarrow-0.15.1.dev36*.tar.gz
