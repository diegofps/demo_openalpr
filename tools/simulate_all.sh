#!/bin/bash

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_default.sh'
./simulate.sh result_default.csv

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_w.sh'
./simulate.sh hybrid_w.csv

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_r.sh'
./simulate.sh hybrid_r.csv

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_wob.sh'
./simulate.sh hybrid_wob.csv

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_awob.sh'
./simulate.sh hybrid_awob.csv

ssh locust@10.20.31.92 'cd /home/ngd/Sources/demo_openalpr/tools && sudo ./expose_m.sh'
./simulate.sh hybrid_m.csv

