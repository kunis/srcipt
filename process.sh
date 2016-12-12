all_makefile=`find . -type f -name 'Android.mk'`
system_dir=out/target/product/newton/system

function match_makefile()
{
      for file in  $all_makefile
      do
          result=`grep -w "$1" $file`
	  result1=`echo $result| grep -w "LOCAL_MODULE"`
          result2=`echo $result| grep -w "LOCAL_PACKAGE_NAME"`
	  if [ -n "$result" -a -n "$result1" ]; then
	      
	      echo  $file
	      break
	 
          fi
	  if [ -n "$result" -a -n "$result2" ];then
	      echo  $file
	      break 
	  fi 
      done
      

}
function get_module_tags()
{

	 result=`grep -w "LOCAL_MODULE_TAGS" $1`
	 if [ -n "result" ];then
              tag=`echo $result |awk -F ':=' '{print $2}'`
	      echo $tag
         fi

}

function process_share_lib()
{
   lib_dir=$system_dir/lib
   all_lib_file=`find $lib_dir -type f -exec basename {} \;`
   for lib_file in $all_lib_file 
   do     
	   lib_file_name=`echo $lib_file |awk -F '.' '{print $1}'`
	   makefile=`match_makefile  $lib_file_name`
	   if [-n "$makefile" ];then 
	       echo `dirname $makefile` $lib_file
	   else
	       echo $lib_file
           fi

   done



   return

}
function process_execute_bin()
{

   exec_dir=$system_dir/bin
   all_exec_file=`find $exec_dir -type f -exec basename {} \;`
   for exec_file in $all_exec_file 
   do      
	   makefile=`match_makefile  $exec_file`
	   echo `dirname $makefile` $exec_file 

   done



}

function process_android_package()
{
   app_dir=$system_dir/app
   all_app=`ls $app_dir`
   for app in $all_app
   do      
	   makefile=`match_makefile  $app`
	   if [ -n "$makefile" ];then 
	     echo `dirname $makefile` $app `get_module_tags $makefile` 
           else
	     echo `dirname $makefile $app` 	   
           fi
   done


}

function process_android_private_package()
{
   priv_app_dir=$system_dir/priv-app
   priv_all_app=`ls $priv_app_dir`
   for app in $priv_all_app
   do      
	   makefile=`match_makefile  $app`
	   if [ -n "$makefile" ];then 
	     echo `dirname $makefile` $app `get_module_tags $makefile` 
           else
	     echo `dirname $makefile $app` 	   
           fi
   done


}
process_share_lib 
process_android_package
process_execute_bin
process_android_private_package
