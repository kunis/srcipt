all_file=`adb shell ls /sdcard/2016*|tr -d '\r'`

for f in $all_file
do

        adb pull ${f}   
done
