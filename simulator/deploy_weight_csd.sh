#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_proxy-weight.yaml
sudo kubectl apply -f ../deployment_openalpr_csd.yaml
sudo kubectl expose deployment/openalpr-proxy-weight --type="LoadBalancer" --port 4570

