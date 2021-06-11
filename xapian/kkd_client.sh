#!/bin/bash
server_ip=10.150.21.207
server_port=8080
qps=$1 # load of client. determine total execution time: (total_qps of server)/(qps).
LATS_DIR=/home/caslab/tailbench-v0.9_modify/xapian
client_threads=10 # the number of client threads. 1 thread creates two processes(threads).


TBENCH_RANDSEED=10000 \
    TBENCH_SERVER=$server_ip \
    TBENCH_SERVER_PORT=$server_port \
    TBENCH_QPS=$qps \
    TBENCH_CLIENT_THREADS=$client_threads \
    TBENCH_MINSLEEPNS=100000 \
    TBENCH_TERMS_FILE=/home/caslab/tailbench.inputs/xapian/terms.in \
    SLEEP_NS=$((2000 * 1000 * 1000)) \
    BURST_NS=$((2000 * 1000 * 1000))\
    chrt -r 99 /home/caslab/tailbench-v0.9_modify/xapian/xapian_networked_client


/home/caslab/tailbench-v0.9_modify/utilities/parselats.py $LATS_DIR/lats.bin
