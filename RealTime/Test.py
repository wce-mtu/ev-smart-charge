import numpy as np
import random
import scipy.stats as stats
import matplotlib.pyplot as plt, test
import matplotlib.animation as animation
import matplotlib.dates as dates
import os
from matplotlib import style
from datetime import datetime
import matplotlib.lines as mlines
from time import *
from socket import *
from sys import *
from Vehicle import *
from Station import *
f = open("/home/jason/Documents/TestScript.txt", "r")
random.seed()
for line in f:
    print(line)