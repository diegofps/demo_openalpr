#!/bin/bash

sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`

NAME=`sudo kubectl get deployments | grep -e 'openalpr-[a-z]*\s' | awk '{ print $1}'`
sudo kubectl expose deployment/$NAME --type="LoadBalancer" --port 4568

./wait_run.sh
