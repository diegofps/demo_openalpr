#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f ./deployment/proxy-awob.yaml
sudo kubectl apply -f deployment/svc-proxy.yaml

./wait_run.sh
