#!/bin/bash

sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`

sudo kubectl apply -f ../deployment_proxy-awob.yaml
sudo kubectl expose deployment/openalpr-proxy-awob --type="LoadBalancer" --port 4570

./wait_run.sh
