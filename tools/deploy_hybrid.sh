#!/bin/bash

# Undeploy any previous cluster app
./undeploy_app.sh

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ./deployment/app-csd.yaml
sudo kubectl apply -f ./deployment/app-perl.yaml

# Wait for all pods to start
./wait_run.sh
