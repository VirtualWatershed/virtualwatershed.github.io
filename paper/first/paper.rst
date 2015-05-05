The virtual watershed platform has been built of various "cyberinfrastructure"
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


Infrastructure for precipitation sensitivity studies with iSNOBAL
-----------------------------------------------------------------


Joel Johanson's Grid Maker
``````````````````````````


WRF as climate forcing data
---------------------------



