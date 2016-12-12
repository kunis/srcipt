#!/bin/bash
#  
# upgrade sony gps firmware v2.22
#
function push_gps_fw()
{

        adb push ./sony_gps_fw_e.bin  /system/etc/firmware/
        adb push ./sony_gps_fw.bin  /system/etc/firmware/
        adb shell sync

}

function push_agps()
{

        adb push ./sony_agps.bin  /system/etc/firmware/
        adb shell sync

}

function push_sensorhub_fw()
{

        adb push ./sensorhub.bin  /system/etc/firmware/
        adb shell sync

}

function upgrade_fw
{

        echo "start upgrade gps firmware V2.22..."
        adb shell "echo 1 > /sys/class/huami/sensor_hub/gps_upgrade_fw"
        echo "done"
        adb shell cat /sys/class/huami/sensor_hub/gps_upgrade_fw
}
adb wait-for-device
while true
do
        version=`adb shell cat /sys/class/huami/sensor_hub/version`
        if [ "$version" != "0.0.0" ];then

                echo "sensorhub ready! version: "$version
                break
        fi
done

adb remount
push_gps_fw
upgrade_fw
