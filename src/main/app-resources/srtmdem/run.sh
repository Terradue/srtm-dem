#!/bin/bash
 
# source the ciop functions (e.g. ciop-log)
source ${ciop_job_include}

# define the exit codes
SUCCESS=0
ERR_NODEM=7

# add a trap to exit gracefully
function cleanExit ()
{
  local retval=$?
  local msg=""
  
  case "$retval" in
    ${SUCCESS})           msg="Processing successfully concluded";;
    ${ERR_NODEM})         msg="DEM not generated";;
    *) msg="Unknown error";;
  esac
  
  [ "${retval}" != "0" ] && ciop-log "ERROR" "Error ${retval} - ${msg}, processing aborted" || ciop-log "INFO" "${msg}"
  
  exit ${retval}
}

trap cleanExit EXIT

export PATH=/application/srtmdem/bin:${PATH} 
export DISPLAY=:99.0

while read input
do
  UUIDTMP="/tmp/$( uuidgen )"
  mkdir ${UUIDTMP}
  cd ${UUIDTMP}

  # SRTM.py uses matplotlib, set a temporary directory
  export MPLCONFIGDIR=${UUIDTMP}/

  ciop-log "INFO" "Working in ${UUIDTMP}" 

  dem_name="$( uuidgen )"

  wkt="$( ciop-getparam wkt )"
  
  ciop-log "DEBUG" "wkt is ${wkt}"

  # the centroid script get the WKT footprint and calculates the
  # geometry centroid
  pts=$( centroid "${wkt}" )
  lon=$( echo ${pts} | cut -d " " -f 1 )
  lat=$( echo ${pts} | cut -d " " -f 2 )

  ciop-log "DEBUG" "centroid script finished: ${lon} ${lat}"

  ciop-log "INFO" "Generating DEM"

  # Invoke the SRTM.py
  SRTM.py ${lat} ${lon} ${UUIDTMP}/${dem_name} -D /data/SRTM41/ ${option} 1>&2
  [ ! -e ${UUIDTMP}/${dem_name}.dem ] && exit ${ERR_NODEM}

  # save the bandwidth
  ciop-log "INFO" "Compressing DEM"
  
  tar cfz ${dem_name}.dem.tgz ${dem_name}*

  # have the compressed archive published and its reference exposed as metalink
  ciop-log "INFO" "Publishing results"
  
  ciop-publish -m ${UUIDTMP}/${dem_name}.dem.tgz  

  # clean-up for the next dataset reference
  rm -rf ${UUIDTMP}
done

exit ${SUCCESS}
