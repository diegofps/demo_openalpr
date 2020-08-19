#!/bin/bash

OUTPUTFILE="$1"
PREFIX="output"
LOCUST_SERVER="http://10.20.31.30:8089"
STABILITY_TIME=30
COLLECT_TIME=600
HOST="http://10.20.31.92:4570/forward"
#HOST="http://10.20.31.92:31397"

if [ -z $OUTPUTFILE ]
then
    OUTPUTFILE="result.csv"
fi

function start
{
    echo "Starting server"
    killall locust
    locust -f locustfile.py &
    sleep 5

    curl -d user_count=100 -d hatch_rate=30 -d host=$HOST ${LOCUST_SERVER}/swarm
    rm -f $OUTPUTFILE
    mkdir tmp
}

function measure
{
    QTD=$1
    FILENAME="tmp/${PREFIX}_${QTD}.csv"

    echo "Running experiment for ${QTD} users"
    curl -d user_count=$QTD -d hatch_rate=30 ${LOCUST_SERVER}/swarm
    sleep $STABILITY_TIME

    echo "Stability time finished, measuring"
    curl ${LOCUST_SERVER}/stats/reset
    sleep $COLLECT_TIME
    wget ${LOCUST_SERVER}/stats/requests/csv -O ${FILENAME}

    q -H -d ',' "select $QTD as \"Users\",\"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",0 as \"Var in Avg Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",0 as \"Var in Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from ${FILENAME} limit 1" >> $OUTPUTFILE
}

function terminate
{
    killall locust
}

start

measure 300
measure 600
measure 900
measure 1200

terminate

echo "Experiment completed"
sleep 2
