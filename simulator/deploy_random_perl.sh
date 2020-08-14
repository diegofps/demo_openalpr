#!/bin/bash

# Create the desired proxy, cluster mode and expose it 
sudo kubectl apply -f ../deployment_openalpr_perl.yaml
sudo kubectl expose deployment/openalpr-perl --type="LoadBalancer" --port 4568

