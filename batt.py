#!/usr/bin/python
# -*- coding: utf-8 -*-
#python version v2.7
###########################################################################################################
#
# example:
#         ./klog.py kmsg.txt -u -o kmsg-utc.txt
#         ./klog.py kmsg.txt -o kmsg-local-time.txt 
#
############################################################################################################


import datetime
import getopt
import re
import sys
utc_flag=False
def main():
    try:
        fileo=open(sys.argv[1])
    except (IOError,TypeError),e:
        print 'Open File Fail:',e
        return
   
    base_jiffy=float(0)
    base_utc=None
    timezone=float(0)

    print 'batt,date'
    for line in fileo:
        line=line.strip()
        jiffy = float(re.search(r"\[([ 0-9.]+)\]", line).group(1))
       
        m = re.match(r"(.*)\[(.*)\] timestamp: (.*?),timezone:(.*)", line)
        if m:
            base_jiffy=jiffy
            base_utc=datetime.datetime.utcfromtimestamp(float(m.group(3)))
            timezone=float(m.group(4))
       
        m=re.match(r"(.*)\[(.*)\] Total suspend: ([0-9]+)days ([0-9]+)hours ([0-9]+)mintues ([0-9]+)seconds",line)
        if m:
            day=int(m.group(3))
            hours=int(m.group(4))
            mintues=int(m.group(5))
            seconds=int(m.group(6))
            base_utc+=datetime.timedelta(days=day,hours=hours,minutes=mintues,seconds=seconds)
            base_jiffy=jiffy
        
        m = re.match(r"(.*)\[(.*)\] PM: suspend ([a-z]+) (.*?) UTC", line)
        if m:
            if "exit" in m.group(3):
                jiffy = float(m.group(2))
                utc = m.group(4)
                utc = utc[:-3]
                utc = datetime.datetime.strptime(utc, "%Y-%m-%d %H:%M:%S.%f")
                base_utc = utc
                base_jiffy=jiffy

        if(True == utc_flag):
            timezone=0

        if base_utc != None:
            utc=base_utc+datetime.timedelta(seconds=(float(jiffy)-float(base_jiffy)-timezone*60))
            m = re.match(r"(.*)\[(.*)\] healthd: battery l=(.*?) v=(.*?) (.*?)", line)
            if m:
                print m.group(3)+','+str(utc)
    
    fileo.close()


if __name__ == '__main__':
    try:
        main()
    except BaseException,e:
        print e


