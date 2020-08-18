#!/bin/bash

sudo kubectl apply -f ../deployment_proxy-m.yaml
sudo kubectl expose deployment/openalpr-proxy-m --type="LoadBalancer" --port 4570

./wait_run.sh
