Workflow design
===============

Data 
****

This application uses SRTM tiles. 

Software and COTS
*****************

GMTSAR make_dem.csh script
--------------------------

To generate the DEM for GMTSAR [#f1]_ interferogram generation, the application uses the make_dem.csh script.

 Ran Novitsky Nof SRTM.py script
 -------------------------------
 
To generate the ROI_PAC [#f2]_ and Gamma [#f3]_ DEM, the application reuses parts of the approach found here: http://rnovitsky.blogspot.it/2009/05/howto-create-dem-for-roi-pac-processing.html.

Workflow design
***************

The application's data pipeline activities can be defined as follows:

Use the GMTSAR make_dem.csh script or Ran Novitsky Nof SRTM.py script to apply stich the SRTM tiles over an area spanning 1.5 degrees in all cardinal directions starting from the SAR product centroid.

.. uml::

  !define DIAG_NAME Workflow example

  !include includes/skins.iuml

  skinparam backgroundColor #FFFFFF
  skinparam componentStyle uml2

  start
  
  while (check stdin?) is (line)
    :Stage-in data;
    :Stich SRTM tiles;
    :Stage-out DEM;
  endwhile (empty)

  stop

This translates into a very simple workflow containing a single processing step: strm-dem 

The simple workflow can be represented as:

.. uml::

  !define DIAG_NAME Workflow example

  !include includes/skins.iuml

  skinparam backgroundColor #FFFFFF
  skinparam componentStyle uml2

  start

  :node_srtmdem;
  
  stop

The *node_srtmdem* is described in details in :doc:`/field/dem/lib_dem_insar1/src/main/doc/fieldguide/nodes/index`

.. [#f1] `GMTSAR - An InSAR processing system based on GMT <http://topex.ucsd.edu/gmtsar/>`_

.. [#f2] `Repeat Orbit Interferometry PACkage (ROI_PAC) <www.roipac.org/>`_

.. [#f3] `GAMMA SAR and Interferometry Software <http://www.gamma-rs.ch/no_cache/software.html>`_
