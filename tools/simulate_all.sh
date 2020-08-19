#!/bin/bash

function run
{
    NAME=$1
    ssh locust@10.20.31.92 "cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_${NAME}.sh"
    ./simulate.sh ${NAME}
}

run "hybrid_default"
run "hybrid_w"
run "hybrid_r"
run "hybrid_wob"
run "hybrid_awob"
run "hybrid_m"
