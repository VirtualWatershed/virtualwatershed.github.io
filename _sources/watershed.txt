.. Documentation for the vw_adaptor module
.. _watershed-main:

Virtual Watershed Adaptor
=========================

These tools help the user connect to the Virtual Watershed Data API. For more
information, see the Data API docs at http://vwp-dev.unm.edu/docs/index.html.

VWClient: User Interface to the Virtual Watershed
`````````````````````````````````````````````````

The ``VWClient`` performs several routine virtual watershed functions. The
first, performed in the constructor, is for authentication. 
There two ``search`` methods, ``dataset_search`` and ``modelrun_search``. 
There are obvious ``download`` and ``upload`` functions. To create a model run,
this class provides the ``initialize_modelrun`` method.
An ``insert_metadata`` function pushes JSON watershed metadata to the
database. For deleteing model runs, use ``delete_modelrun``.

.. autoclass:: wcwave_adaptors.wcwave_adaptors.watershed.VWClient
    :members:

Typically there will be no need to directly use the constructor to create a new
``VWClient`` instance. Instead use this convenience function that will read
``default.conf`` and establish a connection with 

.. autofunction:: wcwave_adaptors.wcwave_adaptors.watershed.default_vw_client


VW Client Examples
------------------

Assuming you have properly filled out your ``default.conf`` file with the 
IP address of the watershed and your login information, you can do the 
following.

.. code-block:: python

    from wcwave_adaptors import default_vw_client

    vw_client = default_vw_client()

    # get the first model_run_uuid returned from the model run search
    model_run_uuid = vw_client.modelrun_search().records[0]['Model Run UUID']

    # get a QueryResult that contains the total records, subtotal returned
    # with the query, and a list of the records themselves
    result = vwClient.dataset_search(model_run_uuid=modelRunUUID)
    total_records_available = result.total
    records_returned_this_query = result.subtotal
    records_themselves = result.records
    assert len(records_themselves) == records_returned_this_query

The default number of results fetched (enforced by the watershed) is 15, so to 
get 30, use the ``limit`` keyword, for example

.. code-block:: python

    thirty = vwClient.dataset_search(model_run_uuid=model_run_uuid, limit=30)

When using the ``VWClient.dataset_search`` function, you can specify any of the 
key/value pairs specified in the `virtual watershed documentation 
<http://vwp-dev.unm.edu/docs/stable/search.html#search-objects>`_.

The search function returns a ``QueryResult`` instance.

.. autoclass:: wcwave_adaptors.wcwave_adaptors.watershed.QueryResult
    :members:


Metadata builders
`````````````````

There are two functions for building metadata. One for creating JSON-formatted
Virtual Watershed metadata and one for generating XML-formatted FGDC "science"
metadata. The templates used to implement these functions are stored in the
``resources/`` directory.

.. autofunction:: wcwave_adaptors.wcwave_adaptors.watershed.make_watershed_metadata

.. autofunction:: wcwave_adaptors.wcwave_adaptors.watershed.make_fgdc_metadata


Example using metadata builders and the VW Client
`````````````````````````````````````````````````

Here we upload a file stored at ``'data/in.0001'`` to the virtual watershed 
and create the appropriate metadata for it. We pretend the variable names
that are represented in this file are ``R_n,H,L_v_E,G,M,delta_Q``, they are
input files. This is the procedure for inserting a brand-new, parent-free
model run set of data. Soon the "initial insert" section of this will be 
automated.

Get a VW Client connection (will soon be done during initialization)
--------------------------------------------------------------------

>>> vw_client = default_vw_client(configFile) # gets connection info from file

Initialize a new model run
--------------------------

.. code-block:: python

    new_uuid = vw_client.initialize_model_run(model_run_name='iSNOBAL for Water
        Year 2010', description='input and output files for observed data for
        water year 2010', researcher_name='Matt Turner',
        keywords='isnobal,idaho')


Upload File
-----------

.. code-block:: python

    data_file = "src/test/data/in.0001"
    vw_client.upload(new_uuid, data_file)


Build metadata
--------------

.. code-block:: python

    start_datetime = '2010-01-01 01:00:00'
    end_datetime = '2010-01-01 02:00:00'

    upl_res = vw_client.upload(new_uuid, input_file)
    assert upl_res.status_code == 200, "Error on upload!"

    # now description refers to an individual metadata record
    description = 'isnobal I_lw geotiff #2'

    fgdc_metadata = make_fgdc_metadata(data_file, parent_uuid,
        start_datetime=start_datetime, end_datetime=end_datetime,
        model=model_name)

    watershed_metadata = metadata_from_file(data_file, parent_uuid,
        new_uuid, description, watershed_name, state,
        start_datetime=start_datetime, end_datetime=end_datetime,
        model_name=model_name, fgdc_metadata=fgdc_metadata)

Insert Metadata
---------------

.. code-block:: python

    vw_client.insert_metadata(watershed_metadata)

Make Watershed Metadata
```````````````````````

We could have used the ``make_watershed_metadata`` function, but
``metadata_from_file`` helps us out, especially when inserting geotiffs and
iSNOBAL binaries, which it knows about and automatically creates appropriate
metadata in these cases. 

.. autofunction:: wcwave_adaptors.wcwave_adaptors.watershed.metadata_from_file


Upsert
-------

.. warning::

    This works, but may soon be deprecated and will likely not be supported any
    more.
I wrote out all of the previous steps to show what is possible with the 
watershed. The function that puts this all together, though, is the ``upsert``
function, which allows the user to upload and insert either a single file or a
whole directory to the virtual watershed

.. _upsert-ref:

.. autofunction:: wcwave_adaptors.wcwave_adaptors.watershed.upsert


