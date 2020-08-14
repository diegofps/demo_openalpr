#!/bin/bash

TE=`sudo kubectl get pods | grep Terminating | wc -l`

while [ $TE != '0' ]
do
    echo "Pods still Terminating: $TE"
    sleep 1
    TE=`sudo kubectl get pods | grep Terminating | wc -l`
done

