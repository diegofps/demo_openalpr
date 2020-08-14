#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_proxy-weight-on-busy.yaml
sudo kubectl apply -f ../deployment_openalpr_perl.yaml
sudo kubectl expose deployment/openalpr-proxy-weight --type="LoadBalancer" --port 4570

# Wait for all pods to start
./wait_run.sh
