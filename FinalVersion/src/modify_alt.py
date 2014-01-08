import csv_scheme as CSV


# csv columns for custom csv scheme
COLUMN_DOMAIN = 0
COLUMN_RESPONSABLE = 1
COLUMN_REDIRECT = 2
COLUMN_RESSOURCE = 3
COLUMN_COUNT = 4
COLUMN_XENUCOUNT = 5
COLUMN_CHANNEL = 6
COLUMN_SOURCES = 7
DELIMITER = ";"
EOL = "\n"

##
# Stores the temporary result csv file to the final csv result file 
#
# @param String filename    temporary csv result file
# @param String destination final csv result file
def csv_modify(filename, destination, final, mode="w"):

    destination_file = open(destination, mode)

    final_file = open(final, mode)

    with open(filename) as source_file:

        lines = source_file.readlines()
        # remove column labels
        lines.pop(0)
        # remove invalid line 
        lines.pop(294)

        for line in lines:

            line = line.replace('\r\n', '')
            line = line.replace('\n', '')

            columns = line.split(';')

            domain = columns[COLUMN_DOMAIN]

            if (columns[COLUMN_CHANNEL] == "media" or columns[COLUMN_CHANNEL] == ".resources"): 
                columns[COLUMN_RESPONSABLE] = "Redirect"
            elif (columns[COLUMN_CHANNEL] == "veranstaltungen"): 
                columns[COLUMN_RESPONSABLE] = "Redaktion"
            elif (columns[COLUMN_CHANNEL] == "rathaus"): 
                columns[COLUMN_RESPONSABLE] = "Gernhaeuser"
            elif (columns[COLUMN_CHANNEL] == "media-static"): 
                columns[COLUMN_RESPONSABLE] = "Technik"
            elif (columns[COLUMN_CHANNEL] == "mhp"): 
                columns[COLUMN_RESPONSABLE] = "Branchenbuch"
            else: 
                columns[COLUMN_RESPONSABLE] = "Offen"

            verantwortlich = columns[COLUMN_RESPONSABLE]

            redirect = columns[COLUMN_REDIRECT]

            ressource = columns[COLUMN_RESSOURCE]

            count = columns[COLUMN_COUNT]

            xenucount = columns[COLUMN_XENUCOUNT]

            channel = columns[COLUMN_CHANNEL]
            
            sources = columns[COLUMN_SOURCES]

            csv_line = DELIMITER.join([domain, verantwortlich, redirect, ressource, count, xenucount, channel, sources]) + EOL
            
            destination_file.write(csv_line)

            # define new criterion for refined output 

            new_value = int(columns[COLUMN_COUNT])

            # print lines that match new criterion to refined output file 

            if (int(columns[COLUMN_COUNT]) >= 100): 
                final_file.write(csv_line)

    source_file.close()
    destination_file.close()
    final_file.close()
    print(filename + ' converted and saved to ' + destination)
    print(destination + ' converted and saved to ' + final)


   


    