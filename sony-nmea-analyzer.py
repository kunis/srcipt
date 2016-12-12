#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################################################################
#
# 将要分析的nmea文件存放到一个文件夹中比如: nmea-dir-name
#
# 执行以下程序
# example ./sony-nmea-analyzer.py  nmea-dir-name 
#
# 将产生的数据重定向到.csv文件中，可以用excel打开并查看
############################################################################################################

import datetime
import math
import os
import re
import sys
import time
import getopt
import glob

startTime=None
fixTime=None
bepTime=None
current_utc=''


def init_var():
    global startTime
    global fixTime
    global bepTime
    global current_utc
    startTime=None
    fixTime=None
    bepTime=None
    current_utc=''


def parse_nmea_rmc(rmc_str):

    strarr=rmc_str.split(',')
    global fixTime
    global startTime
    global current_utc

    hour=strarr[1][0:2]
    m=strarr[1][2:4]
    s=strarr[1][4:6]
    year=2000 + int(strarr[9][4:6])
    mon=strarr[9][2:4]
    day=strarr[9][0:2]


    if(strarr[2] == 'A'):
        try:
            current_utc=str(year)+'-'+mon+'-'+day+' '+hour+':'+m+':'+s
            if fixTime == None:
                fixTime=str(year)+'-'+mon+'-'+day+' '+hour+':'+m+':'+s
        except ValueError:
            print 'nmea parse failed'
    else:

        if startTime == None:
            startTime =str(year)+'-'+mon+'-'+day+' '+hour+':'+m+':'+s


def get_delta_time(start,end):
    utc = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    starttimestamp=time.mktime(utc.timetuple())
    utc = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    endtimestamp=time.mktime(utc.timetuple())
    return endtimestamp-starttimestamp


def parse_nmea(filename):
    global bepTime
    global current_utc
    init_var()
    fileo=open(filename)

    for line in fileo:
        line=line.strip('\n')
        line=line.strip('\r')
        line=line.replace(' ','')

        res=line.find('GPRMC')
        if(res > 0):
            parse_nmea_rmc(line)

        res=line.find('GNRMC')
        if(res > 0):
            parse_nmea_rmc(line)

        res=line.find('PSGSA')
        if(res > 0):
            strarr=line.split(',')
            if strarr[19] == 'A':
                if bepTime == None:
                    bepTime = current_utc
                    print filename+','+str(get_delta_time(startTime,fixTime))+','+str(get_delta_time(fixTime,bepTime))
    fileo.close()



def main():
    print 'File Name,TTFF,CEP Time'
    for root, dirs, files in os.walk(sys.argv[1]):
        for fn in files:
            filename=os.path.join(root, fn)
            if filename.endswith('.txt'):
                parse_nmea(filename)
            if filename.endswith('.nmea'):
                parse_nmea(filename)


if __name__ == '__main__':
    main()
