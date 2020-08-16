#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_app-csd.yaml

# Wait for all pods to start
./wait_run.sh
