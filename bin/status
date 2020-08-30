#!/bin/bash


echo -e "\n---Deployments---"
sudo kubectl get deployments -o wide

echo -e "\n---Services---"
sudo kubectl get services -o wide

echo -e "\n---Nodes---"
sudo kubectl get nodes -o wide

echo -e "\n---Nodes SSH---"
parallel-ssh -h ~/nodes -i -t 0 "echo alive"

echo -e "\n---Pods---"
PODS=`sudo kubectl get pods`

CC=`echo "$PODS" | grep Pending | wc -l`
PE=`echo "$PODS" | grep ContainerCreating | wc -l`
EIP=`echo "$PODS" | grep ErrImagePull | wc -l`
IPBF=`echo "$PODS" | grep ImagePullBackOff | wc -l`
CLBO=`echo "$PODS" | grep CrashLoopBackOff | wc -l`
ERR=`echo "$PODS" | grep Error | wc -l`
RUN=`echo "$PODS" | grep Running | wc -l`
TE=`echo "$PODS" | grep Terminating | wc -l`

echo "Pending: $CC"
echo "ContainerCreating: $PE"
echo "ErrImagePull: $EIP"
echo "ImagePullBackOff: $IPBF"
echo "CrashLoopBackOff: $CLBO"
echo "Error: $ERR"
echo "Running: $RUN"
echo "Terminating: $TE"

echo -e "\n---GIT---"
git status
