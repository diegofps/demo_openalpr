#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f ./deployment/proxy-m.yaml
sudo kubectl expose deployment/openalpr-proxy-m --type="LoadBalancer" --port 4570

./wait_run.sh
