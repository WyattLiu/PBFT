import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import re
from collections import defaultdict
import statistics

from latency_analyzer import *

def plot(op, list_of_num):
    data_size=len(list_of_num)
    data_set=sorted(set(list_of_num))
    bins=np.append(data_set, data_set[-1]+1)
    counts, bin_edges = np.histogram(list_of_num, bins=bins, density=False)
    counts=counts.astype(float)/data_size
    cdf = np.cumsum(counts)
    ax1.plot(bin_edges[0:-1], cdf,linestyle='--', label = op)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError('wrong arg')
    with open(sys.argv[1]) as file:
        lines = file.readlines()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    for line in lines:
        cols = line.split()
        print("lt file: " + cols[0] + " label: " + cols[1])
        plot(cols[1], latency_analyzer(cols[0]).get_all_lt())
    plt.xlabel("Latency (ms)")
    plt.ylabel("CDF")
    plt.grid(True)
    plt.xscale('log')
    plt.ylim((0,1))
    plt.legend(loc='best');
    plt.savefig("./cdf.png", dpi = 300)

