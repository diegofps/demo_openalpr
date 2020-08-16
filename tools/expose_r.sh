#!/bin/bash

sudo kubectl apply -f ../deployment_proxy-r.yaml
sudo kubectl expose deployment/openalpr-proxy-w --type="LoadBalancer" --port 4570

./wait_run.sh
