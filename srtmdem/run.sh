#!/bin/bash
 
# source the ciop functions (e.g. ciop-log)
source ${ciop_job_include}

# define the exit codes
SUCCESS=0
ERR_NOINPUT=1
ERR_INVALIDFORMAT=2
ERR_NOPARAMS=5
ERR_JPEGTMP=7
ERR_BROWSE=9
 
# add a trap to exit gracefully
function cleanExit ()
{
local retval=$?
local msg=""
case "$retval" in
$SUCCESS) msg="Processing successfully concluded";;
$ERR_INVALIDFORMAT) msg="Invalid format must be roi_pac or gamma";;
$ERR_GDAL) msg="Graph processing of job ${JOBNAME} failed (exit code $res)";;
*) msg="Unknown error";;
esac
[ "$retval" != "0" ] && ciop-log "ERROR" "Error $retval - $msg, processing aborted" || ciop-log "INFO" "$msg"
exit $retval
}
trap cleanExit EXIT
 
export PATH=/application/srtmdem/bin:$PATH 
 
# retrieve the parameters value from workflow or job default value
format="`ciop-getparam format`"

case $format in
  roi_pac)
    option="";;
  gamma)
    option="-g";;
  *)
    exit $ERR_INVALIDFORMAT;;
esac

cd $TMPDIR

while read inputfile
do
  pts=`centroid $inputfile`
  lon=`echo $pts | cut -d " " -f 1`
  lat=`echo $pts | cut -d " " -f 2`
  
  SRTM.py $lat $lon $TMPDIR/dem -D /application/SRTM/data $option -s
  
  ciop-publish -M dem*
  
  rm -fr dem*
done
