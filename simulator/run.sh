#!/bin/bash

OUTPUTFILE="result.csv"
PREFIX="output"
STABILITY_TIME=30
COLLECT_TIME=30

function start
{
    echo "Starting server"
    killall locust
    locust -f locustfile.py &
    sleep 5

    curl -d user_count=100 -d hatch_rate=30 -d host=http://10.20.31.92:4570/forward http://10.20.31.26:8089/swarm
    rm -f $OUTPUTFILE
    mkdir tmp
}

function measure
{
    QTD=$1
    FILENAME="tmp/${PREFIX}_${QTD}.csv"

    echo "Running experiment for ${QTD} users"
    curl -d user_count=$QTD -d hatch_rate=30 http://10.20.31.26:8089/swarm
    sleep $STABILITY_TIME

    echo "Stability time finished, measuring"
    curl http://10.20.31.26:8089/stats/reset
    sleep $COLLECT_TIME
    wget http://10.20.31.26:8089/stats/requests/csv -O ${FILENAME}

    q -H -d ',' "select $QTD as \"Users\",\"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",0 as \"Var in Avg Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",0 as \"Var in Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from ${FILENAME} limit 1" >> $OUTPUTFILE
}

start

measure 300
measure 600
measure 900
measure 1200

