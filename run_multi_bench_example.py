#!/usr/bin/python3

from multibench import *

# Insturction:
# 1. Make a copy of this file and rename to run_multi_bench.py
# 2. Change SERVER_LIST to remote servers with RAC server
# 3. see jsons below to define a workload

SERVER_LIST = ["192.168.44.237:3002"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
            raise ValueError('wrong arg')
    
    client = sys.argv[1]

    test = {
        "nodes_pre_server": 1,
        "use_server": 1,
        "client_multiplier": int(client),

        "typecode": "pnc",
        "total_objects": 1000,

        "prep_ops_pre_obj": 10,
        "num_reverse": [0],
        "prep_ratio": [1, 0, 0],


        "ops_per_object": 100,
        "op_ratio": [[0.15, 0.15, 0.7]],
        "target_throughput": 0
    }


    run_experiment(test, "num_reverse", "op_ratio", "single_pbft_test_result_file_" + client, SERVER_LIST, True)
