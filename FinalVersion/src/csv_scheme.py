# CSV SCHEME


##
# Returns an enum datatype
# from http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
#
# Usage:
#   Numbers = enum(ONE=1, TWO=2, THREE='three')
#   Numers.ONE
#   >> 1
#   Numbers.reverse_mapping['three']
#   >> THREE
#
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

# line end
EOL = '\n'
# column delimiter
DELIMITER = '\t'
# source location, if both: may be intern or extern
LOCATION = enum(BOTH="0", INTERN="1", EXTERN="2")
# columns in working csv file
# [RESSSOURCE_ERRORS, SOURCE, RESSOURCE, SOURCE_LOCATION, RESSOURCE_LOCATION]
COLUMNS = enum(RESSSOURCE_ERRORS=0, SOURCE=1, RESSOURCE=2, SOURCE_LOCATION=3, RESSOURCE_LOCATION=4)


def get_columns(line):
    return line.split(DELIMITER)


# return columns as line matching scheme
def get_line(ressource_errors, source_url, ressource_url, source_location=0, ressource_location=0):
    # SCHEME
    return DELIMITER.join([ressource_errors, source_url, ressource_url, source_location, ressource_location]) + EOL
