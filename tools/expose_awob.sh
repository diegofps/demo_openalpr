#!/bin/bash

sudo kubectl apply -f ../deployment_proxy-awob.yaml
sudo kubectl expose deployment/openalpr-proxy-awob --type="LoadBalancer" --port 4570

./wait_run.sh
