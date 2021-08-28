# incubyte database is created manually via pgAdmin application in the database already.

import psycopg2

# connect to the Incubyte Database of Local Machine via psycopg2 python library.
conn = psycopg2.connect(
   database="Incubyte", user='postgres', password='1234', host='localhost'
)

# initialize the cursor object.
cursor = conn.cursor()

# this function checks if the country's table is present in the database or not.
def check_table(table):
    stmt = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='" + table + "')";
    cursor.execute(stmt)
    result = cursor.fetchone()[0]
    return result
    
# this function will create a new table as country's name in the database. 
def create_table(table):
    stmt = '''create table ''' + table + '''(
	Customer_Name varchar(255) primary key,
	Customer_ID varchar(18) not null,
	Customer_Open_Date date not null,
	Last_Consulted_Date date,
	Vaccination_Type char(5),
	Doctor_Consulted char(255),
	State char(5),
	Post_Code integer,
	Date_Of_Birth date,
	Active_Customer char(1)
    )'''
    cursor.execute(stmt)
   
# this function checks if the entry is already exist in the country's table or not.
def check_entry(entry,table):
    stmt = "SELECT EXISTS(SELECT 1 FROM " + table + " WHERE Customer_Name='" + entry + "')";
    cursor.execute(stmt)
    result = cursor.fetchone()[0]
    return result
    
# this function adds new entry into the country's table which is present in the database.
def add_entry(fields,table):
    cursor.execute("INSERT INTO " + table + " (Customer_Name,Customer_ID,Customer_Open_Date,Last_Consulted_Date,Vaccination_Type,Doctor_Consulted,State,Post_Code,Date_Of_Birth,Active_Customer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[8],fields[9],fields[10]))

# read a pipe delimited text file as input.
f = open("DataPipe.txt", "r")

# this for loop will take entries from file and do operations accordingly.
for line in f:
    fields = line.split('|')
    fields = fields[2:]
    fields[len(fields)-1] = fields[len(fields)-1].strip('\n')
    if fields[7]=='\\N':
        continue
    if fields[9]!='\\N':
        fields[9] = fields[9][4:8]+fields[9][2:4]+fields[9][0:2]
    for i in range(len(fields)):
        if fields[i]=='\\N':
            fields[i]=None
    result = check_table(fields[7].lower())
    if not result:
        create_table(fields[7].lower())
    result_entry = check_entry(fields[0],fields[7].lower())
    if not result_entry:
        add_entry(fields,fields[7].lower())

conn.commit()
conn.close()