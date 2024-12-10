#!/usr/bin/python3

# who            when           what
# Dave K Brown   27 Aug  2024  Created
# Dave K Brown    2 Sept 2024  Changed so that one file is created per LPA

# https://www.planning.data.gov.uk/dataset/conservation-area-document-type# https://www.planning.data.gov.uk/dataset/conservation-area-document-type# https://www.planning.data.gov.uk/dataset/conservation-area-document-type


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
data_to_split_file       = root_dir + 'Missing Conservation Area List 240909a.csv'
data_to_split_file       = root_dir + 'Input/ExistingConservationArea_Good3.csv'
data_to_split_file       = root_dir + 'Input/Existing_NoDups_NotLessThanZero.csv'
data_to_split_file       = root_dir + 'Missing Conservation Area List 240909a.csv'
output_dir               = root_dir + 'Output/Split/'

print("Set your Output dir!")
exit(0)

#df_organisation_lookup = pd.read_csv(organisation_lookup_file)
#df_data_to_split       = pd.read_csv(data_to_split_file, encoding='cp1252')

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
    # print(LPA, org_index)
    entity = df_organisation_lookup["entity"][org_index.values[0]]

    return entity

def clear_output_dir():

    files = glob.glob(output_dir + '/*.csv')
    for f in files:
        try:
           os.remove(f)
        except PermissionError:
           print("Close the file!")
           exit() 


################################################################
################################################################

print("Started")

df_organisation_lookup = pd.read_csv(organisation_lookup_file)
df_data_to_split       = pd.read_csv(data_to_split_file, encoding='cp1252', engine='python')
#df_data_to_split       = pd.read_csv(data_to_split_file, encoding='cp1252')

#print(entity_lookup('Allerdale Borough Council'), short_organisation_lookup('Allerdale Borough Council'))
#print(short_organisation_lookup("Amber Valley Borough Council"))
#print(short_organisation_lookup("Babergh District Council"))

#os.system('whoami')

clear_output_dir()

last_lpa = ""
designation_date = ''
# for row in df_data_to_split.head(180).itertuples(index=False):
for row in df_data_to_split.itertuples(index=False):

    '''
    print(row[0:9][1]) 
    print(row[0:9][3]) 
    print(row[0:9][4]) 
    print(row[0:9][5]) 
    print(row[0:9][6]) 
    print(row[0:9][7]) 
    print(row[0:10][9]) 
    print(row[0:11][10]) 
    '''

    ActualMapURL      = False

    reference         = str(entity_lookup(row[0:9][0])) + "_" + short_organisation_lookup(row[0:9][0])
    name              = row[0:9][1]
    name              = '"' + name + '"'

    document_url      = row[0:9][3]
    if  document_url == 'nan' or document_url == '' or pd.isnull(document_url) or document_url == 'None':
        document_url = "No Appraisal document"
    
    document_url      = '"' + document_url + '"'

    try:
       documentation_url = '"' + row[0:9][2] + '"'
    except:
       print("Exception") 
       print(row[0:9][0])
       documentation_url = ''


    geometry          = ""
    point             = ""
    notes             = str(row[0:9][6])
    organisation      = organisation_lookup(row[0:9][0])
    entry_date        = ""
    start_date        = ""
    end_date          = ""
    ca_entity         = str(row[0:21][20])


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
        # Close last files and ...
        # Close the files
        try:
           f_ca.close()
        except:
           pass 

        try:
           f_cad.close()
        except:
           pass 


        # Open a file for this one!   
        # open_both_files(short_organisation_lookup(row[0:9][0]))        

        f_ca  = open(output_dir + "/" + short_organisation_lookup(row[0:9][0]) + "-conservation-area.csv", "a") 
        #      'organisation'        + delimiter + \
        line = 'reference'           + delimiter + \
               'name'                + delimiter + \
               'designation-date'    + delimiter + \
               'document-url'        + delimiter + \
               'documentation-url'   + delimiter + \
               'geometry'            + delimiter + \
               'point'               + delimiter + \
               'notes'               + delimiter + \
               'entry_date'          + delimiter + \
               'start_date'          + delimiter + \
               'end_date'            + delimiter + \
               'ca_entity'           + '\n' 
   
        f_ca.write( line )
   
        f_cad = open(output_dir + "/" + short_organisation_lookup(row[0:9][0]) + "-conservation-area-document.csv", "a") 
        #       'organisation'       + delimiter + \
        line = 'reference'           + delimiter + \
                'conservation-area'  + delimiter + \
                'name'               + delimiter + \
                'documentation-url'  + delimiter + \
                'document-url'       + delimiter + \
                'document-type'      + delimiter + \
                'notes'              + delimiter + \
                'entry_date'         + delimiter + \
                'start_date'         + delimiter + \
                'end_date'            + delimiter + \
                'ca_entity'           + '\n' 

        f_cad.write( line )


        last_lpa = row[0:9][0]
    else:
        CA_row_number = CA_row_number + 1 

    #      organisation                           + delimiter + \
    line = reference + '_CA' + str(CA_row_number) + delimiter + \
           name                                   + delimiter + \
           designation_date                       + delimiter + \
           document_url                           + delimiter + \
           documentation_url                      + delimiter + \
           geometry                               + delimiter + \
           point                                  + delimiter + \
           notes                                  + delimiter + \
           entry_date                             + delimiter + \
           start_date                             + delimiter + \
           end_date                               + delimiter + \
           ca_entity                              + '\n'

    f_ca.write( line )
    #print(line) 

    # Hmm there may be more than one record here, an appraisal and a map
    # Does best map column F, ident 5, have a map in it?
    # If so we need to add another line for it

    #      organisation                                  + delimiter + \
    line = 'D_' + reference + '_CA' + str(CA_row_number) + "_1" + delimiter + \
           reference + '_CA' + str(CA_row_number)        + delimiter + \
           name                                          + delimiter + \
           documentation_url                             + delimiter + \
           document_url                                  + delimiter + \
           'area-appraisal'                              + delimiter + \
           notes                                         + delimiter + \
           entry_date                                    + delimiter + \
           start_date                                    + delimiter + \
           end_date                                      + delimiter + \
           ca_entity                                     + '\n'

    f_cad.write( line )
    #print(line) 

    if ActualMapURL:

       #   organisation                                  + delimiter + \
       line = 'D_' + reference + '_CA' + str(CA_row_number) + "_2" + delimiter + \
           reference + '_CA' + str(CA_row_number)        + delimiter + \
           name                                          + delimiter + \
           documentation_url                             + delimiter + \
           map                                           + delimiter + \
           'area-map'                                    + delimiter + \
           notes                                         + delimiter + \
           entry_date                                    + delimiter + \
           start_date                                    + delimiter + \
           end_date                                      + delimiter + \
           ca_entity                                     + '\n'

       f_cad.write( line )
       #print(line)

#cp /mnt/c/Users/DavidBrown/Documents/GIS/ExportCAs/Output/conservation-area.csv /var/lib/mysql-files/

try:
   f_ca.close()
except:
   pass 

try:
   f_cad.close()
except:
   pass 


print("Finished")

