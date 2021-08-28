# incubyte database is created manually via pgAdmin application in the database already.

import psycopg2
import os

# connect to the Incubyte Database of Local Machine via psycopg2 python library.
conn = psycopg2.connect(
   database="Incubyte", user='postgres', password='1234', host='localhost'
)

# initialize the cursor object.
cursor = conn.cursor()

# this function copies the data from the table to data.txt file.
def extract_data(table):
    stmt = "COPY (SELECT Customer_Name,Customer_ID,to_char(Customer_Open_Date,'YYYYMMDD'),to_char(Last_Consulted_Date,'YYYYMMDD'),trim(Vaccination_Type),trim(Doctor_Consulted),trim(State),trim(Country),Post_Code,to_char(Date_Of_Birth,'DDMMYYYY'),Active_Customer FROM " + table + ") TO 'D:\Study\Placement\Incubyte\Incubyte Technical Assessment\Data Engineer Technical Assessment\Datatemp.txt' (DELIMITER '|');"
    cursor.execute(stmt)

# call the extract data function
extract_data("customer_records")

# to set according to the format of sample file
prefix = '|D|'
dest = ''
with open('Datatemp.txt', 'r') as src:  
    with open('DataPipe.txt', 'w') as dest:  
        for line in src:  
            dest.write('%s%s%s\n' % (prefix, line.rstrip('\n'),""))

os.remove('Datatemp.txt')

conn.commit()
conn.close()