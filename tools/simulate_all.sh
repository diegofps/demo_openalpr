#!/bin/bash

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_default.sh
./simulate.sh result_default.csv

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_w.sh
./simulate.sh hybrid_w.csv

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_r.sh
./simulate.sh hybrid_r.csv

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_wob.sh
./simulate.sh hybrid_wob.csv

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_awob.sh
./simulate.sh hybrid_awob.csv

ssh locust@10.20.31.92 sudo /home/ngd/Sources/demo_openalpr/tools/expose_m.sh
./simulate.sh hybrid_m.csv

