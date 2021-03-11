# import necessary packages
#import _mysql
import MySQLdb as mdb
import sys
import asciitable
import edd
import EDD_config


# location of the bar files:
bar_files_dir=EDD_config.bar_files


# MAIN
# connect to mysql database
try:
    db=mdb.connect(EDD_config.host,user=EDD_config.user,passwd=EDD_config.passwd,db=EDD_config.database)
    # accept empty values in integer columns
except:
    print("There was an error connecting to the database")
    exit(1)

    
cur=db.cursor()    
cur.execute("DROP DATABASE IF EXISTS "+EDD_config.database+";CREATE DATABASE "+EDD_config.database+";USE "+EDD_config.database+";")
cur.close()


# create the ktables table
edd.create_tables(db)

# loop through the info file and insert into the ktables table
try:
    f=open("catalogs_info.dat","r")
except:
    print("Error in opening catalogs_info.dat file.")
    exit
    
# initialize an empty table to hold the ktables info
NO_catal = 0 
mydata_tables = []
mydata_columns=[]
coordinates_columns_info={}
special_code=[]
keywords =  ["category","catalog","abbreviation","dbtable","bibcode","description","filename"]
for myline in f:
   try: 
    myline_args=myline.lstrip().rstrip().split("=>")

    if myline_args[0]=="begin":
        # initialise a new catalog dictionary
        mycatalog={}
        # initialise a new list of columns to create the corresponding table
        create_columns=[]
        # assume that we don't have special columns
        coordinates_columns=[]

    if myline_args[0] in keywords:
        mycatalog[myline_args[0]]=myline_args[1]
        #if myline_args[0]=="dbtable":
        #print "Parsing information for catalog: "+myline_args[1]


    if myline_args[0]=="column":
       columns=myline_args[1].split("|")
       columns=[x.lstrip().rstrip() for x in columns]
       #print columns
       if columns[0]=="sql":
            continue
       format=edd.determine_format(columns[1])
       mydata_columns.append([mycatalog["dbtable"],columns[0],columns[2],columns[3],"","r",format])
       create_columns.append([columns[0],columns[1]])

    if myline_args[0]=="coordinate":
      columns=myline_args[1].split("|")
      columns=[x.lstrip().rstrip() for x in columns]
      coordinates_columns.append((columns[0],int(columns[1].lstrip().rstrip())-1,int(columns[2].lstrip().rstrip())))

    if myline_args[0]=="special_code":
      code=myline_args[1]
      special_code.append(code)

    if myline_args[0]=="end":
         print("Finished scanning catalog: "+mycatalog["dbtable"])
         try:
           mydata_tables.append((NO_catal,mycatalog["dbtable"],mycatalog["category"],mycatalog["bibcode"],mycatalog["catalog"],mycatalog["abbreviation"],mycatalog["description"],mycatalog["filename"]))
           NO_catal+=1
         except:
           print("Table "+mycatalog["dbtable"]+" seems to be missing some description information")
           exit()
         mysql_statement="CREATE TABLE "+mycatalog["dbtable"]+"("
         for col_def in create_columns:
            col_def[0]=col_def[0].replace('"','')
            if col_def[1]=="":
                col_def[1]="varchar(3)"
            if "int" in col_def[1]:
               col_def[1]="integer"
            if col_def[0]=="pgc":
               col_def[1]="integer not null"

            mysql_statement=mysql_statement+"`"+col_def[0]+"` "+col_def[1].lower()+","
         if coordinates_columns:
              # we have coordinates! adding two more columns
              print("adding al and de columns to table "+mycatalog["dbtable"])
              mysql_statement=mysql_statement+"`al2000` numeric(20,15),"
              mysql_statement=mysql_statement+"`de2000` numeric(20,15),"
              coordinates_columns_info[mycatalog["dbtable"]]=coordinates_columns
              mydata_columns.append([mycatalog["dbtable"],"al2000","h","Right Ascention (J2000)","","r","%20.15f"])
              mydata_columns.append([mycatalog["dbtable"],"de2000","dec","Declination (J2000)","","r","%20.15f"])

         mysql_statement=mysql_statement+"PRIMARY KEY (`PGC`) );"
         try:
             cur=db.cursor()
             cur.execute(mysql_statement)
             db.commit()
             cur.close()
         except:
             print("Error in creating a table. The SQL statement that created an error was:")
             print("---------")
             print(mysql_statement)
             print("---------")
             print("Suggestion: copy and paste this statement into a mysql window and see what the problem is")
             exit()
   except:
     print("There is something wrong with this line in catalogs_info.dat:")
     print(myline)
     exit()

# insert data into mysql tables
print("Inserting data into ktables...")
cur=db.cursor()
cur.executemany(
    """INSERT INTO ktables (ID_catal,dbtable,category,bibcode,catalog,abbreviation,description,file)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",mydata_tables)
db.commit()

print("Inserting data into kcolumns...")
cur.executemany(
    """INSERT INTO kcolumns(dbtable,tabcolumn,units,description,ucd,justification,format)
    VALUES (%s,%s,%s,%s,%s,%s,%s)""",mydata_columns)
db.commit()
cur.close()

# cycle through the tables using a mysql query

pgc=set();
cur=db.cursor()
cur.execute('SELECT ID_catal,dbtable,category,bibcode,catalog,abbreviation,description,file from ktables ORDER BY ID_catal ASC')
tables=cur.fetchall()
cur.close()
for table in tables:
  dbtable=table[1]
  print('Table Metadata: ', table)
  print("Inserting data into table "+dbtable)
  file=table[7]

  # retrieve the list of columns
  cur=db.cursor()
  cur.execute('SELECT tabcolumn from kcolumns where dbtable="'+dbtable+'"')
  columns=list(cur.fetchall())
  cur.close()

  # open the corresponding bar file
  print("reading file ... "+file)
  data=[]
  f=open(bar_files_dir+"/"+file,"r")
  data=f.readlines()
  print("done")
  # special handling of coordinates
  if dbtable in list(coordinates_columns_info.keys()):
    print("Converting coordinates into el de format for table "+dbtable)
    if dbtable in ['kbothun','kdellan','kpscz','krfgcvel']:
      remove=False
    else:
      remove=True
    data=edd.calculate_el_de(data,coordinates_columns_info[dbtable],remove)
  # actual reading of the file
  data_from_file = []
  for line in data:
    line=line.replace("NaN","").replace("\n","").replace("inf","").replace("nan","").split("|")
    line=[x.rstrip().lstrip() for x in line]
    line=[str(x).encode('cp1252', errors='ignore') if x else '' for x in line]
    if len(line)<=1 or line[0]=='':
        continue
    if ("kleda" not in table):
        pgc.add(int(line[0]))
    data_from_file.append((line))
    
  # prepare the columns format string
  num_columns = len(columns)
  num_elements = len(data_from_file[0])
  print("Number of columns: "+str(num_columns)+" Number of elements: "+str(num_elements))
  if (num_columns!=num_elements):
    print("Warning: the number of columns does not match the number of elements")
    db.close()
    zipped = list(map (lambda x,y: [x,y], columns, data_from_file[0]))
    for tup in zipped:
      print(tup)
    exit()
  format = "%s,"*num_elements
  format = format[:-1]
  # insert data into database
  print("inserting data into database...")
  print("Checking health of lines to be inserted")
  for line in data_from_file:
      if len(line) != num_columns:
          print("A Line has a problem:\n")
          print(line)
          exit()
  cur=db.cursor()
  cur.executemany("INSERT IGNORE INTO "+dbtable+" VALUES ("+format+")", data_from_file)
  db.commit()
  #try:
  #    cur=db.cursor()
  #    cur.executemany("INSERT INTO "+dbtable+" VALUES ("+format+")",data_from_file)
  #    db.commit()
  #except mdb._exceptions.OperationalError as e:
  #    print(e)
  #    #print(data_from_file)
  #    with open('myfile.txt', 'w') as f:
  #        for item in data_from_file:
  #            f.write('%s\n' % item)
  #    sys.exit(1)
              
  print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
  cur.close()

print("generating PGC table from all tables except leda")
cur=db.cursor()
pgc=sorted(pgc)
cur.executemany("INSERT INTO pgc VALUES (%s)",pgc)
db.commit()
cur.close()
print("comparing with pgc from leda")
cur=db.cursor()
cur.execute("select pgc from kleda_orig;")
pgc_leda=cur.fetchall()
pgc_leda=[x[0] for x in pgc_leda]
cur.close()
print("Current number of object in the database: "+str(len(pgc)))
print("Number of objects in Leda:                "+str(len(pgc_leda)))
print(pgc[0])
print(pgc_leda[0])

diff=list(set(pgc)-set(pgc_leda))
#print diff
if (len(diff)>0):
    print("Leda table is incomplete. "+str(len(diff))+" objects are missing")
    answer=edd.query_yes_no("Do you want to retrieve the missing LEDA objects from Lyon?",default="yes")
    if (answer=="yes"):
        edd.generate_kleda_orig_from_lyon(db,diff)

# now generate the actual kleda table from the original
edd.copy_leda_orig_into_leda(db)

print("Applying special mysql code...")
cur=db.cursor()
try:
  for code in special_code:
    print("running code: "+code)
    cur.execute(code)
    db.commit()
except:
  print("Unable to execute special code "+code)
  cur.close()

print("All done")
print("Don't forget to run the sql code to transfer the EDDsDB data into the public database")


db.close()


