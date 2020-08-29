#!/bin/bash

echo -e "\n---Deployments---"
sudo kubectl get deployments -o wide

echo -e "\n---Services---"
sudo kubectl get services -o wide

echo -e "\n---Nodes---"
sudo kubectl get nodes -o wide

echo -e "\n---Nodes SSH---"
parallel-ssh -h ~/nodes -i -t 0 "echo alive"
