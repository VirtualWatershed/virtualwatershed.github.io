.. Virtual Watershed Documentation documentation master file, created by
   sphinx-quickstart on Mon Mar 16 16:02:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tri-State EPSCoR WC-WAVE's Virtual Watershed
============================================

Scientific tools
----------------

The virtual watershed platform has been built of various `"cyberinfrastructure"
<http://www.nsf.gov/div/index.jsp?div=ACI>`_
resources including a robust data management platform (the VW data engine),
a web service that converts properly formatted CSV data to NetCDF data, web
services that run hydrological models, and cutting-edge 3D immersive
visualization environments. The "adaptors" are the glue that holds this together
in a single framework. 

There are adaptors for getting data into the data engine, adaptors that check
which models the NetCDF files output from grid making are compatible with,
convert model output back to our common format, NetCDF, and create metadata so
that all this data can be (re)discovered later using the data engine's API. 
We deliver this complete package through a web app, which can be thought of as
the human adaptor. 

To get started, continue on to the :ref:`tutorial... <tutorial>`


Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   netcdf 
   isnobal_netcdf
   watershed
   isnobal
   isnobal_experiment


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

