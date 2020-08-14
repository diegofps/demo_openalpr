#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_openalpr_csd.yaml
sudo kubectl expose deployment/openalpr-csd --type="LoadBalancer" --port 4568

# Wait for all pods to start
./wait_run.sh
