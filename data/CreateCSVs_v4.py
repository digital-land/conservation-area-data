#!/usr/bin/python3

# who            when           what
# Dave K Brown   27th Aug 2024  Created

import pandas as pd
import re
import os
import glob

delimiter = ':^:'
delimiter = '	'   # tab
delimiter = ','

root_dir = '/mnt/c/Users/DavidBrown/Documents/GIS/ExportCAs/'

organisation_lookup_file = root_dir + 'organisation_lookup.csv'
data_to_split_file       = root_dir + 'Missing Conservation Area List_edit.csv'
output_dir               = root_dir + 'Output'

df_organisation_lookup = pd.read_csv(organisation_lookup_file)
df_data_to_split       = pd.read_csv(data_to_split_file)

def short_organisation_lookup(LPA):
    org_index = df_organisation_lookup.index[df_organisation_lookup.name == LPA]
    #print(org_index.values)
    full_organisation_value = df_organisation_lookup["organisation"][org_index.values[0]]
    x = re.split(":", full_organisation_value)
    short_organisation_value = x[1]
    
    return short_organisation_value

def organisation_lookup(LPA):
    org_index = df_organisation_lookup.index[df_organisation_lookup.name == LPA]
    full_organisation_value = df_organisation_lookup["organisation"][org_index.values[0]]
    
    return full_organisation_value

def entity_lookup(LPA):
    org_index = df_organisation_lookup.index[df_organisation_lookup.name == LPA]
    entity = df_organisation_lookup["entity"][org_index.values[0]]

    return entity

def clear_output_dir():

    files = glob.glob(output_dir + '/*')
    for f in files:
        try:
           os.remove(f)
        except PermissionError:
           print("Close the file!")
           exit() 

print("Started")

df_organisation_lookup = pd.read_csv(organisation_lookup_file)
df_data_to_split       = pd.read_csv(data_to_split_file)

#print(entity_lookup('Allerdale Borough Council'), short_organisation_lookup('Allerdale Borough Council'))
#print(short_organisation_lookup("Amber Valley Borough Council"))
#print(short_organisation_lookup("Babergh District Council"))

#os.system('whoami')

clear_output_dir()

# Enter header rows to each output file
f_ca  = open(output_dir + "/conservation-area.csv", "a") 
line = 'reference'           + delimiter + \
       'name'                + delimiter + \
       'designation-date'    + delimiter + \
       'document-url'        + delimiter + \
       'documentation-url'   + delimiter + \
       'geometry'            + delimiter + \
       'point'               + delimiter + \
       'notes'               + delimiter + \
       'organisation'        + delimiter + \
       'entry_date'          + delimiter + \
       'start_date'          + delimiter + \
       'end_date'            + '\n' 

f_ca.write( line )

f_cad = open(output_dir + "/conservation-area-document.csv", "a") 
line = 'reference'           + delimiter + \
        'conservation-area'  + delimiter + \
        'name'               + delimiter + \
        'documentation-url'  + delimiter + \
        'document-url'       + delimiter + \
        'document-type'      + delimiter + \
        'notes'              + delimiter + \
        'organisation'       + delimiter + \
        'entry_date'         + delimiter + \
        'start_date'         + delimiter + \
        'end_date'           + '\n' 
f_cad.write( line )



last_lpa = ""
designation_date = '2023-12-25'
for row in df_data_to_split.head(180).itertuples(index=False):

    ActualMapURL      = False

    reference         = str(entity_lookup(row[0:9][0])) + "_" + short_organisation_lookup(row[0:9][0])
    name              = row[0:9][1]
    name              = '"' + name + '"'

    document_url      = row[0:9][3]
    if  document_url == 'nan' or document_url == '' or pd.isnull(document_url) or document_url == 'None':
        document_url = "No Appraisal document"
    
    document_url      = '"' + document_url + '"'
        



    documentation_url = '"' + row[0:9][2] + '"'
    



    geometry          = ""
    point             = ""
    notes             = str(row[0:9][6])
    organisation      = organisation_lookup(row[0:9][0])
    entry_date        = ""
    start_date        = ""
    end_date          = ""


    if notes == 'nan':
       notes = '' 

    extras            = row[0:9][4]
    if extras == 'N':
       pass
    elif extras == 'Y':
       notes = notes + 'Extra documents are available. '
    else:
       pass

    map = str(row[0:9][5])
    #print('>>>' + str(row[0:9][5]))
    #print('<<<' + map)
    #print('<<<' + map[0:4])

    if map[0:4] != 'http':
       if map[0:1] == 'P':
          notes = notes + 'Best Map is shown on page ' + map[1:] + ' of the appraisal document. '
       else:
          map = ""
    else:
       ActualMapURL = True


    notes             = '"' + notes + '"'

   #print(reference)
   #print(name)
   #print(document_url)
   #print(documentation_url)
   #print(geometry)
   #print(point)
   #print(notes)
   #print(organisation)
   #print(entry_date)
   #print(start_date)
   #print(end_date)
        
    if last_lpa != row[0:9][0]:
        # This is a new LPA
        CA_row_number = 1
        
        last_lpa = row[0:9][0]
    else:
        CA_row_number = CA_row_number + 1 

    line = reference + '_CA' + str(CA_row_number) + delimiter + \
           name                                   + delimiter + \
           designation_date                       + delimiter + \
           document_url                           + delimiter + \
           documentation_url                      + delimiter + \
           geometry                               + delimiter + \
           point                                  + delimiter + \
           notes                                  + delimiter + \
           organisation                           + delimiter + \
           entry_date                             + delimiter + \
           start_date                             + delimiter + \
           end_date                               + '\n'

    f_ca.write( line )
    #print(line) 

    # Hmm there may be more than one record here, an appraisal and a map
    # Does best map column F, ident 5, have a map in it?
    # If so we need to add another line for it

    line = 'D_' + reference + '_CA' + str(CA_row_number) + "_1" + delimiter + \
           reference + '_CA' + str(CA_row_number)        + delimiter + \
           name                                          + delimiter + \
           documentation_url                             + delimiter + \
           document_url                                  + delimiter + \
           'area-appraisal'                              + delimiter + \
           notes                                         + delimiter + \
           organisation                                  + delimiter + \
           entry_date                                    + delimiter + \
           start_date                                    + delimiter + \
           end_date                                      + '\n'

    f_cad.write( line )
    #print(line) 

    if ActualMapURL:

       line = 'D_' + reference + '_CA' + str(CA_row_number) + "_2" + delimiter + \
           reference + '_CA' + str(CA_row_number)        + delimiter + \
           name                                          + delimiter + \
           documentation_url                             + delimiter + \
           map                                           + delimiter + \
           'area-map'                                    + delimiter + \
           notes                                         + delimiter + \
           organisation                                  + delimiter + \
           entry_date                                    + delimiter + \
           start_date                                    + delimiter + \
           end_date                                      + '\n'

       f_cad.write( line )
       #print(line)

# Close the files
try:
    f_ca.close()
except:
    pass 

try:
    f_cad.close()
except:
    pass 

#cp /mnt/c/Users/DavidBrown/Documents/GIS/ExportCAs/Output/conservation-area.csv /var/lib/mysql-files/

print("Finished")


