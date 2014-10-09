What you will learn
===================

With this field guide application, you will learn:

1. To manage test data in a sandbox - you will copy the USGS Landsat sample products, convert them into the ERDAS image format, copy them to S3 and register them in the sandbox catalogue
2. To create a simple application - you will implement a Python module and test it against the registered Landsat data
3. To test the application - you will execute the processing step and inspect the results and will execute the workflow
4. To exploit the application - you will use the Web Processing Service (WPS) interface to invoke the application

Where is the code
+++++++++++++++++

The code for this tutorial is available on GitHub repository `Developer Cloud Sandbox Python tutorial - Landsat NDVI <https://github.com/Terradue/dcs-python-ndvi>`_.

To deploy the tutorial on a Developer Sandbox:

.. code-block:: console

  cd ~
  git clone git@github.com:Terradue/srtm-dem.git
  cd srtm-dem
  mvn install
  
This will:

* copy the application resources on the /application volume.

The code can be modified (e.g. to support Landsat 8) by forking the repository here: `<https://github.com/Terradue/srtm-dem/fork>`_

Questions, bugs, and suggestions
++++++++++++++++++++++++++++++++

Please file any questions, bugs or suggestions as `issues <https://github.com/Terradue/srtm-dem/issues/new>`_ or send in a pull request.
