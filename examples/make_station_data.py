"""
Example of translating tabular weather station data to NetCDF.

Author: Matt Turner <maturner01@gmail.com>
File: examples/make_station_data.py
"""
from netCDF4 import Dataset
import numpy as np
import pandas as pd

ncfile = Dataset('pygen_station_data.nc', mode='w', format='NETCDF4')

# `None` stands for UNLIMITED here
time_dim = ncfile.createDimension('time', None)
station_dim = ncfile.createDimension('station', 3)

station = ncfile.createVariable('station', str, ('station',))
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
temp = ncfile.createVariable('temp', np.float32, ('time', 'station'),
                             fill_value=-999.99)
temp.units = 'K'
temp.standard_name = 'air_temperature'

# Load tabular data and populate netcdf
station_info = pd.read_csv('station_info.csv')
station_weather = pd.read_csv('station_weather.csv')

station[:] = station_info.station_name.values

lon[:] = station_info.lon.values
lat[:] = station_info.lat.values
alt[:] = station_info.alt.values

station_weather.sort(['time', 'station_name'], inplace=True)

times = station_weather.time.copy()
times.sort()
time[:] = times.unique()

temp_array = np.reshape(station_weather.temp.values,
                        (len(time), len(station)))

temp[:, :] = temp_array

ncfile.close()
