# NGLess scripts

Note that the results of running this benchmark are provided in
`data/precomputed`.

## Running MOCAT benchmark

You must have [jug](http://jug.rtfd.io) and [MOCAT2](http://mocat.embl.de)
installed and have run the `download-data.py` script at the top level of this
repository.

Then execute:

    jug execute

will generate the file `ngless_benchmark.csv` with the results. Note that this
will produce very large intermediate files (several 100s of GiB) and require
ca. 64 GiB of RAM.

The files `gut.ngl` and `ocean.ngl` contain the full pipelines. The variations
with names such as `gut0-rtf.ngl` contain parts of the processing. The only
purpose of splitting the pipeline into its constituent parts is to facilitate
benchmarking. Splitting the pipeline into its constituent blocks is also why it
generates such large outputs as it saves all the intermediate results.



