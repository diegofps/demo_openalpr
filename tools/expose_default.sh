#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
NAME=`sudo kubectl get deployments | grep -e 'openalpr-[a-z]*\s' | awk '{ print $1}'`
sudo kubectl expose deployment/$NAME --type="LoadBalancer" --port 4568

./wait_run.sh
