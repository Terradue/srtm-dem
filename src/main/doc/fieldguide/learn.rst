What you will learn
===================

With this field guide application, you will learn to create a Web Processing Service (WPS) for the generation of a Digital Elevation Model taking as input a reference to a SAR product catalogue entry.

The SAR product catalogue entry contains the geographical area covered and this information is used to stich SRTM tiles together extending the geographical area half degree in all directions.

Where is the code
+++++++++++++++++

The code for this tutorial is available on GitHub repository `Developer Cloud Sandbox SRTM DEM generation <https://github.com/Terradue/strm-dem>`_.

To deploy the application on a Developer Sandbox:

.. code-block:: console

  cd ~
  git clone git@github.com:Terradue/srtm-dem.git
  cd srtm-dem
  mvn install
  
This will copy the application resources on the /application volume.

The code can be modified (e.g. to support other DEM) by forking the repository here: `<https://github.com/Terradue/srtm-dem/fork>`_

Questions, bugs, and suggestions
++++++++++++++++++++++++++++++++

Please file any questions, bugs or suggestions as `issues <https://github.com/Terradue/srtm-dem/issues/new>`_ or send in a pull request.
