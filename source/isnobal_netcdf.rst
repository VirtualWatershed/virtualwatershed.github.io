(iSNOBAL) modeling with NetCDF
============================

As we integrate more models into the virtual watershed, it's good to look at the
one model that has been pretty well integrated with virtual watershed
technologies: iSNOBAL. In order to run this you'll have to have the 
IPW library, which can either be cloned from GitHub for Linux: 
https://github.com/tri-state-epscor/water-ipw (please get in touch if you can't
access the page, it's private) or downloaded here with precompiled binaries for 
OS X: :download:`ipw-2.1.0.tar.gz <downloads/ipw-2.1.0.tar.gz>`.

I've created a model run and dataset on the virtual watershed for this tutorial
by running the following commands:

.. code-block:: python

    from wcwave_adaptors import (default_vw_connection, isnobal,
        make_fgdc_metadata, metadata_from_file)

    vwc = default_vw_connection()
    modelrun_uu = vwc.initialize_modelrun(
        model_run_name='Two weeks of input for iSNOBAL tutorial',
        description='tutorial input data', 
        researcher_name='Matt Turner', 
        keywords='isnobal, netcdf')

    file_path = 'twoweek_inputs_with_zlib.nc'

    # can check that upl_res.status_code == 200 and upl_res.text == 'OK'
    upl_res = vwc.upload(modelrun_uu, file_path)
    # set required metadata fields for the FGDC "science" metadata
    config = None  # sets config to be loaded from default.conf
    start_datetime = '2010-01-01 00:00:00'
    end_datetime = '2010-01-08 00:00:00'
    model_name = 'isnobal'

    fgdc_metadata = make_fgdc_metadata(file_path, config, modelrun_uu,
                                       start_datetime, end_datetime,
                                       model_name='isnobal')
    # data from ftp://icewater.boisestate.edu/boisefront-products/other/projects/Kormos_iSNOBAL/
    watershed_name = 'Dry Creek'
    state = 'Idaho'
    desc = 'netCDF with roughly two weeks (400 hours) of input data ready for an isnobal run'

    watershed_md = \
        metadata_from_file(file_path, modelrun_uu, modelrun_uu, desc,
            watershed_name, state, start_datetime=start_datetime,
            end_datetime=end_datetime, model_name=model_name,
            fgdc_metadata=fgdc_metadata, model_set='inputs', 
            taxonomy='geoimage', model_set_taxonomy='grid')

    insert_res = vwc.insert_metadata(watershed_md)

    file_uu = insert_res.text


Now we're going to show how to download that data and run iSNOBAL. We'll need
file_uu from the steps above.

.. code-block:: python

    import netCDF4

    # use the file_uu from before to find the dataset record we need
    input_records = vwc.dataset_search(uuid=uu).records

    assert len(input_records) == 1, "there should be only one unique record"

    input_record = input_records.pop()

    dl_url = input_record['downloads'][0]['nc']

    input_path = 'two-weeks-input.nc'
    vwc.download(dl_url, input_path)

    input_nc = netCDF4.Dataset(input_path)

    output_path = 'two-weeks-output.nc'
    # capture netcdf Dataset output for other processing
    nc_out = isnobal(input_nc, output_path)  # saves output nc to output_path
    nc_out.close()  # if no processing to be done, close the file

    # now upload the output to the modelrun_uu from before
    vwc.upload(modelrun_uu, output_path)

    # need to build the metadata again for the outputs
    # use a lot of the same values from before
    fgdc_md = make_fgdc_metadata(output_path, config, modelrun_uu,
        start_datetime, end_datetime, model_name='isnobal')

    desc = 'outputs from two weeks of Dry Creek data isnobal run'
    watershed_md = \
        metadata_from_file(output_path, modelrun_uu, modelrun_uu, desc,
            watershed_name, state, start_datetime=start_datetime,
            end_datetime=end_datetime, model_name=model_name,
            fgdc_metadata=fgdc_metadata, model_set='outputs', 
            taxonomy='geoimage', model_set_taxonomy='grid')

    insert_res = vwc.insert_metadata(watershed_md)


And in that way we can run iSNOBAL using data from the Virtual Watershed and
push our outputs back to the Virtual Watershed.
