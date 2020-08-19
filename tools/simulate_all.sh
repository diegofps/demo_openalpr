#!/bin/bash

./expose_default.sh
./simulate.sh result_default.csv

./expose_w.sh
./simulate.sh hybrid_w.csv

./expose_r.sh
./simulate.sh hybrid_r.csv

./expose_wob.sh
./simulate.sh hybrid_wob.csv

./expose_awob.sh
./simulate.sh hybrid_awob.csv

./expose_m.sh
./simulate.sh hybrid_m.csv

