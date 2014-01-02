import csv_scheme as CSV

##
# XEN Exported Map
#
# MAPPING
#
#	CSV
# 	SOURCE: Referer := Ressource die eine andere Ressource anfordert (intern oder extern)
# 	RESSOURCE: URL := Ressource die nicht gefunden wurde (intern)
#
# 	XEN
# 	SOURCE: OriginPage := Ressource die eine andere Ressource anfordert (intern)
# 	RESSOURCE: LinkToPage := Ressource die nicht gefunden wurde NOT (intern oder extern) SKIPPED EXTERNAL, thus (intern)
#
# 	=> Referer ~ OriginPage
# 	=> URL ~ LinkToPage
##

# xen columns for custom csv scheme
COLUMN_SOURCE = 0
COLUMN_RESSOURCE = 1
COLUMN_STATUS = 2


##
# Returns the first line split by tabs
# result:
# 	['OriginPage', 'LinkToPage', 'LinkToPageStatus', 'LinkToPageTitle', 'OriginPageDate', 'OriginPageTitle\r\n']
#
def xenGetColumnNames(source):

	with open(source) as source_file:
		for line in source_file:
			return line.split('\t')


##
# Filters entries by status codes and stores the result as semi-colon
# separated csv
#
# @param String source          source file name and path
# @param String destination     destination file name and path
# @param List valid_status      list of valid status codes
def xenFilter(source, destination, valid_status, mode="w"):
	print('start filtering ' + source + ' ...')

	current_line = 0
	destination_file = open(destination, mode)
	with open(source) as source_file:
		for line in source_file:

			columns = line.split('\t')
			if (columns[COLUMN_STATUS] in valid_status):

				current_line += 1
				# convert columns to csv scheme
				csv_line = CSV.get_line("1", columns[COLUMN_SOURCE], columns[COLUMN_RESSOURCE], CSV.LOCATION.INTERN, CSV.LOCATION.INTERN)
				destination_file.write(csv_line)

	source_file.close()
	destination_file.close()

	print(str(current_line) + ' lines filtered to ' + destination)


##
# print all available status codes within the given file
#
# results:
#   status: skip external
#   status: ok
#   status:   info@vogelpfeifer.de
#   status: server error
#   status: forbidden request
#   status: not found
#   status: the resource is no longer available
#   status: timeout
#   status: user skip
#   status: LinkToPageStatus
def print_status_codes(source_file):

	found_status_codes = {}

	with open(source_file) as source:
		for line in source:

			columns = line.split('\t')
			status = columns[COLUMN_STATUS]
			#if (found_status_codes.get(status, None) is None):
			#    found_status_codes[status] = True
			found_status_codes[status] = True

	for status in found_status_codes:
		print('status: ' + status)
