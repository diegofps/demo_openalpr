#!/bin/bash

# Delete all services and deployments
sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`
sudo kubectl delete deployment `sudo kubectl get deployments | awk '{if(NR>1) print $1}'`

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_proxy-weight-on-busy.yaml
sudo kubectl apply -f ../deployment_openalpr_perl.yaml
sudo kubectl expose deployment/openalpr-proxy-weight --type="LoadBalancer" --port 4570

