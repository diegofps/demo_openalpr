#!/bin/sh


PREFIX="output"
STABILIZE_TIME=60
COLLECT_TIME=180

echo "Starting server"
locust -f locustfile.py &
sleep 5

################################################################################

echo "Running experiment for 300 users"
curl -d user_count=300 -d hatch_rate=30 -d host=http://10.20.31.92:4570/forward http://10.20.31.26:8089/swarm
sleep $STABILIZE_TIME

echo "Stability time finished, measuring"
curl http://10.20.31.26:8089/stats/reset
sleep $COLLECT_TIME
wget http://10.20.31.26:8089/stats/requests/csv -O $PREFIX_300.csv

################################################################################

echo "Running experiment for 600 users"
curl -d user_count=600 -d hatch_rate=30 http://10.20.31.26:8089/swarm
sleep $STABILIZE_TIME

echo "Stability time finished, measuring"
curl http://10.20.31.26:8089/stats/reset
sleep $COLLECT_TIME
wget http://10.20.31.26:8089/stats/requests/csv -O $PREFIX_600.csv

################################################################################

echo "Running experiment for 900 users"
curl -d user_count=900 -d hatch_rate=30 http://10.20.31.26:8089/swarm
sleep $STABILIZE_TIME

echo "Stability time finished, measuring"
curl http://10.20.31.26:8089/stats/reset
sleep $COLLECT_TIME
wget http://10.20.31.26:8089/stats/requests/csv -O $PREFIX_900.csv

################################################################################

echo "Running experiment for 1200 users"
curl -d user_count=1200 -d hatch_rate=30 http://10.20.31.26:8089/swarm
sleep $STABILIZE_TIME

echo "Stability time finished, measuring"
curl http://10.20.31.26:8089/stats/reset
sleep $COLLECT_TIME
wget http://10.20.31.26:8089/stats/requests/csv -O $PREFIX_1200.csv

################################################################################

echo "" > results.csv

q -H -d ',' "select \"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from $PREFIX_300.csv limit 1" -O >> results.csv

q -H -d ',' "select \"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from $PREFIX_600.csv limit 1" >> results.csv

q -H -d ',' "select \"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from $PREFIX_900.csv limit 1" >> results.csv

q -H -d ',' "select \"Request Count\",\"Failure Count\",\"Median Response Time\",\"Average Response Time\",\"Min Response Time\",\"Max Response Time\",\"Average Content Size\",\"Requests/s\",\"Failures/s\",\"50%\",\"66%\",\"75%\",\"80%\",\"90%\",\"95%\",\"98%\",\"99%\",\"99.9%\",\"99.99%\",\"99.999%\",\"100%\" from $PREFIX_1200.csv limit 1" >> results.csv

