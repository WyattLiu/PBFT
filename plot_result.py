import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import re
from collections import defaultdict
import statistics

from latency_analyzer import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError('wrong arg')
    print(str(latency_analyzer(sys.argv[1]).get_res()))
