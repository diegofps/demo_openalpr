#!/bin/bash

sudo kubectl delete deploy `sudo kubectl get deploy | awk '{if(NR>1) print $1}' | grep -v openalpr-proxy`

./wait_term.sh
