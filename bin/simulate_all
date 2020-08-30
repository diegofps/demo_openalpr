#!/bin/bash

TARGET=$1
REST_TIME=60

if [ -z $TARGET ]
then
    TARGET="10.20.31.92"
fi

function run
{
    CLUSTER=$1
    PROXY=$2
    
    ssh locust@$TARGET "cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_${PROXY}.sh"

    if [ ${PROXY} == "default" ]
    then
        SVC_NAME=$(ssh locust@$TARGET "sudo kubectl get services | grep openalpr- | awk '{print \$1}'")
        NODE_PORT=$(ssh locust@$TARGET "sudo kubectl get services/$SVC_NAME -o go-template='{{(index .spec.ports 0).nodePort}}'")
        echo "default proxy, got svc=$SVC_NAME and port=$NODE_PORT"

        ./simulate.sh "${CLUSTER}_${PROXY}" "http://$TARGET:$NODE_PORT"
    else
        echo "Not a default proxy"
        ./simulate.sh "${CLUSTER}_${PROXY}" "http://$TARGET:4570/forward"
    fi

    sleep $REST_TIME
}

run "hybrid" "default"
run "hybrid" "aw"
run "hybrid" "w"
run "hybrid" "r"
run "hybrid" "wob"
run "hybrid" "awob"
run "hybrid" "m"

