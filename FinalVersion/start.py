##
# OVERVIEW
# create filtered XEN (map) by status
# parse XEN, CSV:
# create hierarchies (by source, by ressource)
# merge hierarchies
# "evaluate" (count entries, assign link to second hierarchy)
# export
##


import os
from src.xen_filter import xenFilter
from src.csv_filter import csvFilter
import src.csv_scheme as CSV
import src.tree as Tree

FILE_RESULT = "results/evaluation.csv"
FILE_XEN_SOURCE_MAP = "sources/XEN_20_broken_map.txt"
FILE_CSV_SOURCE = "sources/www.muenchen.de-2013-11.csv"

CLEAR_CACHE = False
FILE_DATA = "cache/data.csv"
FILE_DATA_XEN = "cache/xen.csv"
FILE_DATA_LOG = "cache/log.csv"

# Create source data file
# if (not os.path.exists(FILE_DATA) or CLEAR_CACHE is True):
#     # Create filtered XEN map, create new file
#     xenFilter(FILE_XEN_SOURCE_MAP, FILE_DATA, ["not found", "the resource is no longer available"])
#     # Create converted CSV and append
#     csvFilter(FILE_CSV_SOURCE, FILE_DATA, 'a')

# Create filtered XEN map
if (not os.path.exists(FILE_DATA_XEN) or CLEAR_CACHE is True):
    xenFilter(FILE_XEN_SOURCE_MAP, FILE_DATA_XEN, ["not found", "the resource is no longer available"])

# Clean and convert CSV file
if (not os.path.exists(FILE_DATA_LOG) or CLEAR_CACHE is True):
    csvFilter(FILE_CSV_SOURCE, FILE_DATA_LOG)

# First. Create hierarchy of xen file only
xen_tree = Tree.create_from_csv(FILE_DATA_XEN, CSV.COLUMNS.RESSOURCE, CSV.COLUMNS.SOURCE)
# and copy node weight on leafs as xen_count.
Tree.leaf_copy_info_value(xen_tree, Tree.COUNT, Tree.XEN_COUNT)
# Then extend tree with log data
domain_tree = Tree.create_from_csv(FILE_DATA_LOG, CSV.COLUMNS.RESSOURCE, CSV.COLUMNS.SOURCE, CSV.COLUMNS.RESSSOURCE_ERRORS, xen_tree)

# perform evaluation
# ...

#Tree.verbose(domain_tree, 1)

# save results
Tree.export_as_csv(domain_tree, FILE_RESULT)
print('done')
