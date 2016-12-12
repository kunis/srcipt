
suspend_entry=0
suspend_exit=0
wakeup_source=""
if [ -z $1 ] ;then

        echo "no kernel file" >&2;
        exit 0
fi
echo -n -e "Suspend Entry Timestamp,Suspend Exit Timestamp,Wakeup Reason,"
echo -n -e "Suspend Entry Date,Suspend Exit Date\n"

#echo -n -e "Suspend Entry Date,Suspend Exit Date,Light Time,level\n"

while read line
do

        res=`echo $line|grep -E "PM: suspend entry "`
        if [ ! -z "$res" ] ; then
                utc=${res#*PM: suspend entry }
                suspend_entry=`date +%s -d "$utc"`
                wakeup_source=""
                continue
        fi
 
        res=`echo $line|grep "healthd"`
        if [ ! -z "$res" ] ; then

                power_state=`echo $line|grep "healthd"|grep -Eo "chg=(.*)"|awk -F '=' '{print $2}'`
                
                if [ "$power_state" = "u" ] ; then
                        echo "usb plugin"
                else
                        echo "usb plugout"
                fi
                continue
        fi
        
        res=`echo $line|grep -E "WAKE UP:"`
        if [ ! -z "$res" ] ; then
              
                wakeup_source=$wakeup_source" "${res#*WAKE UP:}
                continue
        fi
        
        res=`echo $line|grep -E "sensorhub wakeup reason:"`
        if [ ! -z "$res" ] ; then
              
                wakeup_source=$wakeup_source" ""HUB:"${res#*sensorhub wakeup reason:}
                continue
        fi


        res=`echo $line|grep -E "slpt_backlight"`
        if [ ! -z "$res" ] ; then

                bl_time=`echo $line|grep -Eo 'bl_time=[0-9]+'|awk -F '=' '{print $2}'`
                bl_level=`echo $line|grep -Eo 'bl_level=[0-9]+'|awk -F '=' '{print $2}'`
                #echo -n -e "$entry_date,$exit_date,$bl_time,$bl_level\n"
                continue

        fi
        
        res=`echo $line|grep -E "PM: suspend exit "`
        if [ ! -z "$res" ] ; then
                utc=${res#*PM: suspend exit }
                suspend_exit=`date +%s -d "$utc"`
                entry_date=`date -d @$suspend_entry  "+%Y-%m-%d %T"`
                exit_date=`date -d @$suspend_exit  "+%Y-%m-%d %T"`
                echo -n -e $suspend_entry","$suspend_exit","$wakeup_source","$entry_date","$exit_date"\n"
                continue
        fi


done < $1


