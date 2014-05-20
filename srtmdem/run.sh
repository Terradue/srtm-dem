#!/bin/bash
 
# source the ciop functions (e.g. ciop-log)
source ${ciop_job_include}

# define the exit codes
SUCCESS=0
ERR_INVALIDFORMAT=2
ERR_NOIDENTIFIER=5
ERR_NODEM=7

# add a trap to exit gracefully
function cleanExit ()
{
local retval=$?
local msg=""
case "$retval" in
$SUCCESS)           msg="Processing successfully concluded";;
$ERR_INVALIDFORMAT) msg="Invalid format must be roi_pac or gamma";;
$ERR_NOIDENTIFIER)  msg="Could not retrieve the dataset identifier";;
$ERR_NODEM)         msg="DEM not generated";;
*) msg="Unknown error";;
esac
[ "$retval" != "0" ] && ciop-log "ERROR" "Error $retval - $msg, processing aborted" || ciop-log "INFO" "$msg"
exit $retval
}
trap cleanExit EXIT
 
export PATH=/application/srtmdem/bin:$PATH 

export DISPLAY=:1.0

# SRTM.py uses matplotlib, set a temporary directory
export MPLCONFIGDIR=$TMPDIR/
 
# retrieve the DEM format to generate
format="`ciop-getparam format`"

case $format in
  roi_pac)
    option="";;
  gamma)
    option="-g";;
  gmtsar)
    flag="true";;
  *)
    exit $ERR_INVALIDFORMAT;;
esac

cd $TMPDIR

# read the catalogue reference to the dataset
while read inputfile
do
   ciop-log "INFO" "`basename $inputfile` centroid is ($lon $lat)" 
   dem_name=`ciop-casmeta -f "dc:identifier" $inputfile`
   [ -z "$dem_name" ] && exit $ERR_NOIDENTIFIER 

   # the centroid R script get the WKT footprint and calculates the geometry centroid
   pts=`centroid $inputfile`
   lon=`echo $pts | cut -d " " -f 1`
   lat=`echo $pts | cut -d " " -f 2`

  # GMTSAR
  [ $flag == "true" ] && {
   # invoke make_dem.csh
   #recreate a 3 deg bbox around the centroid lon/lat
    lon1=$( echo "$lon - 1.5" | bc ) 
    lon2=$( echo "$lon + 1.5" | bc )
    lat1=$( echo "$lat - 1.5" | bc )
    lat2=$( echo "$lat + 1.5" | bc )
    ciop-log "INFO" "using GMTSAR with coords $lon1 $lon2 $lat1 $lat2"

    cd $TMPDIR
    export PATH=$PATH:/usr/local/GMTSAR/gmtsar/csh/
    /usr/local/GMTSAR/gmtsar/csh/make_dem.csh $lon1 $lon2 $lat1 $lat2 2 /data/SRTM3/World/
    
    #rename the output
    mv dem.grd $dem_name.dem
    mv dem_grad.png $dem_name.png
    mv dem_grad.kml $dem_name.kml
    
  } || {

   # use the dataset identifier as filename for the result
   # SRTM.py concatenates .dem.<extension>

   # invoke the SRTM.py
   # the folder /application/SRTM/data contains the SRTM tiles in tif format
   ciop-log "INFO" "Generating DEM"
   SRTM.py $lat $lon $TMPDIR/$dem_name -D /data/SRTM41/ $option 1>&2
  } 

  # check the output
  [ ! -e $TMPDIR/$dem_name.dem ] && exit $ERR_NODEM

  # save the bandwidth 
  ciop-log "INFO" "Compressing DEM"
  tar cfz $dem_name.dem.tgz $dem_name*   
 
  # have the compressed archive published and its reference exposed as metalink
  ciop-log "INFO" "Publishing results"
  ciop-publish -m $TMPDIR/$dem_name.dem.tgz  
   
  # clean-up for the next dataset reference
  rm -fr $dem_name*
   
done
