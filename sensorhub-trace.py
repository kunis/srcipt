#!/usr/bin/python
# -*- coding: utf-8 -*-
#

'''
sensorhub_data: data_len=0
'''

import re
import sys

fileo=open(sys.argv[1])

cmd_start=float(0)
cmd_end=float(0)
data_len=int(0)
print 'start,end,time,command,data length'
for line in fileo:
    line=line.strip('\n')
    res = line.find('sensorhub_request_start')
    if(res > 0):
        cmd_start=float(re.search('[0-9]+\.[0-9]+',line).group(0))
        data_len = 0
    
    res = line.find('sensorhub_data')
    if(res > 0):
        data_str=re.search('data_len=[0-9]+',line).group(0)
        data_len=data_len + int(data_str.split('=')[1])

    res = line.find('sensorhub_request_end')
    if(res > 0):
        cmd_end=float(re.search('[0-9]+\.[0-9]+',line).group(0))
        cmd=int(line.split('=')[1])
        print str(cmd_start)+','+str(cmd_end)+','+str(cmd_end-cmd_start)+','+ str(cmd)+','+ str(data_len)

