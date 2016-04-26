Digital Elevation Model generation
==================================

Digital Elevation Model (DEM) are mandatory inputs for several applications such as interferometry (e.g. ROI_PAC, GMTSAR and Gamma). 

This field guide uses the Developer Cloud Sandbox service to implement an auxiliary service to generate DEM taking as input a reference to a SAR product catalogue entry.

This work reuses parts of the approach found here: `<http://rnovitsky.blogspot.it/2009/05/howto-create-dem-for-roi-pac-processing.html>`_. We thank `Ran Novitsky Nof <http://www.blogger.com/profile/13547751431352852077>`_ for that! 

Contents:

.. toctree::
   :maxdepth: 1
   
   What you will learn <learn>
   Addressing a scientific and processing goal <goal>
   Workflow design <workflow>
   Processing nodes design <nodes/index>
   Application testing <testing>
   Data preparation <data>
..   Application integration <integration>
..   Application exploitation <exploitation>
..   Going further <further>
