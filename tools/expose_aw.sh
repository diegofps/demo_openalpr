#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f ./deployment/proxy-aw.yaml
sudo kubectl expose deployment/openalpr-proxy-aw --type="LoadBalancer" --port 4570

./wait_run.sh
