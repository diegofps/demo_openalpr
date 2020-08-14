#!/bin/bash

# Delete all services and deployments
sudo kubectl delete service `sudo kubectl get services | awk '{if(NR>1) print $1}' | grep -v kubernetes`
sudo kubectl delete deployment `sudo kubectl get deployments | awk '{if(NR>1) print $1}'`
