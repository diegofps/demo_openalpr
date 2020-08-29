#!/bin/bash

# Undeploy any previous proxy
./undeploy_proxy.sh

# Create and expose the proxy
sudo kubectl apply -f deployment/svc-openalpr.yaml

./wait_run.sh

SVC_NAME=$(ssh locust@$TARGET "sudo kubectl get services | grep openalpr- | awk '{print \$1}'")
NODE_PORT=$(ssh locust@$TARGET "sudo kubectl get services/$SVC_NAME -o go-template='{{(index .spec.ports 0).nodePort}}'")
echo "default proxy, got svc=$SVC_NAME and port=$NODE_PORT"
