import re

# csv columns for custom csv scheme
COLUMN_DOMAIN = 0
COLUMN_RESPONSABLE = 1
COLUMN_REDIRECT = 2
COLUMN_RESSOURCE = 3
COLUMN_COUNT = 4
COLUMN_XENUCOUNT = 5
COLUMN_CHANNEL = 6
COLUMN_SOURCE1 = 7 
COLUMN_SOURCE2 = 8 
COLUMN_SOURCE3 = 9 
COLUMN_SOURCE4 = 10 
COLUMN_SOURCE5 = 11 
COLUMN_SOURCE6 = 12 
COLUMN_SOURCE7 = 13 
COLUMN_SOURCE8 = 14 
COLUMN_SOURCE9 = 15
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

    # header for destination file

    destination_file.write("Domain;Verantwortlich;Redirect;Fehlende URL;Serverlog-Haeufigkeit;Xenu-Haeufigkeit;Channel;Quell-URLs\n")

    # header for refined output file

    final_file.write("Domain;Verantwortlich;Redirect;Fehlende URL;Serverlog-Haeufigkeit;Xenu-Haeufigkeit;Channel;Quell-URLs\n")

    with open(filename) as source_file:

        lines = source_file.readlines()
        # remove column labels
        lines.pop(0)
        # remove invalid line 
        lines.pop(294)

        for line in lines:

            line = line.replace('\r\n',';;;;;;;;')
            line = line.replace('\n',';;;;;;;;')

            # print(line)
            # Achtung: Hier sind noch alle Werte fuer Sources da!

            columns = line.split(';')
            # print(columns)

            domain = columns[COLUMN_DOMAIN]
            # print(domain)

            # Falls "media/lhm/_de/rubriken/Rathaus/por/stellenangebote" in ressource: -> "Redirect" = "http://www.muenchen.de/leben/job.html" 
            if "media/lhm/_de/rubriken/Rathaus/por/stellenangebote" in columns[COLUMN_RESSOURCE]:          
                columns[COLUMN_REDIRECT] = "http://www.muenchen.de/leben/job.html"

            # Falls "Channel" == "media" oder "Channel" == ".resources" -> "Verantwortlich" = "Redirect"

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

            # alle Bilddateien in media/lhm -> "Verantwortlich" = "Gernhaeuser"   
            if (("media/lhm" in columns[COLUMN_RESSOURCE]) and (".jpeg" in columns[COLUMN_RESSOURCE] or ".jpg" in columns[COLUMN_RESSOURCE] or ".png" in columns[COLUMN_RESSOURCE] or ".gif" in columns[COLUMN_RESSOURCE] or ".bmp" in columns[COLUMN_RESSOURCE])):
                columns[COLUMN_RESPONSABLE] = "Gernhaeuser"

            # alle Bilddateien in /media -> "Verantwortlich" = "Redirect" nur bei "Serverlog-Haeufigkeit" >= 500, sonst "Verantwortlich" = "Offen"
            if ((columns[COLUMN_CHANNEL] == "media") and (".jpeg" in columns[COLUMN_RESSOURCE] or ".jpg" in columns[COLUMN_RESSOURCE] or ".png" in columns[COLUMN_RESSOURCE] or ".gif" in columns[COLUMN_RESSOURCE] or ".bmp" in columns[COLUMN_RESSOURCE])): 
                if (int(columns[COLUMN_COUNT]) <= 500): 
                    columns[COLUMN_RESPONSABLE] = "Offen"

            redirect = columns[COLUMN_REDIRECT]

            ressource = columns[COLUMN_RESSOURCE]

            count = columns[COLUMN_COUNT]

            xenucount = columns[COLUMN_XENUCOUNT]

            channel = columns[COLUMN_CHANNEL]
            
            source1 = columns[COLUMN_SOURCE1]

            source2 = columns[COLUMN_SOURCE2]

            source3 = columns[COLUMN_SOURCE3]

            source4 = columns[COLUMN_SOURCE4]

            source5 = columns[COLUMN_SOURCE5]

            source6 = columns[COLUMN_SOURCE6]

            source7 = columns[COLUMN_SOURCE7]

            source8 = columns[COLUMN_SOURCE8]

            source9 = columns[COLUMN_SOURCE9]

            if ((not(re.search("muenchen.de", source1))) and (source1 != "") and (source1 != " ")): 
                columns[COLUMN_RESPONSABLE] = "Mailaufforderung"
            #    print(source1)

            # if ((not(re.search("muenchen.de", source2))) and (source2 != "") and (source2 != " ")): 
            #     columns[COLUMN_RESPONSABLE] = "Mailaufforderung"
            #     print("external source2 found")


            verantwortlich = columns[COLUMN_RESPONSABLE]

            csv_line = DELIMITER.join([domain, verantwortlich, redirect, ressource, count, xenucount, channel, source1, source2, source3, source4, source5, source6, source7, source8, source9]) + EOL
            
            # print(csv_line)

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

# csv_modify("./evaluation_temporary.csv","./evaluation.csv","./evaluation_refined.csv")


    