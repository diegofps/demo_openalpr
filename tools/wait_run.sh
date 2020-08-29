#!/bin/bash

function summary
{
    echo "Summary: ContainerCreating=$CC, Pending=$PE, ErrImagePull=$EIP, ImagePullBackOff=$IPBF, CrashLoopBackOff=$CLBO, Error=$ERR, Running=$RUN"
}

sleep 1

CC=`sudo kubectl get pods | grep ContainerCreating | wc -l`
PE=`sudo kubectl get pods | grep Pending | wc -l`
EIP=`sudo kubectl get pods | grep ErrImagePull | wc -l`
IPBF=`sudo kubectl get pods | grep ImagePullBackOff | wc -l`
CLBO=`sudo kubectl get pods | grep CrashLoopBackOff | wc -l`
ERR=`sudo kubectl get pods | grep Error | wc -l`
RUN=`sudo kubectl get pods | grep Running | wc -l`

summary

while [ $CC != '0' -o $PE != '0' ]
do
    sleep 1

    CC=`sudo kubectl get pods | grep ContainerCreating | wc -l`
    PE=`sudo kubectl get pods | grep Pending | wc -l`
    EIP=`sudo kubectl get pods | grep ErrImagePull | wc -l`
    IPBF=`sudo kubectl get pods | grep ImagePullBackOff | wc -l`
    CLBO=`sudo kubectl get pods | grep CrashLoopBackOff | wc -l`
    ERR=`sudo kubectl get pods | grep Error | wc -l`
    RUN=`sudo kubectl get pods | grep Running | wc -l`

    summary
done

