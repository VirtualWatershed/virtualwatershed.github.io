.. Virtual Watershed Documentation documentation master file, created by
   sphinx-quickstart on Mon Mar 16 16:02:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: figures/WC-WAVE_banner.png

Python API for the Virtual Watershed
====================================

Developer Tools for Building Scientific Applications
----------------------------------------------------


The virtual watershed platform has been built of various `"cyberinfrastructure"
<http://www.nsf.gov/div/index.jsp?div=ACI>`_
resources. At the backbone of these resources is a robust data management platform, 
which we'll call the VW Data Engine (VWDE).
Using the VWDE as a powerful provider of data (web) services, we are also
building add-on web services that run hydrological models, and cutting-edge 3D immersive
visualization environments. The "adaptors" are the glue that holds this together
in a single framework. This Python API mainly provides adaptors for interacting
with various facets of the virtual watershed.

There are adaptors for getting data into the data engine, adaptors that check
which models the NetCDF files output from grid making are compatible with,
adaptors that convert model output back to our common format, NetCDF, and create metadata so
that all this data can be (re)discovered later using the data engine's API. 
We deliver this complete package through a web app, which can be thought of as
the human adaptor, though that is contained in the 
`vwplatform <https://github.com/mtpain/vwplatform>`_.

To get started interacting with the VWDE through the Python adaptor API, 
continue reading this quickstart guide. It will guide you
through a series of commands that you can use right now in a Python shell.
IPython is a really handy shell and is recommended in general and for this
tutorial guide.

If you are looking for API documentation, see below

**API Documentation Table of Contents**

.. toctree:: 
    :maxdepth: 1

    watershed
    isnobal


Connect to and query the VWDE
-----------------------------

First, the pre-requisites are:

1. You've followed the installation instructions at the `wcwave_adaptors GitHub page <https://github.com/tri-state-epscor/wcwave_adaptors>`_.
2. You've added the  ``wcwave_adaptors`` to your path, either through ``sys.path.append('~/path/to/adaptors')`` or through the ``$PYTHONPATH`` environment variable.
3. You have an account with the Virtual Watershed data engine, which you must ask for. Please email `Matt Turner <maturner@uidaho.edu>`_ for an account.

Now in an IPython (or other) shell, follow along with these examples.

To connect to the virtual watershed

.. code-block:: python
    
    from wcwave_adaptors import VWClient
    vw_client = VWClient('https://vwp-dev.unm.edu', 'your-username', 'your-password')

If you have been authenticated correctly, this will finish silently. 

You may also use this

.. code-block:: python

    vw_client = default_vw_client()

But in order for this to work, you must have personalized your ``default.conf`` 
as described in the `wcwave_adaptors README <https://github.com/tri-state-epscor/wcwave_adaptors#configuration-files>`_.

.. warning::

    The timeout period is undocumented for the VWDE, but seems short. If you
    ever have a long output of HTML returned instead of what this guide says you 
    should get, repeat the above step to re-authenticate.


In order to query all datasets and how many are in the virtual watershed,

.. code-block:: python

    search_result = vw_client.dataset_search()
    
    from wcwave_adaptors import QueryResult
    assert isinstance(search_result, QueryResult)
    
    # search
    total_records = search_result.total
    n_recs_returned = search_result.subtotal
    assert n_recs_returned == 15  # because that is default number of recs returned

    # get the actual search records
    records = search_result.records
    assert len(records) == n_recs_returned  # because that is default number of recs returned

    first_dataset_metadata = records[0]
    assert isinstance(first_dataset_metadata, dict)

.. note::

    In Python, writing ``assert ...`` causes Python to throw an error if the
    statement is ``False``. Otherwise, the program continues on uninterrupted.


If you ``print r0``, you will see the actual metadata record which someone has
generated and inserted for the data. There you can also see the ``downloads``
section of the metadata, which is a list of dictionaries. This contains the 
download link for the data file that the metadata represents. Access it like so:

::

    In [17]: print r0['downloads'][0]['bin'];
    Out[17]: u'http://vwp-dev.unm.edu/apps/vwp/datasets/a33893dd-d919-472a-8583-b35d9cda967a/in.0000.original.bin'

Navigate there (or click the following link) and you will download the iSNOBAL 
input file ``in.0000`` 
(http://vwp-dev.unm.edu/apps/vwp/datasets/a33893dd-d919-472a-8583-b35d9cda967a/in.0000.original.bin).  
All this metadata is for this one file.

This may seem overwhelming, but the ``wcwave_adaptors`` provide help to create
this metadata, which is the topic of the next section.


Create VW metadata and insert it to the database
------------------------------------------------

To follow along with this example, download the binary file linked to above 
to your current working directory. We will create a new "model run" in the
Virtual Watershed Data Engine, upload our data (a "dataset" in VWDE terms) 
tagged as part of this new model run, and then create and insert metadata for 
that dataset.

First, we will create a new model run, which returns the model run UUID
generated by the VWDE. We will use this in later steps to tell the VWDE which
uploaded files belong to what model run UUID.

Create a new model run
``````````````````````

.. code-block:: python

    # create a new model run
    new_mr_uuid = \
        vw_client.initialize_modelrun(
            model_run_name='example model run for vw-doc', 
            description='will be inserting only one file, in.0000, a multi-banded iSNOBAL input grid file', 
            researcher_name='Matt Turner', keywords='isnobal,example,idaho')

    print new_mr_uuid  # something like u'0a3e8c1f-c09a-46a3-8acb-6816ebd25e69'


Now we could use another search, the model run search, to search for datasets 
associated with our new model run. 

.. code-block:: python

    mr_search_results = vw_client.modelrun_search()
    new_mr = [r for r in res.records if r['Model Run UUID'] == new_mr_uuid]

The first and only element of the list new_mr is (with a different UUID)

::

    [{u'Description': u'will be inserting only one file, in.0000, a multi-banded iSNOBAL input grid file',
      u'Keywords': u'isnobal,example,idaho',
      u'Model Run Name': u'example model run for vw-doc',
      u'Model Run UUID': u'a26e4bbc-6481-4525-8988-d30e7db28df8',
      u'Researcher Name': u'Matt Turner'}]


Upload Data and Generate and Insert Metadata
````````````````````````````````````````````

The first step is to upload the data to the virtual watershed for which we'll be
making and inserting metadata. The VWDE returns an HTTP error if we
try to insert metadata for which no data exists.

.. code-block:: python

    # upload file to VWDE
    upl_res = vw_client.upload(new_mr_uuid, 'in.0000')

    print res  # <Response [200]>
    print res.text  # u'OK'
  

Next, we need to generate some metadata for this record, and we could use 
``make_watershed_metadata``, but instead we will use the higher-level 
``metadata_from_file`` function.

.. code-block:: python
    
    input_file = 'in.0000'
    parent_uuid = new_mr_uuid
    description = 'isnobal input #1'
    watershed_name = 'Dry Creek'
    state = 'Idaho'
    start_datetime = '2010-01-01 00:00:00'
    end_datetime = '2010-01-01 01:00:00'
    model_name = 'isnobal'

    # create XML FGDC-standard metadata that gets included in VW metadata
    fgdc_metadata = make_fgdc_metadata(input_file, None, new_mr_uuid,
        start_datetime, end_datetime, model=model_name)

    # create VW metadata
    watershed_metadata = metadata_from_file(input_file, parent_uuid,
        new_mr_uuid, description, watershed_name, state,
        start_datetime=start_datetime, end_datetime=end_datetime,
        model_name=model_name, fgdc_metadata=fgdc_metadata)


Now when you ``print watershed_metadata``, you will see something that looks
like the first record we pulled out after we made our first dataset query.

Next we insert the metadata we just created, making use of our ``vw_client``.
If you get a weird error message, try re-connecting as shown in the very first
steps.


Upload

.. code-block:: python

    response = vw_client.insert_metadata(watershed_metadata)
    assert response.status_code = 200, "Code not 200, Insert failed!"


And if the insert succeeded, ``response.text`` is a new UUID, which is the dataset UUID. It's
possible to insert the same metadata record multiple times, which may be a bug,
but either way it will stay that way for a while. A new metadata record will be
created every time even if you insert the exact same ``watershed_metadata``.

Now, assuming you've only ran the above command once, you can see the record you
just inserted by

.. code-block:: python

    res = vw_client.dataset_search(model_run_uuid=new_mr_uuid)
    assert res.total == 1

    print res[0]
    
If you insert a geotiff, ``metadata_from_file`` detects it as ready for visualization, and
marks the metadata as such by setting ``'model_set_type': 'vis'``. OGC web
services WMS and WCS will also be enabled.

To try this, download this geotiff from the virtual watershed: 
``http://vwp-dev.unm.edu/apps/vwp/datasets/8561e37b-6236-4156-9347-cce7582260cf/in.0008.I_lw.tif.original.tif``
and extract and move the tiff to your current working directory. This file is 
a geotiff of long-wave input radiation for the ninth time step of an iSNOBAL
model run.

Now everything else is the same, except input_file. First we'll upload our 
new tif file and then create metadata and insert that.

.. code-block:: python

    input_file = 'in.0008.I_lw.tif'
    # the ninth time step starts at 8:00 AM for this data 
    start_datetime = '2010-01-01 08:00:00'
    end_datetime = '2010-01-01 09:00:00'

    upl_res = vw_client.upload(new_mr_uuid, input_file)
    assert upl_res.status_code == 200, "Error on upload!"

    description = 'isnobal I_lw geotiff #9'

    fgdc_metadata = make_fgdc_metadata(input_file, parent_uuid, 
        start_datetime=start_datetime, end_datetime=end_datetime,
        model=model_name)

    watershed_metadata = metadata_from_file(input_file, parent_uuid,
        new_mr_uuid, description, watershed_name, state,
        start_datetime=start_datetime, end_datetime=end_datetime,
        model_name=model_name, fgdc_metadata=fgdc_metadata)

    vw_client.insert_metadata(watershed_metadata)

Now you can search for visualization-enabled datasets for the model run we've
created here like so:

.. code-block:: python

    res = vw_client.dataset_search(model_set_type='vis', model_run_uuid=new_mr_uuid)
    assert res.total == 1, "There are either zero or more than expected results!"

When you view the single record using

.. code-block:: python

    print res.records[0]

look for the WCS and WMS blocks, which you can print like so

.. code-block:: python

    print res.records[0]['services']

which will show

:: 

    {u'wms': u'http://vwp-dev.unm.edu/apps/vwp/datasets/687189e1-a2f4-4fce-8d46-da5589aea70c/services/ogc/wms?SERVICE=wms&REQUEST=GetCapabilities&VERSION=1.1.1'},
    {u'wcs': u'http://vwp-dev.unm.edu/apps/vwp/datasets/687189e1-a2f4-4fce-8d46-da5589aea70c/services/ogc/wcs?SERVICE=wcs&REQUEST=GetCapabilities&VERSION=1.1.2'}]

You can load either of these into ArcGIS or QGIS and visualize the dataset
you've just uploaded.

.. note::

    There is a function called ``upsert`` that works on directories as well as
    files to upload data and generate and insert associated metadata. It works
    only for properly-formatted iSNOBAL inputs and outputs. It may simply be
    removed or just heavily refactored in the future.


Advanced Model Run Tracking using Parent Model Runs
```````````````````````````````````````````````````

Above, we set ``parent_uuid = new_mr_uuid``. However, what if, for example, 
some data is derived from another set of data. More specifically, consider the
case where we modify observed data to see what the sensitivity of a model is
with respect to certain variables. Then the modified data could be seen as a 
"child" set of data. In this case, the modified data's ``parent_model_run_uuid``
would be the observed data's ``model_run_uuid``. 

This allows us to better discover data by its "lineage".

Delete a Model Run
------------------

Unfortunately, there is no way to run the VWDE locally, so all testing must be
done against the shared development system. This means that the sample data and
metadata that we've pushed to the server is just sitting there never to be used
again. In this case, we need to delete our model run. We would also want to do
this if, for example, a process failed after writing partial data to the VWDE.

.. code-block:: python

    # remove all data and the model run entry that we've created
    vw_client.delete_model_run(new_mr_uuid)

    # prove that nothing is left
    new_mr_entry = [r for r in vw_client.modelrun_search().records if r['Model Run UUID'] == new_mr_uuid]

    assert len(new_mr_entry) == 0
    assert vw_client.dataset_search(model_run_uuid=new_mr_uuid).total == 0



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

