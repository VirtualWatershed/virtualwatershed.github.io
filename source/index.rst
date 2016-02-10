Cyberinfrastructure Solutions for Watershed Hydrology
=====================================================

What is the Virtual Watershed? Briefly, it is a collection of
`"cyberinfrastructure" <http://www.nsf.gov/div/index.jsp?div=ACI>`_
*services*. A cyberinfrastructure service is just like other services, like
public transportation. The use cases below illustrate 
how these cyberinfrastructure services can make watershed science more
efficient and enable scientists to ask new modeling questions.

.. toctree::
    :maxdepth: 2
    
    vw-py-vwclient
    isnobal



User Story 1: ISNOBAL modeling in Reynolds Creek, Idaho
-------------------------------------------------------

This use case was the first use case we considered and became the prototype
for the entire system. Like other models a hydrologist may use,
ISNOBAL takes as input and outputs a file format that's unique to ISNOBAL. No
other hydrological model uses this format. Clarissa Enslin, a graduate student
at Idaho State University, was tasked with using ISNOBAL to better understand
the difference between snow water input, a key number for predicting water
availability, in wet and dry years. 

ISNOBAL is part of the `"Image Processing Toolbox" 
<http://cgiss.boisestate.edu/~hpm/software/IPW/>`_. 
The current best practice for creating ISNOBAL-ready inputs, 
as defined by the creators of ISNOBAL and IPW, is to use
other functions that are part of the IPW. Fine, except the only online
documentation hasn't been updated since 2002, the source code is only available
if you know someone, and even if you manage to obtain the source code, the
makefiles don't seem to be compatible with modern ``make``. 

Clarissa has already spent months doing Quality Assurance/Quality Control
(QA/QC) on raw data from the Johnston Draw subcatchment of Reynolds Creek. The
last thing she or any other watershed scientist wanting to use ISNOBAL should
have to do is spend extra time on getting archaic software to work. Instead,
Donna Delparte and her students Joel Johansen and Tucker Chapman 
have built a tool for statistical prediction of climate variables on a grid,
which is what ISNOBAL requires. In conjunction with ISNOBAL model adaptors that
allow ISNOBAL to take properly-formatted 
`netCDF <http://www.unidata.ucar.edu/software/netcdf/>`_ 
files as input, this greatly simplifies the previous ISNOBAL workflow which
required the generation of as many files as timesteps.

In the face of trying watershed behavior under future climate scenarios
and the desire to understand the behavior of watershed across historic 
water years, Clarissa and other watershed scientists are faced with a data
management problem. This is not to say they are unable to manage their data
themselves, but again, if they didn't have the overhead of manually managing
model input and output and keeping track of which inputs and outputs correspond
to which historical or forecast scenario, this would allow her and others
to focus on science instad of cyberinfrastructure.  


User Story 2: Precipitation Runoff Modeling in the Lehman Creek Watershed
-------------------------------------------------------------------------

With a heating climate and dwindling snowpack in many mountainous regions and
ever-increasing demand from southern Nevada, the Lehman Creek watershed in Great
Basin National Park is under increasing pressure. Thus it's more critical than
ever to understand the sensitivity of the watershed under various 
climate change scenarios. Chao Chen and her PhD advisor Sajjad Ahmad are
pursuing this important work.

Like many hydrological models, there are many parameters that must be
specified in order to run PRMS, the model being used to study Lehman Creek
hydrology. In addition to being able to run PRMS through a web interface and to
simplify data management for running multiple scenarios, the Lehman Creek team
would also like to be able to interactively manipulate parameters.
Parameterization is very important.  Without proper parameterization, the model
is not scientifically valid.

User Story 3: Coupling floodplain succession models to flooding models
----------------------------------------------------------------------

The fundamental problem in this use case is similar to the first use case:
because many of these models were created in isolation before standards were
available or widely adopted, they are challenging to use together.
Specifically, Sarah Miller from Dan Cadol's group at New Mexico Tech uses 
field observations and satellite imagery along with the 
`CASiMiR <http://www.casimir-software.de/ENG/download_eng.html>`_ modeling package
to understand landscape succession in the Jemez River floodplain.  At the
University of New Mexico, Angela Gregory from Mark Stone's research group
uses DFLOW to understand floodwater dynamics of the Jemez River, 
which includes shear stress.  The amount of shear stress across the 
floodplain can be used to determine which plants and soils will remain after a
flood and which will be destroyed.

Here we have a technological mismatch. DFLOW runs on the University of New
Mexico's `CARC Research Supercomputers <https://www.carc.unm.edu/>`_ while 
CASiMiR runs locally on Windows. DFLOW outputs shear stress in an unstructured
mesh in netCDF. CASiMiR requires specifically-formatted 
`ESRI Ascii files <http://resources.esri.com/help/9.3/arcgisdesktop/com/gp_toolref/spatial_analyst_tools/esri_ascii_raster_format.htm>`_.

In addition to this mismatch of platforms and data formats, we have the
opportunity as in User Story 1 to simplify the entire data management process. 
One of the major goals of the Virtual Watershed is to enable watershed
scientists to investigate the impacts of climate change scenarios on the
watersheds they study. The flood dynamics and landscape succession of the Jemez
River and surrounding area is dependent on the 


User Story 4: Modeling the Hydrodynamics of the Valles Caldera in New Mexico
----------------------------------------------------------------------------

Understanding the hydrodynamics of the Valles Caldera will be important 
in its own right and for understanding flood dynamics and vegetation succession
downstream in the Jemez River floodplain. Modeling the Valles Caldera is a
difficult scientific problem because of the volcanic activity just underneath
the surface.  This causes heating and must be accounted for, which has made the
Valles Caldera difficult for many hydrologists to model. Michael Wine, a
graduate student in Dan Cadol's research group at New Mexico Tech, is pursuing
this difficult task.

Of course there are cyberinfrastructure problems as well. First and foremost,
there is no obvious way to download model-ready data at a fine enough 
resolution to be useful in the Valles Caldera.  We only have access to some
`weather station data made available by the Desert Research Institute
<http://www.wrcc.dri.edu/vallescaldera/>`_.  So this shares a requirement from
User Story 1, that the watershed scientists need gridded data, not weather 
station data, at a useful resolution. Since the outputs of this modeling will be
useful for Sarah and Angela working on User Story 2, Michael will need to be able
to share his data outputs in a meaningful way so they may be easily found and
understood by his collaborators. We'll also want to understand multiple
scenarios, so the model run tracking capabilities of the Virtual Watershed
should be valuable here as well.




The Virtual Watershed System
----------------------------

With these use cases in mind, here is the system we've created that either
solves or will solve these problems. Interspersed with this are links to the
code repositories on GitHub and the current prototypes available online for
public use.


Digital Map of Virtual Waterhsed Code and Resources
---------------------------------------------------

* `Virtual Watershed Organization on GitHub
  <https://github.com/VirtualWatershed>`_
* `vw-doc, the source for this documentation you're reading right now!
  <https://github.com/VirtualWatershed/vw-doc>`_
