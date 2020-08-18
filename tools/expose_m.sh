#!/bin/bash

sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`
sudo kubectl delete deployment `sudo kubectl get deployment | awk '{if(NR>1) print $1}' | grep openalpr-proxy`

sudo kubectl apply -f ../deployment_proxy-m.yaml
sudo kubectl expose deployment/openalpr-proxy-m --type="LoadBalancer" --port 4570

./wait_run.sh
