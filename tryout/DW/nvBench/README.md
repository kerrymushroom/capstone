# Usage:

This work is to replicate and compare nvBench article results with our research

For complete data of nvBench article, please check [nvBench](https://github.com/TsinghuaDatabaseGroup/nvBench) repository.

Y. Luo, J. Tang, and G. Li, ‘‘NvBench: A large-scale synthesized dataset for cross-domain natural language to visualization task,’’ 2021, arXiv:2112.12926.

# Why newNVBench.json and how to use 

The original NVBench.json describes NVBench item Properties, Queries and Visualization data, but misses corresponding html id info and not contain standard Vegalite Vis Object format, hence newNVBench.json is presented for query search and visualization replication.

You could search the html id using query like "What is the trend of oil production since 2004" and find the corresponding html "VIS_6.html" in [nvBench vegalite folder](https://github.com/TsinghuaDatabaseGroup/nvBench/tree/main/nvBench_VegaLite). 

You could also obtain vegalite vis object to visualize yourself at jupyter notebook using `display({'application/vnd.vega.v5+json': yourVisObject}, raw=True)` 