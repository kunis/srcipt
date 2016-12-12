#!/usr/bin/python


from subprocess import *


p=Popen(['adb','shell','cat','/dev/kmsg'],bufsize=1024,stdin=PIPE,stdout=PIPE,close_fds=True)
fout=p.stdout
while(True):
    line=fout.readline()
    retcode=p.poll()
    if retcode != None:
        exit(0)
    if len(line) == 0:
        continue
    strarr=line.split(';')
    if(len(strarr) >= 2):
        [loginfo,logstr]=strarr
        [loglevel,lineno,timestamp,remaind]=loginfo.split(',')
        tm = float(timestamp)/1000/1000

        print '<'+loglevel+'>'+'['+str(tm)+'] '+logstr,
    else:
        print line,
