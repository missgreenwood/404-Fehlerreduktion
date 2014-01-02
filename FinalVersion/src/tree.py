import re
import color
import csv_scheme as CSV

INFO = '__INFO__'
COUNT = 'count'
URL = 'url'
XEN_COUNT = 'xen_count'
REFERENCE = 'sources'
## EVALUATION ??
#
# Programmierfehler
#   null
#   + askdasd +
#
# oder Hack
#   javascript:window.print()
#


##
# Returns the domain hierarchy of the given csv
#
# @param String source_file     CSV file in correct scheme
# @param Integer column_index   Index of column to use as url
# @param Integer weight_index   Index of column to use for weight (optional)
def create_from_csv(source_file, column_index, reference_index, weight_index=False, result={}):

    with open(source_file) as source:
        for line in source:

            columns = CSV.get_columns(line)
            domain_string = columns[column_index]
            reference = columns[reference_index]

            if (weight_index is not False):
                weight = int(columns[weight_index])
                add_url(result, domain_string, reference, weight)

            else:
                add_url(result, domain_string, reference)

    return result


##
# inserts url as folders into tree
#
# @param Dictionary tree    url hierachy
# @param String url         url to add
# @param Integer weight     weight of node (optional)
def add_url(tree, url, reference, weight=1):

    # url = url.replace('\n', '')
    # remove protocol
    url = re.sub(r'https?://', '', url)
    # remove multiple /
    url = re.sub(r'//+', '/', url)
    # remove trailing /
    if (url[-1] == "/"):
        url = url[:-1]

    folders = url.split('/')
    add_folders(tree, url, folders, reference, weight)


##
# inserts folders into dictionary and count occurences
#
# @param Dictionary tree    url hierarchiy
# @param Array folders      url folders to insert
# @param Integer weight     weight of url (optional)
def add_folders(tree, url, folders, reference, weight=1):

    current = tree

    # and insert into hierarchy
    for folder in folders:

        found = current.get(folder, None)

        if (found is None):

            # first folder, add a new dictionary
            current[folder] = {}
            # store as new current
            current = current[folder]
            # and add info data
            current[INFO] = {}
            current[INFO][COUNT] = weight

        else:
            # store as new current
            current = found
            # increase count
            current[INFO][COUNT] += weight

    leaf_url = current[INFO].get(URL, None)
    if (leaf_url is None):
        current[INFO][URL] = url

    if (reference is not '-'):

        references = current[INFO].get(REFERENCE, None)
        if (references is None):
            current[INFO][REFERENCE] = []
            references = current[INFO].get(REFERENCE, None)
        references.append(reference)


##
# Executes a callback on each leaf of the tree
#
# @param Dictionary tree    url hierarchy
# @param Function callback  callback function, receiving [folder:String, info:Dictionary] as arguments
def on_leaf(tree, callback):

    for folder in tree:
        if (folder != INFO):
            # last node = file
            if (len(tree[folder]) == 1):
                callback(folder, tree[folder][INFO])
            else:
                on_leaf(tree[folder], callback)


##
# Copies and info value
#
# @param Dictionary tree    url hierarchy
# @param String source      info field to copy
# @param String destination new info field (copy)
def leaf_copy_info_value(tree, source, destination):

    def callback(folder, info):
        info[destination] = info[source]

    on_leaf(tree, callback)


##
# STEP 1
# Exports the given tree as Nik-CSV
#
# DEPTH(0) = domain; URL = Fehlende URL; COUNT = Haufigkeit; XENU_COUNT = Xenu-Haufigkeit; DEPTHS(1) = Verantwortlich; REFERENCE = Quell-URL
# -> DEPTH(1): nur falls nicht leaf, sonst: domain?
def export_as_csv(tree, destination_file):

    f = open(destination_file, "w")
    #csv = [domain, url, count, xenu_count, verantwortlichkeit, references]
    csv = ["Domain", "Fehlende URL", "Haufigkeit", "Xenu-Haufigkeit", "Verantwortlich", "Quell-URL"]
    line = ";".join(csv) + CSV.EOL
    f.write(line)

    for domain in tree:
        if (domain is not INFO):
            export_domain_as_csv(domain, tree[domain], f)

    # f.close()


##
# STEP 2
def export_domain_as_csv(domain, tree, f):

    verantwortlichkeit = domain

    # verantwortlichkeit = folder
    for folder in tree:

        if (folder is not INFO):
            if (len(tree[folder]) != 1):
                verantwortlichkeit = folder

            export_info_as_csv(tree[folder], domain, verantwortlichkeit, f)


##
# LAST STEPS
#
def export_info_as_csv(tree, domain, verantwortlichkeit, f):

    for folder in tree:
        if (folder is not INFO):
            if (len(tree[folder]) == 1):
                write_line(tree[folder][INFO], domain, verantwortlichkeit, f)
            else:
                export_info_as_csv(tree[folder], domain, verantwortlichkeit, f)


##
# Writes the info to line
def write_line(info, domain, verantwortlichkeit, f):

    url = info.get(URL, "ERROR")
    count = str(info.get(COUNT, 0))
    xenu_count = str(info.get(XEN_COUNT, 0))

    references = info.get(REFERENCE, [])
    # remove duplicates
    references = set(references)
    # add in separate columns
    references = ';'.join(references)

    csv = [domain, url, count, xenu_count, verantwortlichkeit, references]
    line = ';'.join(csv) + CSV.EOL
    f.write(line)


##
# logs contents of domain_hierarchy to console
#
# @param dict   data    domain_hierarchy or sub dictionary
# @param int    deep    how many nested folders to print
# @param string indent  current indentation (whitespaces)
def verbose(tree, deep=-1, indent=""):

    for folder in tree:

        if (folder != INFO):

            # last node = file
            # if (len(tree[folder]) == 1):
            #     print(tree[folder][INFO])
                # references = tree[folder][INFO].get(REFERENCE, None)
                # if (references is not None):
                #     print(references)

            print(indent + color.colored_string(str(tree[folder][INFO][COUNT]), 'RED') + ' ' + folder)

            if (deep != 0):
                verbose(tree[folder], deep - 1, indent + "  ")


##
# log files only
#
# @param Dictionary tree    url hierarchy
# @param Array ignore       filetypes to ignore (optional)
#
def verbose_last(tree, ignore=['htm', 'html', 'php', 'jpg', 'jpeg', 'pdf', 'png', 'css', 'js', 'ttf', 'wof', 'svg', 'gif']):

    def callback(folder, info):
        filetype = folder.split('.').pop()
        if (not filetype in ignore):
            print(folder, info)

    on_leaf(tree, callback)
