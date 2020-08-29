#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f deployment/svc-openalpr.yaml

./wait_run.sh
