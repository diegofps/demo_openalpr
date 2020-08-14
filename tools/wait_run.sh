#!/bin/bash

CC=`sudo kubectl get pods | grep Pending | wc -l`
PE=`sudo kubectl get pods | grep ContainerCreating | wc -l`
EIP=`sudo kubectl get pods | grep ErrImagePull | wc -l`
IPBF=`sudo kubectl get pods | grep ImagePullBackOff | wc -l`

while [ $CC != '0' -o $PE != '0' ]
do
    echo "Pods are still starting: ContainerCreating=$CC, Pending=$PE"
    sleep 1
    CC=`sudo kubectl get pods | grep Pending | wc -l`
    PE=`sudo kubectl get pods | grep ContainerCreating | wc -l`
    EIP=`sudo kubectl get pods | grep ErrImagePull | wc -l`
    IPBF=`sudo kubectl get pods | grep ImagePullBackOff | wc -l`
done

