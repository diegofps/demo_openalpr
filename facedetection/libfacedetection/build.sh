#!/bin/bash

SRCS="facedetectcnn.cpp facedetectcnn-int8data.cpp facedetectcnn-model.cpp"
LIBFLAGS="-Wall -O3 -std=c++11 `pkg-config opencv --libs`"
LIBNAME="libpyfacedetection.so"
DEMONAME="demo"
OPTION=$1


if [ -z "$OPTION" ]; then
    echo "Sintax: $0 <lib|demo|deploy>"
    exit 0
fi

if [ $OPTION == "lib" ]; then

    ARCH=`uname -m`

    if [ $ARCH == "x86_64" ]; then
        echo "Building for amd64"
        clang++ -fPIC -shared ${LIBFLAGS} ${SRCS} pyfacedetectioncnn.cpp -o ${LIBNAME} -mavx2 -mfma -D_ENABLE_AVX2

    elif [ $ARCH == "aarch64" ]; then
        echo "Building for arm64"
        clang++ -fPIC -shared ${LIBFLAGS} ${SRCS} pyfacedetectioncnn.cpp -o ${LIBNAME} -D_ENABLE_NEON

    else
        echo "Unknown arch: ${ARCH}"
        exit 1

    fi

elif [ $OPTION == "demo" ]; then

    ARCH=`uname -m`

    if [ $ARCH == "x86_64" ]; then
        echo "Building for amd64"
        clang++ ${LIBFLAGS} ${SRCS} detect-image.cpp -o ${DEMONAME} -mavx2 -mfma -D_ENABLE_AVX2 

    elif [ $ARCH == "aarch64" ]; then
        echo "Building for arm64"
        clang++ ${LIBFLAGS} ${SRCS} detect-image.cpp -o ${DEMONAME} -D_ENABLE_NEON

    else
        echo "Unknown arch: ${ARCH}"
        exit 1

    fi

elif [ $OPTION == "deploy" ]; then
    mkdir -p /project
    cp /libfacedetection/${LIBNAME} /project

else
    echo "Unknown option: $OPTION"

fi
