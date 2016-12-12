vdop=''
accuary=''
isfix=''
pdop='' 
fixtype=''
gngsa=''
used_data=''
utc_date=''
if [ -z $1 ] ;then

        echo "no kernel file" >&2;
        exit 0
fi

#echo -n -e "Suspend Entry Date,Suspend Exit Date,Light Time,level\n"

function handle_sony_nmea()
{

        used_data=`echo $1|awk -F ',' '{print $20}'`
        used_data=`echo $used_data|awk -F '*' '{print $1}'`

        if [ "$isfix" = "A" ] ;then

                echo $utc_date,$accuary,$vdop,$pdop,$fixtype,$used_data
        else
                echo $utc_date
        fi


}

while read line
do


        res=`echo $line|grep -E "GGA"`
        if [ ! -z "$res" ] ; then

                accuary=`echo $line|awk -F ',' '{print $10}'`

                utc_date=`echo $line|awk -F ',' '{print $2}' `
                continue
        fi
        res=`echo $line|grep -E "GPGSA"`
        if [ ! -z "$res" ] ; then

                gngsa=$line
                vdop=`echo $line|awk -F ',' '{print $18}'|awk -F '*' '{print $1}'`
                pdop=`echo $line|awk -F ',' '{print $16}'`
                fixtype=`echo $line|awk -F ',' '{print $3}'`
                continue
        fi

        res=`echo $line|grep -E "GNGSA"`
        if [ ! -z "$res" ] ; then

                gngsa=$line
                vdop=`echo $line|awk -F ',' '{print $18}'|awk -F '*' '{print $1}'`
                pdop=`echo $line|awk -F ',' '{print $16}'`
                fixtype=`echo $line|awk -F ',' '{print $3}'`
                continue
        fi
        res=`echo $line|grep -E "RMC"`
        if [ ! -z "$res" ] ; then


                isfix=`echo $line|awk -F ',' '{print $3}'`
                if [ "$isfix" = "A" ] ;then

                        echo $utc_date,$accuary,$vdop,$pdop,$fixtype,$used_data
                fi

                continue
        fi

        res=`echo $line|grep -E "PSGSA"`
        if [ ! -z "$res" ] ; then

                #                handle_sony_nmea $line
                continue

        fi
        
        res=`echo $line|grep -E "accuracy"`
        if [ ! -z "$res" ] ; then


                echo $line
        fi



done < $1


