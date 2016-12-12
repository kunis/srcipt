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

output=None
kmsg_name=None
utc_flag=False

def usage():
    print "klog version 1.0"
    print "Usage: logfile kmsgfile [option]"
    print "Options:"
    print "            --help        display this help and exit"
    print "        -o, --output      output file name"
    print "        -u, --utc         convert utc date"

def parse_argument():
    global kmsg_name
    global output
    global utc_flag
   
    if(len(sys.argv) < 4):
        usage()
        sys.exit()

    opts, args = getopt.getopt(sys.argv[2:],"uo:",["utc","output=","help"])
    kmsg_name=sys.argv[1] #first argument is input log file
    
    for op,value in opts:
        if op in ["-o","--output"]:
            output=value
        elif op in ["-u","--utc"]:
            utc_flag=True
        elif op in ["--help"]:
            usage()
            sys.exit()

def main():
    try:
        fileo=open(kmsg_name)
        targeto=open(output,'w')
    except (IOError,TypeError),e:
        print 'Open File Fail:',e
        return

    base_jiffy=float(0)
    base_utc=None
    timezone=float(0)
    
    for line in fileo:
        line=line.strip()
        res=re.search(r"\[([ 0-9.]+)\]", line)

        if(res == None):
            print line
            continue
        jiffy = float(re.search(r"\[([ 0-9.]+)\]", line).group(1))

    
        m = re.match(r"(.*)\[(.*)\] timestamp: (.*?),timezone:(.*)", line)
        if m:
            base_jiffy=jiffy
            base_utc=datetime.datetime.utcfromtimestamp(float(m.group(3)))
            timezone=float(m.group(4))
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
            targeto.write('# '+str(utc)+' # '+line+'\n')
        else:
            targeto.write(line+'\n')
    fileo.close()
    targeto.close()


if __name__ == '__main__':
    try:
        parse_argument()
        main()
    except BaseException,e:
        print e


