#!/bin/bash

TE=`sudo kubectl get pods | grep Terminating | wc -l`

while [ $CC != '0' -o $PE != '0' ]
do
    echo "Pods still Terminating: $TE"
    sleep 1
    TE=`sudo kubectl get pods | grep Terminating | wc -l`
done

