#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f ./deployment/proxy-w.yaml
sudo kubectl expose deployment/openalpr-proxy-w --type="LoadBalancer" --port 4570

./wait_run.sh
