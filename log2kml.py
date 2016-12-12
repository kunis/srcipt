#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################################################################
#
# example ./log2kml.py -h formatted-sensorhub-log.txt  -s hm_sensor_hub_service@2016-04-25-12-25-33-479.txt 
#
############################################################################################################

import sqlite3
import simplekml
import zipfile
import math
import os
import re
import sys
import time
import getopt


def usage():
    print "log2kml version 2.0"
    print "Usage: log2kml [option]"
    print "            --help        display this help and exit"
    print "        -h, --hub         sensorhub log file"
    print "        -s, --service     android sensorhub servce dumpsys log"
    print "        -d, --database    sport database file"

def convert_from_hhmm(value):
    val=value;
    degrees=int(math.floor(val)/100)
    minutes=val-float(degrees)*float(100)
    dcoord=float(degrees) + minutes/60.0
    return dcoord

def get_log_filename():
    opts, args = getopt.getopt(sys.argv[1:],"h:s:d:",["hub=","service=","database=","help"])
    sensorhub_log=''
    sensorhub_service_log=''
    databse_file=''
    for op,value in opts:
        if op in ["-h","--hub"]:
            sensorhub_log=value
        elif op in ["-s","--service"]:
            sensorhub_service_log=value
        elif op in ["-d","--database"]:
            databse_file=value
        elif op in ["--help"]:
            usage()
            sys.exit()
    return [sensorhub_log,sensorhub_service_log,databse_file]
def parse_nmea_rmc(fol,rmc_str,ptname,lineno):
    strarr=rmc_str.split(',')
    gps_coord=[]
    if(strarr[2] == 'A'):
        try:
            latitude=float(strarr[3])
            longitude=float(strarr[5])
            if(strarr[6] == 'W'):
                longitude=-longitude
            hour=strarr[1][0:2]
            m=strarr[1][2:4]
            s=strarr[1][4:6]
            year=2000 + int(strarr[9][4:6])
            mon=strarr[9][2:4]
            day=strarr[9][0:2]
           

            latitude=convert_from_hhmm(latitude)
            longitude=convert_from_hhmm(longitude)
            gps_coord=[(float(longitude),float(latitude))]
            pt=fol.newpoint(name=ptname,coords=[(float(longitude), float(latitude))])
            pt.description=str(longitude)+'<br>'+str(latitude)+'<br>lineno.:'+str(lineno)
            pt.description=pt.description+'<br>'+str(year)+'-'+mon+'-'+day+' '+hour+':'+m+':'+s
            pt.placemark.styleurl='#'+fol.style.id
        except ValueError:
            print 'nmea parse failed,line:',lineno

    return gps_coord
def parse_algo_info(fol,info,ptname,lineno):

    info=info.replace(':',',')
    strarr=info.split(',')
    gps_coord=[]
    if(len(strarr) < 7):
        return gps_coord
    try:
        timestamp=strarr[1]
        if(False == timestamp.isdigit()):
            return gps_coord
        latitude=strarr[2]
        longitude=strarr[3]
        speed=strarr[4]
        stepinfo=int('0x'+strarr[5],16)
        pttype=int(0)
        pttype=int('0x'+strarr[7],16)
        gps_coord=[(float(longitude),float(latitude))]
        pt=fol.newpoint(name=ptname,coords=[(float(longitude), float(latitude))])

        try:
            speed_val=float(speed)
        except ValueError:
            print 'speed value error'
            speed=''
        pt.description='Timestamp: '+timestamp+'ms'+'<br>'+'Speed: '+ speed
        if(pttype&(1<<14)):
            pt.description=pt.description+'<br>Type: '+'AGPS'
            pt.description=pt.description +'<br>un-sumed step count: '+str((stepinfo>>4))
            pt.description=pt.description +'<br>gSecNewStep: '+str(stepinfo&0xf)
            pt.description=pt.description +'<br>lineno.: '+str(lineno)


    except ValueError:
        print strarr
        print '[Invalid coordinates]: ',lineno

    return gps_coord


def parse_hub_log(filename):

    fileo=open(filename)

    i=0
    nmeaindex=0
    lineno=0
    kml = simplekml.Kml()
    nmeakml = simplekml.Kml()

    fol = kml.newfolder(name='Points')
    nmeafol = nmeakml.newfolder(name='Points')
    nmeafol.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    nmeafol.style.iconstyle.color=simplekml.Color.rgb(0xff,0x00,0x00)
    algo_coords=[]
    nmea_coords=[]
    for line in fileo:
        line=line.strip('\n')
        line=line.strip('\r')
        line=line.replace(' ','')
        res=line.find('outdis')
        lineno=lineno+1;
        if(res >= 0):
            coord=parse_algo_info(fol,line[res:],str(i),lineno)
            algo_coords=algo_coords+coord
            i=i+1
            
        res=line.find('GNRMC')
        if(res > 0):
            coord=parse_nmea_rmc(nmeafol,line,str(nmeaindex),lineno)
            nmea_coords=nmea_coords+coord
            nmeaindex=nmeaindex+1

        res=line.find('GPRMC')
        if(res > 0):
            coord=parse_nmea_rmc(nmeafol,line,str(nmeaindex),lineno)
            nmea_coords=nmea_coords+coord
            nmeaindex=nmeaindex+1

    try:
        lin=kml.newlinestring(name=('Track'),coords=algo_coords)
        lin.style.linestyle.color=simplekml.Color.rgb(0x00,0xff,0x00)
        lin.style.linestyle.width=6
    except ValueError:
        print '[Invalid coordinates]: ',lineno
    try:
        nmealin=nmeakml.newlinestring(name=('Track'),coords=nmea_coords)
        nmealin.style.linestyle.color=simplekml.Color.rgb(0x00,0xff,0x00)
        nmealin.style.linestyle.width=6
    except ValueError:
        print '[Invalid coordinates]: ',lineno


    kml.save('gps-raw.kml')
    nmeakml.save('nmea.kml')
    fileo.close()


def parse_service_log(filename):
    fileo=open(filename)
    SportStart=False
    gps_coords=[]
    coords_dict=dict()
    startTime=''
    stopTime=''
    kml=None
    for line in fileo:
        line=line.strip('\n')
        res=line.find('Gps History data')
        if(res > 0):
            startTime='0'
            kml=simplekml.Kml()
            fol = kml.newfolder(name='Points')
            SportStart=True
            i=0
            gps_coords=[]
            continue

        res=line.find('<----Start Sport')
        if(res > 0):
            startTime=line.replace('-','').replace('<','').replace('>','')
            kml=simplekml.Kml()
            fol = kml.newfolder(name='Points')
            fol.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/wht-blank.png'
            SportStart=True
            i=0
            gps_coords=[]
            coords_dict.clear()
            continue

        res=line.find('<----Stop Sport')
        if(res > 0):
            stopTime=line.replace('-','').replace('<','').replace('>','')
            SportStart=False
            try:

                tmp = sorted(coords_dict.iteritems(), key = lambda asd:asd[0],reverse=False)
                for item in tmp:
                    pt=fol.newpoint(name=('%d' %i),
                            coords=[item[1]])
                    pt.placemark.styleurl='#'+fol.style.id
                    pt.description="Timestamp:"+str(item[0])+'ms'
                    gps_coords=gps_coords+[item[1]]
                    i=i+1
                lin=kml.newlinestring(name=('Track'),coords=gps_coords)
                lin.style.linestyle.color=simplekml.Color.rgb(0xff,0x00,0x00)
                lin.style.linestyle.width=6
                lin.description=startTime+'<br>'+stopTime


            except ValueError:
                print('[Invalid coordinates]')

            line=line.replace(' ','').replace('>','').replace('<','').replace('-','').replace('.','-').replace(':','-')
            kml.save(line+'.kml')
            i=0
            continue

        res=line.find('<----Pause Sport ')
        if(res > 0):
            continue

        res=line.find('<----Restart Sport ')
        if(res > 0):
            continue


        res=line.find('Get Location Called')

        if(res < 0):
            if(SportStart):
                line=line.replace(' ','')
                tmps=line.split(':')
                if(len(tmps) == 2):
                    line=tmps[1]
                
                strarr=line.split(',')
                if(len(strarr) < 2):
                    continue
                    
                longitude=strarr[0]
                latitude=strarr[1]

                if coords_dict.has_key(int(strarr[3])) == True:
                    del coords_dict[int(strarr[3])]
                coords_dict[int(strarr[3])]=(float(longitude),float(latitude))


def get_all_point(conn,track_id):
    
    sqlcmd='SELECT track_id , latitude, longitude, timestamp,altitude,accuracy,speed,point_type from location_data where track_id='+str(track_id)
    cursor = conn.execute(sqlcmd)
    gps_coords=[]

    i=0
    kml = simplekml.Kml()
    fol = kml.newfolder(name='Points')
    for row in cursor:
        pt=fol.newpoint(name=('%d' %i), coords=[(float(row[2]), float(row[1]))])
        pt.description="Timestamp:"+str(row[3])+'ms'
        gps_coords=gps_coords+[(row[2],row[1])]
        i=i+1

    if(len(gps_coords) <= 0):
        return
    
    try:
        lin=kml.newlinestring(name=('Track'),coords=gps_coords)
        lin.style.linestyle.color=simplekml.Color.rgb(0x00,0xff,0x00)
        lin.style.linestyle.width=6
    except ValueError:
        print('[Invalid coordinates]')

    kml.save(str(track_id)+'.kml')

def parse_database(filename):

    conn = sqlite3.connect(filename)
    all_track_id=conn.execute("select track_id from sport_summary")
    for id in all_track_id:
        get_all_point(conn,id[0])

    conn.close()

def main():
    files=get_log_filename()
    if(files[0]):
        parse_hub_log(files[0])
    if(files[1]):
        parse_service_log(files[1])

    if(files[2]):
        parse_database(files[2])


if __name__ == '__main__':
    main()
