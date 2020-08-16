#!/bin/bash

sudo kubectl apply -f ../deployment_proxy-wob.yaml
sudo kubectl expose deployment/openalpr-proxy-wob --type="LoadBalancer" --port 4570

./wait_run.sh
