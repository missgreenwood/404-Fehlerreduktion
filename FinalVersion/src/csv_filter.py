import csv_scheme as CSV


# csv columns for custom csv scheme
COLUMN_RESSSOURCE_ERRORS = 0
COLUMN_RESSOURCE = 1
COLUMN_SOURCE = 2

##
# Cleans the given CSV File and stores the result to the given file
#
# @param String filename      csv source file
# @param String destination target file for results
def csvFilter(filename, destination, mode="w"):

    destination_file = open(destination, mode)
    with open(filename) as source_file:

        lines = source_file.readlines()
        # remove column labels
        lines.pop(0)

        for line in lines:

            line = line.replace('\r\n', '')
            line = line.replace('\n', '')

            columns = line.split(';')

            count = columns[COLUMN_RESSSOURCE_ERRORS]
            count = count[1:-1]

            source = columns[COLUMN_SOURCE]
            source = source[1:-1]

            ressource = columns[COLUMN_RESSOURCE]
            ressource = ressource[1:-1]

            # fix to consistent url
            if (ressource[0] == '/'):
                # !check: immer muenchen oder auch subdomains? wzb. s0.portal.muenchen.de etc
                ressource = 'http://www.muenchen.de' + ressource

            csv_line = CSV.get_line(count, source, ressource, CSV.LOCATION.BOTH, CSV.LOCATION.INTERN)
            destination_file.write(csv_line)

    source_file.close()
    destination_file.close()
    print(filename + ' converted and saved to ' + destination)
