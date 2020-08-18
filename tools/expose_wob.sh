#!/bin/bash

sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`

sudo kubectl apply -f ../deployment_proxy-wob.yaml
sudo kubectl expose deployment/openalpr-proxy-wob --type="LoadBalancer" --port 4570

./wait_run.sh
