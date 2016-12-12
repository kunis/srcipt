#!/usr/bin/env python


import re
import numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

from matplotlib import mlab
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.dates import DayLocator
from matplotlib.dates import MinuteLocator
from matplotlib.dates import HourLocator
from matplotlib.dates import DateFormatter
import matplotlib as mpl 
import datetime
import numpy.ma as ma
import copy
import matplotlib.lines as lines
import time
import matplotlib.dates as dates
import sys
from matplotlib.ticker import FuncFormatter, MaxNLocator



def batt_display():
    data=mlab.csv2rec(sys.argv[1],delimiter='\t')

    print data
    x=data['time']
    y = data['value']
    plt.plot(x,y);

    plt.grid(True)
    plt.show()


   


if __name__ == '__main__':
    try:
        batt_display()
    except BaseException,e:
        print e


