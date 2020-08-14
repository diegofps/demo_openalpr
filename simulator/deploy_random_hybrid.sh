#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_openalpr_hybrid.yaml
sudo kubectl expose deployment/openalpr-hybrid --type="LoadBalancer" --port 4568

# Wait for all pods to start
./wait_run.sh
