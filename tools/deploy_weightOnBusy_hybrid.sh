#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_proxy-weight-on-busy.yaml
sudo kubectl apply -f ../deployment_openalpr_hybrid.yaml
sudo kubectl expose deployment/openalpr-proxy-weight-on-busy --type="LoadBalancer" --port 4570

# Wait for all pods to start
./wait_run.sh
