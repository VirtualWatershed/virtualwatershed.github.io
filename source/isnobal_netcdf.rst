iSNOBAL modeling with NetCDF
============================

iSNOBAL is certainly a worthy physical model for representing snow melt-
water input systems. However, it is due for a modernization effort. Since
iSNOBAL is so popular with researchers in the WC-WAVE project, we made this
modernization a priority.

Here we describe how we transform iSNOBAL-specific IPW data in a series of many,
typically thousands, of files into a single NetCDF file. By doing so we may more
easily create and track iSNOBAL input data. 

To generate the lat and lon, which we need to conform with CF convention,
we need to convert UTM grid location to latitude and longitude. We can do this
using the `utm <https://pypi.python.org/pypi/utm>`_ tool written in Python. 
We will generate an array on the
fly using a python list comprehension and some information about the grid, which 
we gleaned from the IPW file's header.

.. code-block:: python

    import numpy as np
    
    lon_arr, lat_arr = map(np.array, 
                   [utm.utmToLatlon(x, y, 11, 'U')[:2] 
                    for x in [bline + dline*i for i in range(nline)]
                        for y in [bsamp + dsamp*i for i in range(nsamp)]
                   ])


then use the arrays to populate lat and lon variables

.. code-block:: python
    
    lat[:] = lat_arr
    lon[:] = lon_arr


