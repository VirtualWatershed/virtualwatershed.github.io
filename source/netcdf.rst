CF-NetCDF as reference data model for VW
========================================

Intro
-----

In this project we want to collect mutually relevant data from WC-WAVE
researchers that will be discoverable as a first step to being usable by
other WC-WAVE researchers for whatever model they choose. In short, this 
necessitated the choice of a data model. The NetCDF data model itself is 
sensible and implemented in common programming languages, but it also offers
web-based tools (a RESTful API?) for selecting and downloading only subsets of 
data on disk. Since NetCDF knows how to slice by loading selectively from disk,
the user does not have to load everything into memory before slicing.

NetCDF is intended as a self-describing data format. In other words, it contains
its own metadata. The Climate and Forecast (CF) conventions provide a common
guiding framework for writing this metadata, so that other any researcher 
following the CF standard can easily share or process thiers or others' data
with a common set of tools like 
`cfplot <http://www.met.reading.ac.uk/~andy/cfplot_sphinx/_build/html/>`_.
CF has the canonical documentation on its standard on its organization page:
`http://cfconventions.org/documents.html 
<http://cfconventions.org/documents.html>`_.

Although necessary for creating a cutting-edge toolset for hydrological
modeling, all this infrastructure comes with some conceptual overhead. Here is
some background on the CF-NetCDF format.


Resources for Understanding NetCDF(-python)
-------------------------------------------

Because Python seems to be the most widely used language in our project, we will
be using and supporting the `NetCDF-python API <https://github.com/Unidata/netcdf4-python>`_.

Probably the best way to quickly get a feel for NetCDF, model and Python
interface, is to see these two python notebooks by the creator of the
NetCDF-python API: `reading_netCDF.ipynb <http://nbviewer.ipython.org/github/Unidata/netcdf4-python/blob/master/examples/reading_netCDF.ipynb>`_ 
and 
`writing_netCDF.ipynb <http://nbviewer.ipython.org/github/Unidata/netcdf4-python/blob/master/examples/writing_netCDF.ipynb>`_.

Also, have a look at the basic data model for NetCDF files:

.. figure:: figures/nc-classic-uml.png
   :alt: Classic Data Model

   Classic Data Model

Taken from `UNIDATA
site <http://www.unidata.ucar.edu/software/netcdf/docs/html_tutorial/nc-classic-uml.png>`_.
There are some important things to note so we are speaking the same language.
First, a ``Dataset`` is a *container* for ``dimensions``, ``variables``, and
``attributes``, themselves containers for their data and metadata about 
themselves or the ``Dataset``. The next part will require the basic understanding 
gained from working through the above ipynb's. 


Example 1: Create a NetCDF of temperature on a grid
---------------------------------------------------

In overly simple terms we use NetCDF to represent data as a function of some
coordinates, like a grid of longitude and latitude values. This example will
show how we create a NetCDF of air temperatures on a 3x4 grid. 

First, in order to follow the CF standard for our variable name, we need to
check what we should use at the `web tool for CF standard names 
<http://cfconventions.org/Data/cf-standard-names/27/build/cf-standard-name-table.html>`_.
Luckily this one is easy, the standard name is `air_temperature`, and actually
the standard name goes in the metadata about the variable, and we could use a
short name like `temp` for the data representation. However, since
`air_temperature` is not too long, we'll use that for the NetCDF variable name
since it's easier to remember one name than two. Some of the code is taken directly from the 
`writing_netCDF.ipynb <http://nbviewer.ipython.org/github/Unidata/netcdf4-python/blob/master/examples/writing_netCDF.ipynb>`_.
example from the netCDF-python documentation.

To represent the "x" and "y" latitude and longitude coordinates, we consult 
Chapter 4 of the CF standard, `Coordinate types <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch04.html>`_.
We will format and give attributes for our coordinate variables, latitude and
longitude, according to the instructions there.

The process of creating a new .nc dataset is:

#. Create an empty Dataset object
#. Create the 'dimensions', e.g. lat, lon, altitude, time
#. Create the variables. Each of the dimensions has an associated variable
   where the actual values of the dimension are stored. Here we also attach
   weather data like temperature, snow water equivalent, solar radiation, etc.
#. Add attributes, which are just additional metadata. There is global- and 
   variable-scope metadata. See CF Conventions `Section 2.6: Attributes 
   <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch02s06.html>`_
   for the reference documentation.

Let's see the exact mechanics of this:

.. code-block:: python
    
    from __future__ import print_function
    import netCDF4      # Note: python is case-sensitive!
    import numpy as np  # numpy provides our data types; see var init below

    # initialize new dataset
    ncfile = netCDF4.Dataset('new.nc', mode='w', format='NETCDF4_CLASSIC') 

    # initialize dimensions
    lat_dim = ncfile.createDimension('lon', 3)     # longitude axis
    lat_dim = ncfile.createDimension('lat', 4)     # latitude axis

    # Define two variables with the same names as dimensions,
    # a conventional way to define "coordinate variables".
    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'

    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'    

    # Temperature is a function of latitude and longitude
    temp = ncfile.createVariable('temp', np.float64, ('lat','lon')) 
    temp.units = 'K'  # degrees Kelvin
    temp.standard_name = 'air_temperature'  # this is a CF standard name

    # Write latitudes, longitudes.
    nlats = len(lat_dim)
    nlons = len(lon_dim)
    # Note: the ":" is necessary in these "write" statements
    lat[:] = -90. + (180./nlats)*np.arange(nlats) # south pole to north pole
    lon[:] = (180./nlats)*np.arange(nlons) # Greenwich meridian eastward 
    
    # populate temperature ndarray with reasonable earth temperatures
    temp_arr = np.random.uniform(low=280, high=330, size=(nlats,nlons))
    temp[:,:] = temp_arr

    # add attributes, all global; see CF standards 
    ncfile.title = 'My model data'
    ncfile.institution = 'Idaho State University'
    ncfile.source = 'Weather Stations in Reynolds Creek Watershed'
    ncfile.history = 'Existed since 1990, first time in public domain'
    
    # to save the file to disk, close the `ncfile` object
    ncfile.close()

To confirm that this worked, check the output of ``ncdump`` at the command line.

.. code-block:: bash
    
    ncdump new.nc

You should see this, but with different random ``data``:


.. code-block:: cdl

    netcdf new {
    dimensions:
            lon = 3 ;
            lat = 4 ;
    variables:
            float lat(lat) ;
                    lat:units = "degrees_north" ;
                    lat:long_name = "latitude" ;
            float lon(lon) ;
                    lon:units = "degrees_east" ;
                    lon:long_name = "longitude" ;
            double temp(lat, lon) ;
                    temp:units = "K" ;
                    temp:standard_name = "air_temperature" ;

    // global attributes:
                    :title = "My model data" ;
                    :institution = "Idaho State University" ;
                    :source = "Weather Stations in Reynolds Creek Watershed" ;
                    :history = "Existed since 1990, first time in public domain" ;
    data:

     lat = -90, -45, 0, 45 ;

     lon = 0, 45, 90 ;

     temp =
      303.51644518952, 329.87896020043, 320.682946298552,
      282.647054412333, 294.753235738639, 297.738184716573,
      290.698305690645, 321.484896481591, 303.564564474415,
      304.710075475009, 321.517749128517, 324.796144202603 ;
    }

Example 2: Create a CF-formatted NetCDF of temperature at weather stations
------------------------------------------------------------------------

Consider the following situation: You have 
weather stations named ``s1``, ``s2``, and ``s3`` recording the temperature at
three-dimensional points in space (x,y,z), which correspond to a longitude, 
latitude, and altitutde. Each station records temperature every fifteen
minutes. The data has been processed so that the all four measurements taken
within an hour are averaged, so our temperature is really *mean temperature*,
but in most spots, we'll just call it ``temp`` for short. Here is our tabular
data:

==============  =======  ===========
station name    time     temp (K)
==============  =======  ===========
s1              0        301.4
s2              0        298.0
s3              0        310.2
s1              1        300.4    
s2              1        293.0    
s3              1        306.2
s1              2        302.4  
s2              2        288.0 
s3              2        308.1 
==============  =======  ===========

This time, our NetCDF dimensions are ``station name`` and ``time`` instead of
``lat`` and ``lon``. Then in our CDL our dimension declaration is

.. code-block:: cdl

    dimensions:
            time = UNLIMITED;
            station = 3;
            name_strlen = 2; // `s1` has two characters

By declaring ``time`` as ``UNLIMITED``, we allow for future measurements to be
appended to the Dataset.

We also have this tabular data about the stations:

==============  =======  ========  ======
station name    lat      lon       alt
==============  =======  ========  ======
s1              49.2     -115.4    1004
s2              49.4     -114.0    1025
s3              50.1     -116.2    923
==============  =======  ========  ======

So although lat, lon, and alt won't be "dimensions", they will be included as
"variables". We will consider them functions of "station name", each represented 
in the CDL as

.. code-block:: cdl

     
    variables:
            char station_name(station):
                    station_name:long_name = "station name";
                    station_name:cf_role = "timeseries_id";
            float lat(station) ;
                    lat:long_name = "station latitude" ;
                    lat:standard_name = "latitude" ;
                    lat:units = "degrees_north" ;
            float lon(station) ;
                    lon:long_name = "station_longitude" ;
                    lon:standard_name = "longitude" ;
                    lon:units = "degrees_east" ;
            float alt(station) ;
                    alt:long_name = "vertical distance above the surface";
                    alt:standard_name = "height";
                    alt:units = "m";
                    alt:positive = "up";
                    alt:axis = "Z";

our temperature variable is a function of station and time:

.. code-block:: cdl

    variables:
            ...
            double time(time);
                    time:standard_name = "time";
                    time:long_name = "time of measurement"
                    time:units = "hours since 2005-10-01 00:00:00"
            float temp(time, station)
                    temp:standard_name = "air_temperature";
                    temp:units = "K";
                    temp:_FillValue = -999.9;


We can consult the examples in the CF Conventions Manual in `Appendix H <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/aph.html>`_ for guidance. We will essentially implement 
`H2.1 <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/aphs02.html>`_
but following the instructions from `the Write NetCDF ipynb <http://nbviewer.ipython.org/github/Unidata/unidata-python-workshop/blob/master/writing_netCDF.ipynb>`_ 
used before. Since we're using the classic data model, our assignments are in
the python procedure are in slightly different order.

.. code-block:: python

    from netCDF4 import Dataset 
    import numpy as np
    from pandas import read_csv

    ncfile = Dataset('pygen_station_data.nc', modw='w', format='NETCDF4_CLASSIC')
    
    # `None` stands for UNLIMITED here
    time_dim = ncfile.createDimension('time', None)
    station_dim = ncfile.createDimension('station', 3)
    name_strlen = ncfile.createDimension('name_strlen', 2)
    
    # dimensions: name_strlen, station, time
    name_strlen = ncfile.createVariable('name_strlen', str, ('name_strlen',))

    station = ncfile.createVariable('station', str, ('station','name_strlen'))
    station.long_name = "station name"
    station.cf_role = "timeseries_id"

    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'hours since 2015-10-01 00:00:00'
    time.long_name = 'time'

    # lon, lat, altitude
    lon = ncfile.createVariable('lon', np.float32, ('station',))
    lon.standard_name = 'longitude'
    lon.long_name = 'station longitude'
    lon.units = 'degrees_east'

    lat = ncfile.createVariable('lat', np.float32, ('station',))
    lat.standard_name = 'latitude'
    lat.long_name = 'latitude'
    lat.units = 'degrees_north'

    alt = ncfile.createVariable('alt', np.float32, ('station',))
    alt.standard_name = 'height'
    alt.long_name = 'vertical distance above the surface'
    alt.units = 'm'
    alt.positive = 'up'
    alt.axis = 'Z'

    # temperature
    temp = ncfile.createVariable('temp', np.float32, ('time','station'),
                                 fill_value=-999.99)
    temp.units = 'K'
    temp.standard_name = 'air_temperature'


We have our tabular data that has the station information in 
`examples/station_info.csv <https://github.com/tri-state-epscor/vw-doc/blob/master/examples/station_info.csv>`_ and the "weather" info (really just temperature)
in `examples/station_weather.csv <https://github.com/tri-state-epscor/vw-doc/blob/master/examples/station_weather.csv>`_. We'll use the `read_csv <http://pandas.pydata.org/pandas-docs/dev/io.html#io-read-csv-table>`_ 
from the `pandas <http://pandas.pydata.org/>`_ data analysis library. We'll 
read those files in and use the data stored in them to finish creating our 
NetCDF version of the weather station data.


.. code-block:: python

    import pandas as pd
    import numpy as np

    station_info = pd.read_csv('examples/station_info.csv')
    station_weather = pd.read_csv('examples/station_weather.csv')

    station[:] = station_info.station_name
    time[:] = station_info.time

    lon[:] = station_info.lon
    lat[:] = station_info.lat
    alt[:] = station_info.alt
    
    station_weather.sort(['time', 'station_name'], inplace=True)  

    temp_array = np.reshape(station_weather.time, (len(time),len(station)))

    temp[:,:] = temp_array

    ncfile.close()


The two blocks of python code in this example can be found in
`example/make_station_data.py <>`_. Run that example from the ``examples``
directory

.. code-block:: bash
    
    cd examples/ && python make_station_data.py

which will create a new file, ``pygen_station_data.nc``. If you haven't already,
get the NetCDF Operators package, `NCO <http://nco.sourceforge.net/>`_. It has
some nice tools, one of which will help us confirm that we have loaded the 
NetCDF ``temp`` variable correctly. Using the `ncks
<http://nco.sourceforge.net/nco.html#ncks-netCDF-Kitchen-Sink>`_ utility (NetCDF
Kitchen Sink, you'll see why) we print a lot of info about the file

.. code-block:: bash

    ncks pygen_station_data.py

.. code-block:: cdl

    time[0]=0 station[0]=s1 temp[0]=301.4 K
    time[0]=0 station[1]=s2 temp[1]=298 K
    time[0]=0 station[2]=s3 temp[2]=310.2 K
    time[1]=1 station[0]=s1 temp[3]=300.4 K
    time[1]=1 station[1]=s2 temp[4]=293 K
    time[1]=1 station[2]=s3 temp[5]=306.2 K
    time[2]=2 station[0]=s1 temp[6]=302.4 K
    time[2]=2 station[1]=s2 temp[7]=288 K
    time[2]=2 station[2]=s3 temp[8]=308.1 K


So just as it was in ``weather_stations.csv`` it is in our newly generated .nc
file.


    
Common data form Description Language (CDL)
-------------------------------------------

The Common data format Description Language is a plain-text, fail-safe way to
create NetCDF datasets. Once you write out the description of the data, you
can run ``ncgen`` (`extended documentation <https://www.unidata.ucar.edu/software/netcdf/docs/netcdf/ncgen.html#ncgen>`_
`manpage documentation <http://www.unidata.ucar.edu/software/netcdf/old_docs/docs_3_6_0/ncgen-man-1.html>`_) 
to create a NetCDF file from a CDL file. This will check your syntax and
initialize a file for you. Here are a few resources for CDL:

* `NetCDF Workshop 2010 page on CDL <https://www.unidata.ucar.edu/software/netcdf/workshops/2010/utilities/CDL.html>`_
* `CDL Syntax <https://www.unidata.ucar.edu/software/netcdf/docs/netcdf/CDL-Syntax.html>`_

Here's how we could do the first example using just CDL files and ``ncgen``. 
There is a CDL file in the `example <https://github.com/tri-state-epscor/vw-doc/tree/master/examples>`_
directory called ``weather_stations.cdl`` that defines weather station data 
from Example 2.  To build an empty NetCDF file we could insert data into, call 

.. code-block:: bash

    ncgen -o weather_stations.nc weather_stations.cdl

and we'd have a new NetCDF file ``weather_stations.nc`` with an all-empty data
section and identical dimension and variable sections.
